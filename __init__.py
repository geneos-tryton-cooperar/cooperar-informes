from trytond.pool import Pool
from .informeCuotaSostenimiento import InformeCuotaSostenimiento, VistaConfigInformeCuotaSostenimiento, ConfigInformeCuotaSostenimiento, InformeCuotaSostenimiento
from .informeRetencionesEfectuadas import InformeRetencionesEfectuadas, VistaConfigInformeRetencionesEfectuadas, ConfigInformeRetencionesEfectuadas, InformeRetencionesEfectuadas
from .informePrestamos import InformePrestamos, VistaConfigInformePrestamos, ConfigInformePrestamos, InformePrestamos
from .informePagosPorConvenio import InformePagosPorConvenio, VistaConfigInformePagosPorConvenio, ConfigInformePagosPorConvenio, InformePagosPorConvenio
from .informeCuotaSostenimientoperiodo import InformeCuotaSostenimientoPeriodo, VistaConfigInformeCuotaSostenimientoPeriodo, ConfigInformeCuotaSostenimientoPeriodo, InformeCuotaSostenimientoPeriodo
from .informeIvaVentas import InformeIvaVentas, VistaConfigInformeIvaVentas, ConfigInformeIvaVentas, InformeIvaVentas
from .informeIvaCompras import InformeIvaCompras, VistaConfigInformeIvaCompras, ConfigInformeIvaCompras, InformeIvaCompras
from .informeSubdiarioCompras import InformeSubdiarioCompras, VistaConfigInformeSubdiarioCompras, ConfigInformeSubdiarioCompras, InformeSubdiarioCompras
from .informeSubdiarioVentas import InformeSubdiarioVentas, VistaConfigInformeSubdiarioVentas, ConfigInformeSubdiarioVentas, InformeSubdiarioVentas
from .informeSubdiarioPagos import InformeSubdiarioPagos, VistaConfigInformeSubdiarioPagos, ConfigInformeSubdiarioPagos, InformeSubdiarioPagos
from .informeSubdiarioCobros import InformeSubdiarioCobros, VistaConfigInformeSubdiarioCobros, ConfigInformeSubdiarioCobros, InformeSubdiarioCobros


def register ():

    Pool.register(
        InformeCuotaSostenimiento,
        InformeRetencionesEfectuadas,
        InformePrestamos, 
        InformePagosPorConvenio,
        InformeCuotaSostenimientoPeriodo, 
        InformeIvaVentas, 
        InformeIvaCompras, 
        InformeSubdiarioCompras,
        InformeSubdiarioVentas,  
        InformeSubdiarioPagos,
        InformeSubdiarioCobros,    
        VistaConfigInformeCuotaSostenimiento,
        VistaConfigInformeRetencionesEfectuadas,
        VistaConfigInformePrestamos,
        VistaConfigInformePagosPorConvenio,
        VistaConfigInformeCuotaSostenimientoPeriodo, 
        VistaConfigInformeIvaVentas,
        VistaConfigInformeIvaCompras, 
        VistaConfigInformeSubdiarioCompras,
        VistaConfigInformeSubdiarioVentas,
        VistaConfigInformeSubdiarioPagos, 
        VistaConfigInformeSubdiarioCobros,
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
        ConfigInformeSubdiarioCompras,
        ConfigInformeSubdiarioVentas,
        ConfigInformeSubdiarioPagos,
        ConfigInformeSubdiarioCobros,
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
        InformeSubdiarioCompras,
        InformeSubdiarioVentas,
        InformeSubdiarioPagos,
        InformeSubdiarioCobros,
        module='cooperar-informes', type_='report'
        )
