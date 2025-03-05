# falabella-challenge
Falabella Challenge

# Documentación Técnica del Proyecto Django

Este proyecto es una aplicación Django que gestiona clientes y sus compras. Incluye una API para consultar información de clientes, exportar datos en formato CSV y un frontend para interactuar con la aplicación.

---

## Requisitos Previos

- **Python**: 3.13.1 o superior.
- **Docker**: Para ejecutar el proyecto en un contenedor.

---

## Estructura del Proyecto

```
project/
├── app/
│   ├── models.py          # Modelos de la base de datos
│   ├── views.py           # Vistas y lógica de negocio
│   ├── serializers.py     # Serializadores para la API
│   ├── urls.py            # Rutas de la API
│   └── templates/         # Plantillas HTML
├── scripts/
│   └── run.sh             # Script para ejecutar el servidor
├── requirements.txt       # Dependencias del proyecto
├── Dockerfile             # Configuración de Docker
└── docker-compose.yml     # Configuración de Docker Compose
```

---

## Endpoints de la API

### 1. Consultar Cliente por Número de Documento
- **URL**: `/api/clients/<str:id_number>/`
- **Método**: `GET`
- **Descripción**: Devuelve la información de un cliente basado en su número de documento.
- **Ejemplo**:
  ```bash
  GET /api/clients/123456789/
  ```
  **Respuesta**:
  ```json
  {
      "id": 1,
      "name": "Juan",
      "lastname": "Pérez",
      "id_type": 1,
      "id_number": "123456789",
      "email": "juan.perez@example.com",
      "phone": "555-1234",
      "address": "Calle Falsa 123"
  }
  ```

### 2. Exportar Información del Cliente en CSV
- **URL**: `/export-client-csv/<int:client_id>/`
- **Método**: `GET`
- **Descripción**: Exporta la información de un cliente en formato CSV, incluyendo si puede ser fidelizado y el monto total de compras del último mes.
- **Ejemplo**:
  ```bash
  GET /export-client-csv/1/
  ```
  **Respuesta**: Un archivo CSV descargable con la siguiente estructura:
  ```csv
  Nombre,Apellido,Tipo de Documento,Número de Documento,Email,Teléfono,Dirección,Monto Total del Último Mes,Puede ser fidelizado
  Juan,Pérez,CC,123456789,juan.perez@example.com,555-1234,Calle Falsa 123,2500000.00,True
  ```

## Pasos para Ejecutar el Proyecto con Docker

### 1. Construir la Imagen de Docker

Ejecuta el siguiente comando para construir la imagen del contenedor:

```bash
docker-compose build
```

### 2. Iniciar el Contenedor

Inicia el contenedor con Docker Compose:

```bash
docker-compose up
```

Esto levantará el servidor Django en `http://localhost:8000`.

### 3. Acceder a la Aplicación

- **Frontend**: Abre tu navegador y visita `http://localhost:8000`.
- **API**: Puedes hacer solicitudes a los endpoints de la API usando herramientas como `curl` o Postman.

### 4. Detener el Contenedor

Para detener el contenedor, ejecuta:

```bash
docker-compose down
```

---

## Script de Ejecución (`scripts/run.sh`)

El script `run.sh` se utiliza para ejecutar el servidor Django dentro del contenedor.

```bash
#!/bin/bash

# Aplicar migraciones
python manage.py migrate

# Iniciar el servidor
python manage.py runserver 0.0.0.0:8000
```

Asegúrate de que el script tenga permisos de ejecución:

```bash
chmod +x scripts/run.sh
```

---

## Ejemplos de Uso

### 1. Consultar un Cliente por Número de Documento

```bash
curl -X GET http://localhost:8000/api/clients/123456789/
```

### 2. Exportar Información del Cliente en CSV

```bash
curl -X GET http://localhost:8000/export-client-csv/1/ --output cliente_123456789.csv
```

---

## Preguntas Frecuentes

### 1. ¿Cómo puedo acceder al contenedor para depurar?

Puedes acceder al contenedor en ejecución con:

```bash
docker exec -it web /bin/bash
```

### 2. ¿Cómo puedo reiniciar el servidor Django?

Detén y levanta el contenedor nuevamente:

```bash
docker-compose down
docker-compose up
```

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

¡Gracias por usar esta aplicación! 😊
