from django.db import models
from django.contrib.auth.models import User

# Modelo que representa los bienes raíces disponibles
class Propiedad(models.Model):
    # Opciones predefinidas para los campos tipo lista desplegable
    TIPO_CHOICES = [('Casa', 'Casa'), ('Departamento', 'Departamento'), ('Local', 'Local')]
    OP_CHOICES = [('Renta', 'Renta'), ('Venta', 'Venta')]
    foto = models.ImageField(upload_to='propiedades/')
    direccion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    operacion = models.CharField(max_length=10, choices=OP_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estacionamiento = models.BooleanField(default=False)
    estado = models.BooleanField(default=False) 

# Modelo que registra los acuerdos legales vinculados a una propiedad
class Contrato(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    inquilino = models.CharField(max_length=100)
    archivo_pdf = models.FileField(upload_to='contratos/')
    fecha_firma = models.DateField()
    fecha_vencimiento = models.DateField()
    plazo_meses = models.IntegerField()
    aval_requerido = models.BooleanField(default=False)
