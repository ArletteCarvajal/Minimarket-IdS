from django_cron import CronJobBase, Schedule
from core.models import Producto
from django.core.mail import send_mail
from django.db.models import F

class NotificacionesStock(CronJobBase):
    RUN_EVERY_MINS = 5  # Ejecuta cada 5 minutos

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.notificaciones_stock'  # Identificador único

    def do(self):
        productos_bajo_stock = Producto.objects.filter(stock__lt=F('stock_minimo'))
        productos_reponer = Producto.objects.filter(stock__lt=F('stock_minimo') * 2)  # Ejemplo: productos con el doble del stock mínimo

        if productos_bajo_stock.exists():
            mensaje = "Los siguientes productos tienen bajo stock:\n\n"
            
            # Agrupamos productos por categoría
            categorias = productos_bajo_stock.values_list('categoria', flat=True).distinct()
            for categoria in categorias:
                mensaje += f"\nCategoría: {categoria}\n"
                productos_categoria = productos_bajo_stock.filter(categoria=categoria)
                for producto in productos_categoria:
                    mensaje += f"- {producto.nombre}: {producto.stock} unidades (Mínimo: {producto.stock_minimo})\n"
            
            # Agregar sugerencias de productos a reponer
            if productos_reponer.exists():
                mensaje += "\n\nSugerencias de productos para reponer:\n"
                for producto in productos_reponer:
                    mensaje += f"- {producto.nombre}: {producto.stock} unidades (Mínimo: {producto.stock_minimo})\n"

            send_mail(
                subject="Notificación: Productos con Bajo Stock",
                message=mensaje,
                from_email="noreply@example.com",
                recipient_list=["admin@example.com"],
            )
            print("Correo enviado con éxito.")
        else:
            print("No hay productos con bajo stock.")
