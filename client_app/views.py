from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from .models import Client, ClientShoppings
from .forms import (
    ClientForm, SeekClientForm, ClientShoppingsForm
)
from .serializers import ClientSerializer
from .enums import IdType
from .constants import AMOUNT_LOYALTY, DATE_LIMIT_LOYALTY


class ClientByDocumentAPIView(APIView):
    def get(self, request, id_number):
        try:
            client = Client.objects.get(id_number=id_number)
            serializer = ClientSerializer(client)

            response = serializer.data.copy()
            response['id_type'] = IdType(client.id_type).name

            return Response(response, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)


def export_client_csv(request, client_id):
    try:
        # Obtener el cliente por su ID
        client = Client.objects.get(id=client_id)

        today = datetime.today()
        last_month = today - timedelta(days=DATE_LIMIT_LOYALTY)

        # Obtener todas las compras del cliente en el último mes
        client_shoppings_last_month = ClientShoppings.objects.filter(
            client=client,
            date__gte=last_month,  # Compras desde hace un mes
            date__lte=today        # Compras hasta hoy
        )

        # Verificar si el cliente puede ser fidelizado
        total_amount_last_month = sum(shopping.amount for shopping in client_shoppings_last_month)

        # Crear un DataFrame con la información del cliente
        data = {
            'Nombre': [client.name],
            'Apellido': [client.lastname],
            'Tipo de Documento': [client.get_id_type_name()],
            'Número de Documento': [client.id_number],
            'Email': [client.email],
            'Teléfono': [client.phone],
            'Dirección': [client.address],
            'Monto Total del Último Mes': [total_amount_last_month],
            'Puede ser fidelizado': [total_amount_last_month > AMOUNT_LOYALTY],
        }
        df = pd.DataFrame(data)

        # Crear una respuesta HTTP con el archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="cliente_{client.id_number}.csv"'

        # Exportar el DataFrame a CSV
        df.to_csv(response, index=False, encoding='utf-8')
        return response

    except Client.DoesNotExist:
        return HttpResponse("Cliente no encontrado", status=404)


def home(request):
    return render(request, 'base.html')


def clients(request):
    context = {
        'clients': Client.objects.all()
    }

    if request.method == 'POST':
        # Determinar cuál formulario se envió
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'seek_client_form':
                # Solo procesar seek_client_form
                seek_client_form = SeekClientForm(request.POST)
                form = ClientForm()  # No validar este formulario

                if seek_client_form.is_valid():
                    id_number = seek_client_form.cleaned_data['id_number']
                    id_type = seek_client_form.cleaned_data['id_type']
                    clients = Client.objects.filter(
                        id_number=id_number,
                        id_type=id_type
                    )
                    context['clients'] = clients
            elif request.POST['form_type'] == 'client_form':
                # Solo procesar form
                form = ClientForm(request.POST)
                seek_client_form = SeekClientForm()  # No validar este formulario

                if form.is_valid():
                    id_type = form.cleaned_data['id_type']
                    id_number = form.cleaned_data['id_number']
                    name = form.cleaned_data['name']
                    lastname = form.cleaned_data['lastname']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    address = form.cleaned_data['address']

                    client = Client(
                        id_type=id_type,
                        id_number=id_number,
                        name=name,
                        lastname=lastname,
                        email=email,
                        phone=phone,
                        address=address
                    )
                    client.save()
                    return redirect('clients')
    else:
        # Si no es POST, inicializar ambos formularios vacíos
        form = ClientForm()
        seek_client_form = SeekClientForm()

    # Agregar ambos formularios al contexto
    context['form'] = form
    context['seek_client_form'] = seek_client_form

    return render(request, 'clients.html', context)


def clientshopping(request):
    context = {
        'clientshoppings': ClientShoppings.objects.all
    }

    if request.method == 'POST':
        form = ClientShoppingsForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            amount = form.cleaned_data['amount']
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']

            clientshopping = ClientShoppings(
                client=client,
                date=date,
                amount=amount,
                name=name,
                description=description
            )
            clientshopping.save()
            return redirect('clientshopping')
    else:
        form = ClientShoppingsForm()

    context['form'] = form

    return render(request, 'clientshopping.html', context)
