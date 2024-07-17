from django.db import models
import random
import string
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.
class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=125)
    direccion = models.CharField(max_length=125)
    telefono = models.CharField(max_length=125)
    correo = models.EmailField()
    codigo_postal = models.IntegerField()
    vendedor = models.CharField(max_length=125)
    rut_vendedor = models.CharField(max_length=125)
    telefono_vendedor = models.CharField(max_length=125)
    correo_vendedor = models.EmailField()

    def __str__(self):
        return str(self.id_orden)
    
    class Meta:
        db_table = 'db_orden'

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=25)

    def __str__(self):
        return self.estado

    class Meta:
        db_table = 'db_estado'


class EstadoEntrega(models.Model):
    id_estado_entrega = models.AutoField(primary_key=True)
    estado_entrega = models.CharField(max_length=25)

    def __str__(self):
        return self.estado_entrega

    class Meta:
        db_table = 'db_estado_entrega'


class Factura(models.Model):
    id_factura = models.CharField(max_length=10, primary_key=True, editable=False)
    orden = models.ForeignKey('Orden', on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    estado_entrega = models.ForeignKey(EstadoEntrega, on_delete=models.CASCADE)
    subtotal = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.id_factura:
            self.id_factura = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        length = 7
        characters = string.ascii_uppercase + string.digits
        while True:
            unique_id = ''.join(random.choice(characters) for _ in range(length))
            if not Factura.objects.filter(id_factura=unique_id).exists():
                return unique_id

    def __str__(self):
        return self.id_factura

    class Meta:
        db_table = 'db_factura'

class ProductoFactura(models.Model):
    id_producto_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, related_name='productos', on_delete=models.CASCADE)
    producto = models.CharField(max_length=125)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    precio_total = models.IntegerField()

    def __str__(self):
        return str(self.id_producto_factura)

    class Meta:
        db_table = 'db_producto_factura'

class HistorialRechazo(models.Model):
    id_historial = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id_historial)

    class Meta:
        db_table = 'db_historial'

class Aceptacion(models.Model): 
    id_aceptacion = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='aceptacion', null=True)
    direccionAcept = models.CharField(max_length=500)
    rutAcept = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id_aceptacion)

    class Meta:
        db_table = 'db_aceptacion'

def create_initial_estados(sender, **kwargs):
    Estado.objects.get_or_create(estado='Creada')
    Estado.objects.get_or_create(estado='Rectificada')
    Estado.objects.get_or_create(estado='Anulada')
    EstadoEntrega.objects.get_or_create(estado_entrega='Por entregar')
    EstadoEntrega.objects.get_or_create(estado_entrega='Entregado')
    EstadoEntrega.objects.get_or_create(estado_entrega='Rechazado')

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    create_initial_estados(sender, **kwargs)