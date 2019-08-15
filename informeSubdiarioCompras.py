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


class InformeSubdiarioCompras(ModelSQL):
    "Informes Subdiario Compras"
    __name__ = "cooperar-informes.informesubdiariocompras"


# Wizard Configuracion 

class VistaConfigInformeSubdiarioCompras(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Subdiario Compras"
    __name__ = 'cooperar-informes.vistasubdiariocompras.start'
    
    desde = fields.Date('Desde', required=True)
    hasta = fields.Date('Hasta', required=True)
    

class ConfigInformeSubdiarioCompras(Wizard):
    "Configuracion Informe Subdiario Compras"
    __name__ = 'cooperar-informes.subdiariocompras'
    start = StateView('cooperar-informes.vistasubdiariocompras.start',
                        'cooperar-informes.view_subdiario_compras_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informesubdiariocompras')

    def do_imprimir(self,action):

        datos = {}
        fechaInicio = self.start.desde.strftime('%Y-%m-%d')
        fechaFin = self.start.hasta.strftime('%Y-%m-%d')

        datos = {'desde':fechaInicio, 'hasta':fechaFin}

        return action, datos

# Reporte Subdiario Compras
# 
class InformeSubdiarioCompras(Report):
    """ Reportes de Subdiario Compras"""
    __name__ = 'cooperar-informes.informe_subdiariocompras'

    @classmethod
    def resumir_datos_subdiario_compras(cls, desde, hasta): 
        Tuplas_Asientos = []
        #import pudb;pu.db
        #Busco Journal de Compras
        Journal = Pool().get('account.journal')
        journal = Journal.search([('name', '=', 'Compras')])
        #journal = Journal.search([('name', '=', 'Gastos')])
        if journal:
            #Traigo las Invoice -> de ese Journal entre fechas (invoice_date)
            Invoice = Pool().get('account.invoice')
            invoices = Invoice.search([('invoice_date', '>=', desde),('invoice_date', '<=', hasta),('journal', '=', journal[0])], order=[('invoice_date', 'ASC')])
            if invoices:
                for invoice in invoices:
                    if (invoice.state != 'draft') and (invoice.state != 'cancel') and (invoice.state != 'validated'):
                        if invoice.move: 
                            move_number = invoice.move.lines[0].id                        
                        else: 
                            move_number = ''                       
                    
                    #TODO: Tipo de Factura de Proveedor

                    subtotal_gravado_con_iva = cls.get_total_gravado_con_iva_por_factura(invoice)
                    subtotal_iva = cls.get_total_iva_por_factura(invoice)
                    subtotal_no_gravado_con_iva = cls.get_total_no_gravado_con_iva_por_factura(invoice)

                    Tuplas_Asientos.append((invoice.invoice_date, move_number, 'Factura Proveedor', 
                                            invoice.number, invoice.invoice_date, 
                                            invoice.party.name, invoice.party.iva_condition, invoice.party.vat_number, 
                                            subtotal_gravado_con_iva, subtotal_iva, invoice.total_amount))
           
            else:    
                #raise error: no hay movimientos para ese diario/periodo
                #cls.raise_user_error('No hay movimientos para el diario COMPRAS en el periodo seleccionado.')
                return Tuplas_Asientos
        else:
            #raise error: no hay subdiario de compras configurado
            #cls.raise_user_error('No hay diario de compras configurado en el sistema.')
            return Tuplas_Asientos

        return Tuplas_Asientos
    
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
    def get_totales(cls, desde, hasta, journal): 

        Invoices = Pool().get('account.invoice')
        invoices = Invoices.search([('invoice_date', '>=', desde),('invoice_date', '<=', hasta),('journal', '=', journal)])
            

        total_gravado_con_iva = 0
        total_iva = 0
        total_facturado = 0
        
        for invoice_periodo in invoices:
            
            subtotal_gravado_con_iva = cls.get_total_gravado_con_iva_por_factura(invoice_periodo)
            subtotal_iva = cls.get_total_iva_por_factura(invoice_periodo)
            
            total_gravado_con_iva += subtotal_gravado_con_iva
            total_iva += subtotal_iva
            total_facturado += invoice_periodo.total_amount
            
        Tuplas_Totales = []
        Tuplas_Totales.append((total_gravado_con_iva, total_iva, total_facturado))
        return Tuplas_Totales
    
        

    @classmethod
    def parse (cls, report, objects, data, localcontext):
       
        tuplas = []
        tuplas = cls.resumir_datos_subdiario_compras(data['desde'],data['hasta'])
        #Totales
        Journal = Pool().get('account.journal')
        journal = Journal.search([('name', '=', 'Compras')])
        
        data['total_gravado_con_iva'] = '0'
        data['total_iva'] = '0'
        data['total_facturado'] = '0'


        if journal:
            tuplas_totales = cls.get_totales(data['desde'],data['hasta'], journal[0])
            data['total_gravado_con_iva'] = str(tuplas_totales[0][0])
            data['total_iva'] = str(tuplas_totales[0][1])
            data['total_facturado'] = str(tuplas_totales[0][2])

        return super(InformeSubdiarioCompras,cls).parse(report,tuplas,data,localcontext)


