from django import forms

from .models import Client, ClientShoppings
from .enums import IdType

class ClientForm(forms.ModelForm):
    form_type = forms.CharField(widget=forms.HiddenInput(), initial='client_form')

    class Meta:
        model = Client
        fields = [
            'id_type',
            'id_number',
            'name',
            'lastname',
            'email',
            'phone',
            'address',
        ]


class SeekClientForm(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(), initial='seek_client_form')

    id_number = forms.CharField(max_length=20, label='Número de Identificación')
    id_type = forms.ChoiceField(
        choices=[(tag.value, tag.name) for tag in IdType],
        label='Tipo de Identificación',
    )


class ClientShoppingsForm(forms.ModelForm):
    class Meta:
        model = ClientShoppings
        fields = [
            'client',
            'date',
            'amount',
            'name',
            'description',
        ]
