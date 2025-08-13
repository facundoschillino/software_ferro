from django.urls import path
from .views import (
    home,
    crear_plato, eliminar_plato,
    crear_guarnicion, eliminar_guarnicion,
    crear_pedido, agregar_items, finalizar_pedido, crear_pedido,eliminar_todos_pedidos, eliminar_pedido, completar_pedido, pedidos_pendientes, pendientes_fragment
)

urlpatterns = [
    path('', home, name='home'),
    path('platos/nuevo/', crear_plato, name='crear_plato'),
    path('platos/eliminar/<int:plato_id>/', eliminar_plato, name='eliminar_plato'),
    path('guarniciones/nuevo/', crear_guarnicion, name='crear_guarnicion'),
    path('guarniciones/eliminar/<int:guarnicion_id>/', eliminar_guarnicion, name='eliminar_guarnicion'),
    path('crear/', crear_pedido, name='crear_pedido'),
    path('items/', agregar_items, name='agregar_items'),
    path('finalizar/', finalizar_pedido, name='finalizar_pedido'),
    path('pedidos/eliminar/<int:pedido_id>/', eliminar_pedido, name='eliminar_pedido'),
    path('pedidos/completar/<int:pedido_id>/', completar_pedido, name='completar_pedido'),
    path('pedidos_pendientes/', pedidos_pendientes, name='pedidos_pendientes'),
    path('pedidos/eliminar_todos/', eliminar_todos_pedidos, name='eliminar_todos_pedidos'),
    path('pendientes/fragmento/', pendientes_fragment, name='pendientes_fragment'),



]
