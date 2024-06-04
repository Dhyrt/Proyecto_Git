from django.db import models
import random
import string

# Create your models here.
class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=125)
    direccion = models.CharField(max_length=125)
    telefono = models.CharField(max_length=125)
    correo = models.EmailField()
    codigo_postal = models.IntegerField()

    def __str__(self):
        return str(self.id_orden)
    
    class Meta:
        db_table = 'db_orden'

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.CharField(max_length=125)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    precio_total = models.IntegerField()
    subtotal = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return str(self.id_factura)
    
    class Meta:
        db_table = 'db_factura'

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=25)

    def __str__(self):
        return self.estado
    
    class Meta:
        db_table = 'db_estado'

class EstadoOrden(models.Model):
    id_estado_orden = models.CharField(max_length=10, primary_key=True, editable=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id_estado_orden:
            self.id_estado_orden = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        length = 7
        characters = string.ascii_uppercase + string.digits
        while True:
            unique_id = ''.join(random.choice(characters) for _ in range(length))
            if not EstadoOrden.objects.filter(id_estado_orden=unique_id).exists():
                return unique_id

    def __str__(self):
        return self.id_estado_orden
    
    class Meta:
        db_table = 'db_estado_orden'