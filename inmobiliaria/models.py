from django.db import models
from django.contrib.auth.models import User

# --------------------------
# PERFIL DE USUARIO (ROLES)
# --------------------------
class Perfil(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('agente', 'Agente')
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

    def __str__(self):
        return self.usuario.username


# --------------------------
# PROPIEDADES
# --------------------------
class Propiedad(models.Model):
    TIPO_CHOICES = [
        ('Casa', 'Casa'),
        ('Departamento', 'Departamento'),
        ('Local', 'Local')
    ]

    OP_CHOICES = [
        ('Renta', 'Renta'),
        ('Venta', 'Venta')
    ]

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('rentada', 'Rentada'),
        ('vendida', 'Vendida')
    ]

    agente = models.ForeignKey(User, on_delete=models.CASCADE)

    foto = models.ImageField(upload_to='propiedades/')
    direccion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    operacion = models.CharField(max_length=10, choices=OP_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estacionamiento = models.BooleanField(default=False)

    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='disponible'
    )

    def __str__(self):
        return self.direccion


# --------------------------
# CONTRATOS
# --------------------------
class Contrato(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    inquilino = models.CharField(max_length=100)

    archivo_pdf = models.FileField(upload_to='contratos/')

    fecha_firma = models.DateField()
    fecha_vencimiento = models.DateField()
    plazo_meses = models.IntegerField()

    aval_requerido = models.BooleanField(default=False)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contrato de {self.inquilino}"
    
