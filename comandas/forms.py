from django import forms
from django.forms import inlineformset_factory
from .models import Plato, Guarnicion, Pedido, ItemPedido

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GuarnicionForm(forms.ModelForm):
    class Meta:
        model = Guarnicion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['numero', 'para_llevar', 'estado']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'para_llevar': forms.CheckboxInput(),
            'estado': forms.HiddenInput(),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['plato', 'cantidad', 'guarniciones', 'comentario']
        widgets = {
            'plato': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.Select(
                attrs={'class': 'form-control'},
                choices=[(i, i) for i in range(1, 11)]
            ),
            'guarniciones': forms.CheckboxSelectMultiple,
            'comentario': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

ItemPedidoFormSet = inlineformset_factory(
    Pedido,
    ItemPedido,
    form=ItemPedidoForm,
    extra=1,
    can_delete=True
)
