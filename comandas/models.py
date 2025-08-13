from django.db import models

class Plato(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Guarnicion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    para_llevar = models.BooleanField(default=False) #type: ignore

    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Pedido #{self.numero}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField(default=1) #type: ignore
    guarniciones = models.ManyToManyField(Guarnicion, blank=True)
    comentario = models.TextField(
        blank=True,
        help_text="Personalización del plato (sin sal, extra queso, etc.)"
    )

    def __str__(self):
        return f"{self.plato.nombre} (Pedido #{self.pedido.numero})" #type: ignore
