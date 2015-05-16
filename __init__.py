from trytond.pool import Pool
from .informeCuotaSostenimiento import InformeCuotaSostenimiento, VistaConfigInformeCuotaSostenimiento, ConfigInformeCuotaSostenimiento, InformeCuotaSostenimiento
from .informeRetencionesEfectuadas import InformeRetencionesEfectuadas, VistaConfigInformeRetencionesEfectuadas, ConfigInformeRetencionesEfectuadas, InformeRetencionesEfectuadas
from .informePrestamos import InformePrestamos, VistaConfigInformePrestamos, ConfigInformePrestamos, InformePrestamos
from .informePagosPorConvenio import InformePagosPorConvenio, VistaConfigInformePagosPorConvenio, ConfigInformePagosPorConvenio, InformePagosPorConvenio
from .informeCuotaSostenimientoperiodo import InformeCuotaSostenimientoPeriodo, VistaConfigInformeCuotaSostenimientoPeriodo, ConfigInformeCuotaSostenimientoPeriodo, InformeCuotaSostenimientoPeriodo
from .informeIvaVentas import InformeIvaVentas, VistaConfigInformeIvaVentas, ConfigInformeIvaVentas, InformeIvaVentas
from .informeIvaCompras import InformeIvaCompras, VistaConfigInformeIvaCompras, ConfigInformeIvaCompras, InformeIvaCompras

def register ():

    Pool.register(
        InformeCuotaSostenimiento,
        InformeRetencionesEfectuadas,
        InformePrestamos, 
        InformePagosPorConvenio,
        InformeCuotaSostenimientoPeriodo, 
        InformeIvaVentas, 
        InformeIvaCompras,  
        VistaConfigInformeCuotaSostenimiento,
        VistaConfigInformeRetencionesEfectuadas,
        VistaConfigInformePrestamos,
        VistaConfigInformePagosPorConvenio,
        VistaConfigInformeCuotaSostenimientoPeriodo, 
        VistaConfigInformeIvaVentas,
        VistaConfigInformeIvaCompras, 
        module='cooperar-informes', type_='model'
        )

    Pool.register(
        ConfigInformeCuotaSostenimiento,
        ConfigInformeRetencionesEfectuadas,
        ConfigInformePrestamos,
        ConfigInformePagosPorConvenio,
        ConfigInformeCuotaSostenimientoPeriodo,
        ConfigInformeIvaVentas,
        ConfigInformeIvaCompras,
        module='cooperar-informes', type_='wizard'
        )

    Pool.register(
        InformeCuotaSostenimiento,
        InformeRetencionesEfectuadas,
        InformePrestamos,
        InformePagosPorConvenio,
        InformeCuotaSostenimientoPeriodo,
        InformeIvaVentas, 
        InformeIvaCompras, 
        module='cooperar-informes', type_='report'
        )
