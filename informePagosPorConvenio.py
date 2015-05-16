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


class InformePagosPorConvenio(ModelSQL):
    "Informes Pagos por Convenio"
    __name__ = "cooperar-informes.informepagosporconvenio"


# Wizard Configuracion 

class VistaConfigInformePagosPorConvenio(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Pagos Por Convenio"
    __name__ = 'cooperar-informes.vistapagosporconvenio.start'
    
    tipo_convenio = fields.Selection([
        ('inaes', 'Inaes'),
        ('cooperar', 'Cooperar')], 'Tipo de Convenio', select=True)

    convenio = fields.Many2One('convenios.convenio', 'Convenio')


class ConfigInformePagosPorConvenio(Wizard):
    "Configuracion Informe Pagos Por Convenio"
    __name__ = 'cooperar-informes.pagosporconvenio'
    start = StateView('cooperar-informes.vistapagosporconvenio.start',
                        'cooperar-informes.view_pagos_por_convenio_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informepagosporconvenio')

    def do_imprimir(self,action):

        datos = {}
        if self.start.convenio:
            if self.start.tipo_convenio:
                datos = {'tipo_convenio':self.start.tipo_convenio, 'convenioid':self.start.convenio.id, 'conveniomonto': self.start.convenio.monto, 'conveniocodigo': self.start.convenio.codigo}
            else:
                datos = {'tipo_convenio':'', 'convenioid':'', 'conveniomonto': '', 'conveniocodigo': ''}    
        else:
            if self.start.tipo_convenio:
                datos = {'tipo_convenio':self.start.tipo_convenio, 'convenioid':'', 'conveniomonto': '', 'conveniocodigo': ''}
            else:
                datos = {'tipo_convenio':'', 'convenioid':'', 'conveniomonto': '', 'conveniocodigo': ''}
               
        return action, datos

# Reporte Pagos Por Convenio
# 
class InformePagosPorConvenio(Report):
    """ Reportes de Pagos Por Convenio"""
    __name__ = 'cooperar-informes.informe_pagosporconvenio'

    @classmethod
    def resumir_datos_clientes(cls, tipo_convenio, convenioid): 

        Pagos = Pool().get('account.voucher')
        if tipo_convenio != '':
            #Filtro por Tipo de Convenio
            pagos = Pagos.search([('convenio.tipo_convenio', '=', tipo_convenio), ('voucher_type', '=', 'payment')])
        else:
            #Filtro por convenio
            pagos = Pagos.search([('convenio.id', '=', convenioid), ('voucher_type', '=', 'payment')])
        
        Tuplas_Pagos = []

        for pago in pagos:
            Tuplas_Pagos.append((pago.party.name, pago.number, pago.date, pago.state, pago.amount))

        return Tuplas_Pagos


    @classmethod
    def parse (cls, report, objects, data, localcontext):

        tuplas = []
        tuplas = cls.resumir_datos_clientes(data['tipo_convenio'], data['convenioid'])
        
        return super(InformePagosPorConvenio,cls).parse(report,tuplas,data,localcontext)


