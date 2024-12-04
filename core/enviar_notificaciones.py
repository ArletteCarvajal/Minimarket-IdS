from django.core.management.base import BaseCommand
from core.models import Producto
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Envía notificaciones de productos con bajo stock'

    def handle(self, *args, **kwargs):
        productos_bajo_stock = Producto.objects.filter(stock__lt=models.F('stock_minimo'))
        if productos_bajo_stock.exists():
            mensaje = "Los siguientes productos tienen bajo stock:\n\n"
            for producto in productos_bajo_stock:
                mensaje += f"- {producto.nombre}: {producto.stock} unidades (Mínimo: {producto.stock_minimo})\n"

            send_mail(
                subject="Notificación: Productos con Bajo Stock",
                message=mensaje,
                from_email="noreply@example.com",
                recipient_list=["admin@example.com"],
                fail_silently=False,
            )
            self.stdout.write("Correo enviado con éxito.")
        else:
            self.stdout.write("No hay productos con bajo stock.")
