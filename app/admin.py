from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Estado)
admin.site.register(Orden)
admin.site.register(Factura)
admin.site.register(ProductoFactura)
admin.site.register(Aceptacion)
admin.site.register(HistorialRechazo)
