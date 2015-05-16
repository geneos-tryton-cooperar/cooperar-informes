#-*- coding: utf-8 -*-

from trytond.pool import Pool
from trytond.report import Report
from trytond.model import ModelSQL, ModelView, Workflow, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button, StateAction
from trytond.transaction import Transaction

from datetime import *
from sql import *
from sql.aggregate import *
from sql.conditionals import *


class InformeCuotaSostenimientoPeriodo(ModelSQL):
    "Informes Cuotas Sostenimiento Periodo"
    __name__ = "cooperar-informes.informecuotasostenimientoperiodo"


# Wizard Configuracion 
class VistaConfigInformeCuotaSostenimientoPeriodo(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Cuota Sostenimiento Periodo"
    __name__ = 'cooperar-informes.vistacuotasostenimientoperiodo.start'
    
    facturado_del_mes = fields.Selection(
        [
            ('1', '01'),
            ('2', '02'),
            ('3', '03'),
            ('4', '04'),
            ('5', '05'),
            ('6', '06'),
            ('7', '07'),
            ('8', '08'),
            ('9', '09'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
        ],
        'Facturado del Mes', required=True
    )
    facturado_del_anio = fields.Integer('Facturado del Anio', required=True)

class ConfigInformeCuotaSostenimientoPeriodo(Wizard):
    "Configuracion Informe Cuota Sostenimiento Periodo"
    __name__ = 'cooperar-informes.cuotasostenimientoperiodo'
    start = StateView('cooperar-informes.vistacuotasostenimientoperiodo.start',
                        'cooperar-informes.view_cuota_sostenimiento_periodo_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informecuotasostenimientoperiodo')

    def do_imprimir(self,action):

        datos = {}
              
        datos = {'facturadomes':self.start.facturado_del_mes, 'facturadoanio':self.start.facturado_del_anio}

        return action, datos

# Reporte Cuota Sostenimiento por Periodo
# 
class InformeCuotaSostenimientoPeriodo(Report):
    """ Reportes de Cuotas Sostenimiento por Periodo"""
    __name__ = 'cooperar-informes.informe_cuotasostenimientoperiodo'

    @classmethod
    def resumir_datos_clientes(cls, facturadomes, facturadoanio): 

        Asociadas = Pool().get('party.party')
        asociadas = Asociadas.search([('asociada', '=', True)])
        
        CuotasAsociada = Pool().get('asociadas.cuota')
 
        Tuplas_Asociadas = []
        
        total_mes = 0
        tipo_factura = ''

        for asociada in asociadas:    
            if asociada.iva_condition == 'responsable_inscripto':
                tipo_factura = 'A'
            else:
                tipo_factura = 'B'
                
            #traigo cuota paga del mes seleccionado
            cuota_paga = CuotasAsociada.search([('asociada', '=', asociada), ('mes', '=', facturadomes), ('anio', '=', facturadoanio), ('pagada', '=', True)])
            if cuota_paga:
                total_mes += cuota_paga[0].monto
                Tuplas_Asociadas.append((asociada.name, str(asociada.monto_actual_cuota), tipo_factura, str(cuota_paga[0].monto)))
            else:
                Tuplas_Asociadas.append((asociada.name, str(asociada.monto_actual_cuota), tipo_factura, '0'))
                
        return Tuplas_Asociadas


    @classmethod
    def get_total_mes(cls, facturadomes, facturadoanio):
        Asociadas = Pool().get('party.party')
        asociadas = Asociadas.search([('asociada', '=', True)])
        CuotasAsociada = Pool().get('asociadas.cuota')
 
        total_mes = 0
        for asociada in asociadas:    
            cuota_paga = CuotasAsociada.search([('asociada', '=', asociada), ('mes', '=', facturadomes), ('anio', '=', facturadoanio), ('pagada', '=', True)])
            if cuota_paga:
                total_mes += cuota_paga[0].monto
                
        return total_mes


    @classmethod
    def parse (cls, report, objects, data, localcontext):

        tuplas = []
        tuplas = cls.resumir_datos_clientes(data['facturadomes'],data['facturadoanio'])
        total_mes = cls.get_total_mes(data['facturadomes'],data['facturadoanio'])
        data['total_mes'] = str(total_mes)

        return super(InformeCuotaSostenimientoPeriodo,cls).parse(report,tuplas,data,localcontext)


