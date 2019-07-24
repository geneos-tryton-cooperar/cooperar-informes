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


class InformeSubdiarioPagos(ModelSQL):
    "Informes Subdiario Pagos"
    __name__ = "cooperar-informes.informesubdiariopagos"


# Wizard Configuracion 

class VistaConfigInformeSubdiarioPagos(ModelView):
    "Vista Configuracion Parametros Entrada Reporte Subdiario Pagos"
    __name__ = 'cooperar-informes.vistasubdiariopagos.start'
    
    desde = fields.Date('Desde', required=True)
    hasta = fields.Date('Hasta', required=True)
    

class ConfigInformeSubdiarioPagos(Wizard):
    "Configuracion Informe Subdiario Pagos"
    __name__ = 'cooperar-informes.subdiariopagos'
    start = StateView('cooperar-informes.vistasubdiariopagos.start',
                        'cooperar-informes.view_subdiario_pagos_form',
                        [Button('Cancelar','end','tryton-cancel'),
                         Button('Aceptar','imprimir','tryton-go-next')])


    imprimir = StateAction('cooperar-informes.imprimir_informesubdiariopagos')

    def do_imprimir(self,action):

        datos = {}
        fechaInicio = self.start.desde.strftime('%Y-%m-%d')
        fechaFin = self.start.hasta.strftime('%Y-%m-%d')

        datos = {'desde':fechaInicio, 'hasta':fechaFin}

        return action, datos

# Reporte Subdiario Pagos
# 
class InformeSubdiarioPagos(Report):
    """ Reportes de Subdiario Pagos"""
    __name__ = 'cooperar-informes.informe_subdiariopagos'

    @classmethod
    def resumir_datos_subdiario_pagos(cls, desde, hasta): 
        Tuplas_Asientos = []
        #Busco Journal de Pagos
        Journal = Pool().get('account.journal')
        journal = Journal.search([('name', '=', 'Pagos')])
        if journal:
            #Traigo las OPago -> de ese Journal entre fechas (invoice_date)
            Voucher = Pool().get('account.voucher')
            #import pudb;pu.db
            opagos = Voucher.search([('date', '>=', desde),('date', '<=', hasta),('journal', '=', journal[0])], order=[('date', 'ASC')])
            if opagos:
                for opago in opagos:
                    if opago.move: 
                        move_number = opago.move.lines[0].id
                    else: 
                        move_number = ''
                    
                    #Retenciones
                    retenciones_efectuadas = 0
                    retenciones_soportadas = 0
                    if opago.retenciones_efectuadas:
                        for retencion_efectuada in opago.retenciones_efectuadas:
                            retenciones_efectuadas += retencion_efectuada.amount
                    if opago.retenciones_soportadas:
                        for retencion_soportada in opago.retenciones_soportadas:
                            retenciones_soportadas += retencion_soportada.amount
                    
                    Tuplas_Asientos.append((opago.move.date, move_number, 'OPAGO', 
                                            opago.number, opago.date, opago.party.name, opago.party.iva_condition, 
                                            opago.party.vat_number, retenciones_efectuadas, retenciones_soportadas,  opago.amount))
           
            else:    
                #raise error: no hay movimientos para ese diario/periodo
                #cls.raise_user_error('No hay movimientos para el diario VENTAS en el periodo seleccionado.')
                return Tuplas_Asientos
        else:
            #raise error: no hay subdiario de ventas configurado
            #cls.raise_user_error('No hay diario de ventas configurado en el sistema.')
            return Tuplas_Asientos

        return Tuplas_Asientos
    
  
    @classmethod
    def get_totales(cls, desde, hasta, journal): 

        Voucher = Pool().get('account.voucher')
        opagos = Voucher.search([('date', '>=', desde),('date', '<=', hasta),('journal', '=', journal)])
              
        total_retenciones_soportadas = 0
        total_retenciones_efectuadas = 0
        total_pagado = 0
        
        for opago in opagos:
            if opago.retenciones_efectuadas:
                for retencion_efectuada in opago.retenciones_efectuadas:
                        total_retenciones_efectuadas += retencion_efectuada.amount
            if opago.retenciones_soportadas:
                for retencion_soportada in opago.retenciones_soportadas:
                        total_retenciones_soportadas += retencion_soportada.amount        

            total_pagado += opago.amount
            
        Tuplas_Totales = []
        Tuplas_Totales.append((total_retenciones_soportadas, total_retenciones_efectuadas, total_pagado))
        return Tuplas_Totales
    
        

    @classmethod
    def parse (cls, report, objects, data, localcontext):
       
        tuplas = []
        tuplas = cls.resumir_datos_subdiario_pagos(data['desde'],data['hasta'])
        #Totales
        Journal = Pool().get('account.journal')
        journal = Journal.search([('name', '=', 'Pagos')])
        
        data['total_retenciones_soportadas'] = '0'
        data['total_retenciones_efectuadas'] = '0'
        data['total_pagado'] = '0'
        

        if journal:
            tuplas_totales = cls.get_totales(data['desde'],data['hasta'], journal[0])
            data['total_retenciones_soportadas'] = str(tuplas_totales[0][0])
            data['total_retenciones_efectuadas'] = str(tuplas_totales[0][1])
            data['total_pagado'] = str(tuplas_totales[0][2])
        



        return super(InformeSubdiarioPagos,cls).parse(report,tuplas,data,localcontext)


