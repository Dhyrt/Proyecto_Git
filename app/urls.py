from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name ="index"),
    path('registro/', registro, name="registro"),
    path('orden/', orden, name="orden"),
    path('factura/', factura, name="factura"),
    path('factura/<int:orden_id>/', factura, name="factura"),
    path('detalle_factura/<id_factura>/', detalle_factura, name="detalle_factura"),
    path('modificar/<id_factura>/', modificar, name ="modificar"),
]
