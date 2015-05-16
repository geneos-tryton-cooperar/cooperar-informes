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


class InformeCuotaSostenimiento(ModelSQL):
    "Informes Cuotas Sostenimiento"
    __name__ = "cooperar-informes.informecuotasostenimiento"


# Wizard Configuracion 

class VistaConfigInformeCuotaSostenimiento(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Cuota Sostenimiento"
    __name__ = 'cooperar-informes.vistacuotasostenimiento.start'
    deuda_al_mes = fields.Selection(
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
        'Deuda al Mes', required=True
    )
    deuda_al_anio = fields.Integer('Deuda al Anio', required=True)

class ConfigInformeCuotaSostenimiento(Wizard):
    "Configuracion Informe Cuota Sostenimiento"
    __name__ = 'cooperar-informes.cuotasostenimiento'
    start = StateView('cooperar-informes.vistacuotasostenimiento.start',
                        'cooperar-informes.view_cuota_sostenimiento_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informecuotasostenimiento')

    def do_imprimir(self,action):

        datos = {}
              
        datos = {'deudames':self.start.deuda_al_mes, 'deudaanio':self.start.deuda_al_anio}

        return action, datos

# Reporte Cuota Sostenimiento
# 
class InformeCuotaSostenimiento(Report):
    """ Reportes de Cuotas Sostenimiento"""
    __name__ = 'cooperar-informes.informe_cuotasostenimiento'

    @classmethod
    def resumir_datos_clientes(cls, deudames, deudaanio): 

        Asociadas = Pool().get('party.party')
        asociadas = Asociadas.search([('asociada', '=', True)])
        
        CuotasAsociada = Pool().get('asociadas.cuota')
 
        Tuplas_Asociadas = []

        #import pudb;pu.db
        for asociada in asociadas:
            cuotas_adeudadas = 0
            monto_adeudado = 0
            ultima_cuota_paga = CuotasAsociada.search([('asociada', '=', asociada)], order=[('mes', 'ASC'), ('anio', 'ASC'),])
            if ultima_cuota_paga:
                if ultima_cuota_paga[0].anio == deudaanio:
                    cuotas_adeudadas = int(deudames) - int(ultima_cuota_paga[0].mes)
                else:
                    anios_diferencia = int(deudaanio) - int(ultima_cuota_paga[0].anio)
                    cuotas_adeudadas = (anios_diferencia - 1) * 12
                    cuotas_adeudadas += deudames
                    cuotas_adeudadas += (12 - int(ultima_cuota_paga[0].mes))

                Tuplas_Asociadas.append((asociada.name, asociada.monto_actual_cuota, str(ultima_cuota_paga[0].mes) + '/' + str(ultima_cuota_paga[0].anio), cuotas_adeudadas, float(cuotas_adeudadas) * float(asociada.monto_actual_cuota)))

            else:
                cuotas_adeudadas = 0
                Tuplas_Asociadas.append((asociada.name, asociada.monto_actual_cuota, 'No se registran cuotas pagas', 'No se registran cuotas pagas', float(cuotas_adeudadas) * float(asociada.monto_actual_cuota)))

        return Tuplas_Asociadas


    @classmethod
    def parse (cls, report, objects, data, localcontext):

        tuplas = []
        tuplas = cls.resumir_datos_clientes(data['deudames'],data['deudaanio'])
        
        #import pudb;pu.db
        return super(InformeCuotaSostenimiento,cls).parse(report,tuplas,data,localcontext)


