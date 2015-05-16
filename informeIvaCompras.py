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


class InformeIvaCompras(ModelSQL):
    "Informes Iva Compras"
    __name__ = "cooperar-informes.informeivacompras"


# Wizard Configuracion 

class VistaConfigInformeIvaCompras(ModelView):
    "Vista Configuracion Parametros Entrada Reporte IVA Compras"
    __name__ = 'cooperar-informes.vistaivacompras.start'
    
    desde = fields.Date('Desde', required=True)
    hasta = fields.Date('Hasta', required=True)
    

class ConfigInformeIvaCompras(Wizard):
    "Configuracion Informe Iva Compras"
    __name__ = 'cooperar-informes.ivacompras'
    start = StateView('cooperar-informes.vistaivacompras.start',
                        'cooperar-informes.view_iva_compras_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informeivacompras')

    def do_imprimir(self,action):

        datos = {}
        fechaInicio = self.start.desde.strftime('%Y-%m-%d')
        fechaFin = self.start.hasta.strftime('%Y-%m-%d')

        datos = {'desde':fechaInicio, 'hasta':fechaFin}

        return action, datos

# Reporte Iva Compras
# 
class InformeIvaCompras(Report):
    """ Reportes de Iva Compras"""
    __name__ = 'cooperar-informes.informe_ivacompras'

    @classmethod
    def resumir_datos_iva_compras(cls, desde, hasta): 

        Invoices = Pool().get('account.invoice')
        invoices_periodo = Invoices.search([('invoice_date', '>=', desde),('invoice_date', '<=', hasta),('type', '=', 'in_invoice')])       

        Tuplas_Facturas = []

        for invoice_periodo in invoices_periodo:
            #Ver Totales
            #Ver Columnas IVA COMPRAS
            #Ver impuestos.grupo: IVA, IIBB, GANANCIAS -> Muestro SOLO IVA
            subtotal_gravado_con_iva = cls.get_total_gravado_con_iva_por_factura(invoice_periodo)
            subtotal_iva = cls.get_total_iva_por_factura(invoice_periodo)
            subtotal_no_gravado_con_iva = cls.get_total_no_gravado_con_iva_por_factura(invoice_periodo)

            Tuplas_Facturas.append((invoice_periodo.invoice_date, invoice_periodo.party.name, invoice_periodo.number, invoice_periodo.party.vat_number, subtotal_gravado_con_iva, subtotal_no_gravado_con_iva, subtotal_iva, invoice_periodo.total_amount))


        return Tuplas_Facturas

    
    @classmethod
    def get_total_no_gravado_con_iva_por_factura(cls, invoice): 

        total_no_gravado = 0
        tiene_iva = False
        for line in invoice.lines:
            for tax in line.taxes:
                if tax.group.name == 'IVA':
                    tiene_iva = True
            if not tiene_iva:
                total_no_gravado += line.amount

        return total_no_gravado

    @classmethod
    def get_total_gravado_con_iva_por_factura(cls, invoice): 

        total_gravado = 0
        for line in invoice.lines:
            for tax in line.taxes:
                if tax.group.name == 'IVA':
                    total_gravado += line.amount
        return total_gravado

    @classmethod
    def get_total_iva_por_factura(cls, invoice): 

        total_iva = 0
        for tax in invoice.taxes:
            if tax.tax.group.name == 'IVA':
                total_iva += tax.amount

        return total_iva

    @classmethod
    def get_totales(cls, desde, hasta): 

        Invoices = Pool().get('account.invoice')
        invoices_periodo = Invoices.search([('invoice_date', '>=', desde),('invoice_date', '<=', hasta),('type', '=', 'in_invoice')])       

        total_gravado_con_iva = 0
        total_iva = 0
        total_no_gravado_con_iva = 0 
        total_facturado = 0
        
        for invoice_periodo in invoices_periodo:
            
            subtotal_gravado_con_iva = cls.get_total_gravado_con_iva_por_factura(invoice_periodo)
            subtotal_iva = cls.get_total_iva_por_factura(invoice_periodo)
            subtotal_no_gravado_con_iva = cls.get_total_no_gravado_con_iva_por_factura(invoice_periodo)

            total_gravado_con_iva += subtotal_gravado_con_iva
            total_iva += subtotal_iva
            total_no_gravado_con_iva += subtotal_no_gravado_con_iva
            total_facturado += invoice_periodo.total_amount
            
        Tuplas_Totales = []
        Tuplas_Totales.append((total_gravado_con_iva, total_iva, total_no_gravado_con_iva, total_facturado))
        return Tuplas_Totales

        

    @classmethod
    def parse (cls, report, objects, data, localcontext):

        tuplas = []
        tuplas = cls.resumir_datos_iva_compras(data['desde'],data['hasta'])
        #Totales
        tuplas_totales = cls.get_totales(data['desde'],data['hasta'])
        
        data['total_gravado_con_iva'] = str(tuplas_totales[0][0])
        data['total_iva'] = str(tuplas_totales[0][1])
        data['total_no_gravado_con_iva'] = str(tuplas_totales[0][2])
        data['total_facturado'] = str(tuplas_totales[0][3])

        return super(InformeIvaCompras,cls).parse(report,tuplas,data,localcontext)


