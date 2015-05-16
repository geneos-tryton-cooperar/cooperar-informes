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


class InformePrestamos(ModelSQL):
    "Informes Prestamos"
    __name__ = "cooperar-informes.informeprestamos"


# Wizard Configuracion 

class VistaConfigInformePrestamos(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Prestamos"
    __name__ = 'cooperar-informes.vistaprestamos.start'
    
    
    asociada = fields.Many2One('party.party', 'Asociada', required=True)
    
   
class ConfigInformePrestamos(Wizard):
    "Configuracion Informe Prestamos"
    __name__ = 'cooperar-informes.prestamos'
    start = StateView('cooperar-informes.vistaprestamos.start',
                        'cooperar-informes.view_prestamos_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informeprestamos')

    def do_imprimir(self,action):

        datos = {}
              
        datos = {'asociadaid': self.start.asociada.id, 'asociadaname': self.start.asociada.name}
        
        return action, datos

# Reporte Prestamos
# 
class InformePrestamos(Report):
    """ Reportes de Prestamos"""
    __name__ = 'cooperar-informes.informe_prestamos'

    @classmethod
    def resumir_datos_clientes(cls, asociadaid): 
        #import pudb;pu.db
        CuotasPrestamos = Pool().get('asociadas.cuotaprestamo')
        cuotasprestamos = CuotasPrestamos.search([('asociada.id', '=', asociadaid)])
        
        Tuplas_CuotasPrestamos = []

        for cuotaprestamo in cuotasprestamos:
            if cuotaprestamo.pagada:
                Tuplas_CuotasPrestamos.append((cuotaprestamo.mes, cuotaprestamo.anio, cuotaprestamo.monto, cuotaprestamo.porcentaje_interes, cuotaprestamo.interes, cuotaprestamo.fecha_vencimiento, 'Si', cuotaprestamo.fecha_pago))
            else:
                Tuplas_CuotasPrestamos.append((cuotaprestamo.mes, cuotaprestamo.anio, cuotaprestamo.monto, cuotaprestamo.porcentaje_interes, cuotaprestamo.interes, cuotaprestamo.fecha_vencimiento, 'No', ''))
                
        return Tuplas_CuotasPrestamos


    @classmethod
    def parse (cls, report, objects, data, localcontext):
        
        tuplas = []
        tuplas = cls.resumir_datos_clientes(data['asociadaid'])
        
        #import pudb;pu.db
        return super(InformePrestamos,cls).parse(report,tuplas,data,localcontext)
        


