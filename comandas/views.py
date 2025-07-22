from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import (
    PlatoForm,
    GuarnicionForm,
    PedidoForm,
    ItemPedidoFormSet
)
from .models import Pedido, Plato, Guarnicion, ItemPedido
from django.db.models import Sum

def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_plato')
    else:
        form = PlatoForm()

    platos = Plato.objects.all().order_by('nombre')
    return render(request, 'comandas/crear_plato.html', {
        'form': form,
        'platos': platos
    })

def eliminar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    plato.delete()
    return redirect('crear_plato')

def crear_guarnicion(request):
    if request.method == 'POST':
        form = GuarnicionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_guarnicion')
    else:
        form = GuarnicionForm()

    guarniciones = Guarnicion.objects.all().order_by('nombre')
    return render(request, 'comandas/crear_guarnicion.html', {
        'form': form,
        'guarniciones': guarniciones
    })

def eliminar_guarnicion(request, guarnicion_id):
    guarnicion = get_object_or_404(Guarnicion, id=guarnicion_id)
    guarnicion.delete()
    return redirect('crear_guarnicion')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, ItemPedido
from .forms import PedidoForm, ItemPedidoForm

from django.shortcuts import redirect
from .models import Pedido

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            request.session['pedido_id'] = pedido.id
            return redirect('agregar_items')
    else:
        ultimo = Pedido.objects.order_by('-numero').first()
        siguiente = (ultimo.numero + 1) if ultimo else 1
        form = PedidoForm(initial={'numero': siguiente})

    pedidos_existentes = Pedido.objects.all().annotate(
        total_cantidad=Sum('items__cantidad')
    )

    return render(request, 'comandas/crear_pedido.html', {
        'form': form,
        'pedidos_existentes': pedidos_existentes
    })

def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    return redirect('crear_pedido')
def agregar_items(request):
    pedido_id = request.session.get('pedido_id')
    if not pedido_id:
        return redirect('crear_pedido')
    pedido = get_object_or_404(Pedido, id=pedido_id)
    formset = ItemPedidoFormSet(request.POST or None, instance=pedido)
    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return redirect('agregar_items')
    return render(request, 'comandas/agregar_item.html', {
        'pedido': pedido,
        'formset': formset
    })
    
def completar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'entregado'
    pedido.save()
    return redirect('crear_pedido')

def finalizar_pedido(request):
    request.session.pop('pedido_id', None)
    return redirect('crear_pedido')

def pedidos_pendientes(request):
    pedidos = Pedido.objects.filter(estado__iexact='pendiente').prefetch_related('items__guarniciones', 'items__plato')
    return render(request, 'comandas/pedidos_pendientes.html', {'pedidos': pedidos})

def home(request):
    return render(request, 'comandas/home.html')

@require_POST
def eliminar_todos_pedidos(request):
    Pedido.objects.all().delete()
    return redirect('crear_pedido')
