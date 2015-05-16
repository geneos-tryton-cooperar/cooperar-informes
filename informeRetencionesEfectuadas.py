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


class InformeRetencionesEfectuadas(ModelSQL):
    "Informes Retenciones Efectuadas"
    __name__ = "cooperar-informes.informeretencionesefectuadas"


# Wizard Configuracion 

class VistaConfigInformeRetencionesEfectuadas(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Retenciones Efectuadas"
    __name__ = 'cooperar-informes.vistaretencionesefectuadas.start'
    
    desde_date = fields.Date('Desde', required=True)
    hasta_date = fields.Date('Hasta', required=True)


class ConfigInformeRetencionesEfectuadas(Wizard):
    "Configuracion Informe Retenciones Efectuadas"
    __name__ = 'cooperar-informes.retencionesefectuadas'
    start = StateView('cooperar-informes.vistaretencionesefectuadas.start',
                        'cooperar-informes.view_retenciones_efectuadas_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informeretencionesefectuadas')

    def do_imprimir(self,action):

        datos = {}
              
        datos = {'desdefecha':str(self.start.desde_date), 'hastafecha':str(self.start.hasta_date)}

        return action, datos

# Reporte Retenciones Efectuadas
# 
class InformeRetencionesEfectuadas(Report):
    """ Reportes de Retenciones Efectuadas"""
    __name__ = 'cooperar-informes.informe_retencionesefectuadas'

    @classmethod
    def resumir_datos_clientes(cls, desdefecha, hastafecha): 

        RetencionesEfectuadas = Pool().get('account.retencion.efectuada')
        retencionesefectuadas = RetencionesEfectuadas.search([('date', '>=', desdefecha),('date', '<=', hastafecha)])
        
        Tuplas_Retenciones = []

        for retencionefectuada in retencionesefectuadas:
            Tuplas_Retenciones.append((retencionefectuada.party.name, retencionefectuada.date, retencionefectuada.tax.name, retencionefectuada.aliquot, retencionefectuada.amount))

        return Tuplas_Retenciones


    @classmethod
    def parse (cls, report, objects, data, localcontext):

        tuplas = []
        tuplas = cls.resumir_datos_clientes(data['desdefecha'],data['hastafecha'])
        
        return super(InformeRetencionesEfectuadas,cls).parse(report,tuplas,data,localcontext)


