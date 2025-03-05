from django.urls import path
from .views import clientshopping, ClientByDocumentAPIView, clients, home, export_client_csv

urlpatterns = [
    path('', home, name='home'),
    path('clients/', clients, name='clients'),
    path('clientshopping/', clientshopping, name='clientshopping'),
    path('api/clients/<str:id_number>/', ClientByDocumentAPIView.as_view(), name='client-by-document'),
    path('export-client-csv/<int:client_id>/', export_client_csv, name='export-client-csv'),
]
