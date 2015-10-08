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
    
    desde = fields.Date('Desde', required=True)
    hasta = fields.Date('Hasta', required=True)
    convenio = fields.Many2One('convenios.convenio', 'Convenio', required=True)


class ConfigInformePagosPorConvenio(Wizard):
    "Configuracion Informe Pagos Por Convenio"
    __name__ = 'cooperar-informes.pagosporconvenio'
    start = StateView('cooperar-informes.vistapagosporconvenio.start',
                        'cooperar-informes.view_pagos_por_convenio_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informepagosporconvenio')

    def do_imprimir(self,action):
        
        fechaInicio = self.start.desde.strftime('%Y-%m-%d')
        fechaFin = self.start.hasta.strftime('%Y-%m-%d')
           
        datos = {'desde':fechaInicio, 'hasta':fechaFin, 'convenioid':self.start.convenio.id, 'conveniomonto': self.start.convenio, 'conveniocodigo': self.start.convenio.codigo}
        return action, datos

# Reporte Pagos Por Convenio
# 
class InformePagosPorConvenio(Report):
    """ Reportes de Pagos Por Convenio"""
    __name__ = 'cooperar-informes.informe_pagosporconvenio'

    @classmethod
    def resumir_datos_clientes(cls, convenioid, desde, hasta): 

        pdb.set_trace()

        Pagos = Pool().get('account.voucher')
        #Filtro por convenio
        pagos = Pagos.search([('convenio.id', '=', convenioid), ('voucher_type', '=', 'payment'), ('date','>=', desde), ('date','<=', hasta)])
        
        inicial = 0
        Convenios = Pool().get('convenios.convenio')
        convenio = Convenios.search([('id', '=', convenioid)])
        
        if convenio:
            inicial = convenio[0].monto

        Tuplas_Pagos = []
        Tuplas_Pagos.append(('', '', '', '', '', '', '', '', '', '', 'Saldo Inicial', inicial))
                        
        for pago in pagos:
            #Orden: 
            #Fecha de operacion, Cheque Nro, Medio de Pago, Proveedor, CUIT Prov, Tipo de Comp, Nro Comp, Fecha Comp, Importe Comprobante, Importe pago, "SALDO INICIAL", valor original y DESCONTANDO)
            
            #Numero de cheque si hay
            cheque_nro = ''
            for cheque in pago.issued_check:
                cheque_nro = cheque.name
            #Tipo, Numero, Fecha, Importe de comprobante de alguna linea que este cancelada en las facturas de prov.
            comprobante_tipo = ''
            comprobante_nro = ''
            comprobante_fecha = ''
            comprobante_valor = 0
            for line in pago.lines:
                if int(line.amount) > 0:
                    comprobante_nro = line.name
                    comprobante_valor = line.amount_original
                    Invoice = Pool().get('account.invoice')
                    invoices = Invoice.search([('number', '=', line.name)])
                    if invoices:
                        comprobante_tipo = invoices[0].invoice_type
                        comprobante_fecha = invoice[0].invoice_date

            saldo = inicial - pago.amount_to_pay
            
            Tuplas_Pagos.append((pago.date, cheque_nro, pago.pay_lines[0].pay_mode.name, 
                        pago.party.name, pago.party.vat_number, comprobante_tipo, comprobante_nro, comprobante_fecha,
                        comprobante_valor, pago.amount_to_pay, '', saldo))
             
        return Tuplas_Pagos


    @classmethod
    def parse (cls, report, objects, data, localcontext):

        tuplas = []
        tuplas = cls.resumir_datos_clientes(data['convenioid'],data['desde'],data['hasta'])
        
        return super(InformePagosPorConvenio,cls).parse(report,tuplas,data,localcontext)


