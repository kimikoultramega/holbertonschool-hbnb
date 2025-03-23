HBnB Application API
Este proyecto es la parte 2 del proyecto HBnB. Se ha desarrollado una API RESTful para gestionar usuarios, aplicando un enfoque modular con separación en capas: Presentación (API), Lógica de Negocio (Modelos) y Persistencia (repositorio en memoria). Además, se utiliza el patrón Facade para orquestar la comunicación entre estas capas.

Estructura del Proyecto
La estructura del proyecto es la siguiente:

bash
Copiar
hbnb/
├── app/                          # Código fuente de la aplicación
│   ├── __init__.py               # Configuración y creación de la app Flask
│   ├── api/                      # Endpoints de la API
│   │   ├── __init__.py
│   │   └── v1/                   # Versión 1 de la API
│   │       ├── __init__.py
│   │       ├── users.py         # Endpoints para gestión de usuarios
│   │       ├── places.py        # Endpoints para gestión de lugares (a implementar)
│   │       ├── reviews.py       # Endpoints para gestión de reseñas (a implementar)
│   │       └── amenities.py     # Endpoints para gestión de amenidades (a implementar)
│   ├── models/                   # Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── base_model.py        # Clase base con atributos comunes (id, created_at, updated_at)
│   │   ├── user.py              # Modelo de Usuario
│   │   ├── place.py             # Modelo de Lugar
│   │   ├── review.py            # Modelo de Reseña
│   │   └── amenity.py           # Modelo de Amenidad
│   ├── services/                 # Capa de servicios (Facade)
│   │   ├── __init__.py          # Instancia singleton de la fachada
│   │   └── facade.py            # Implementación del patrón Facade para operaciones de usuarios, etc.
│   └── persistence/              # Capa de persistencia
│       ├── __init__.py
│       └── repository.py        # Repositorio en memoria (implementa CRUD básico)
├── tests/                        # Pruebas unitarias
│   ├── __init__.py
│   ├── test_user.py             # Tests para el modelo User y endpoints
│   ├── test_place.py            # Tests para el modelo Place y relaciones
│   ├── test_review.py           # Tests para el modelo Review
│   └── test_amenity.py          # Tests para el modelo Amenity
├── run.py                        # Punto de entrada para ejecutar la app
├── config.py                     # Configuración global (por ejemplo, SECRET_KEY, DEBUG, etc.)
├── requirements.txt              # Lista de dependencias (Flask, flask-restx, etc.)
└── README.md                     # Este documento


Características Principales

Endpoints de Usuario (User):

POST /api/v1/users/: Crea un nuevo usuario, verificando que el email no esté registrado.

GET /api/v1/users/<user_id>: Recupera los detalles de un usuario por su ID.

GET /api/v1/users/: Lista todos los usuarios registrados.

PUT /api/v1/users/<user_id>: Actualiza la información de un usuario existente.

Endpoints de Amenidad (Amenity)

POST /api/v1/amenities/: Registra una nueva amenidad.

GET /api/v1/amenities/: Recupera una lista de todas las amenidades.

GET /api/v1/amenities/<amenity_id>: Recupera los detalles de una amenidad específica por su ID.

PUT /api/v1/amenities/<amenity_id>: Actualiza la información de una amenidad existente.

Patrón Facade:

La clase HBnBFacade en app/services/facade.py centraliza la lógica de negocio y la comunicación con el repositorio, facilitando la integración entre la capa de presentación y la persistencia.

Persistencia en Memoria:

Se implementa un repositorio en memoria en app/persistence/repository.py que simula el almacenamiento de datos, y que se podrá reemplazar en futuras partes del proyecto por una solución basada en bases de datos (por ejemplo, con SQLAlchemy).

Validación de Datos:

Se utilizan modelos y validaciones a nivel de API (con Flask-RESTx) y en los modelos (por ejemplo, en el constructor de User) para asegurar que los datos cumplan los requisitos.

Cómo Ejecutar la Aplicación

Clonar o descargar el proyecto:

Asegúrate de tener el proyecto en tu máquina.

Instalar las dependencias:

En el directorio raíz del proyecto (donde se encuentra requirements.txt), ejecuta:

pip install -r requirements.txt

Esto instalará Flask, flask-restx y cualquier otra dependencia necesaria.

Ejecutar la aplicación:
Desde la raíz del proyecto, ejecuta:

python run.py
Flask se iniciará en el puerto 5000 por defecto, y deberías ver un mensaje similar a:

* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Probar los Endpoints:
Puedes usar Postman, cURL o tu navegador para hacer peticiones. Por ejemplo, para crear un usuario:


curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'

curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'

Notas Adicionales
Evolución del Proyecto:
Esta parte se enfoca en la gestión de usuarios, pero la misma estructura se extenderá a otras entidades como Place, Review y Amenity.

Testing:
Se recomienda usar herramientas como Postman para pruebas manuales y frameworks de testing (por ejemplo, pytest) para pruebas automatizadas. El directorio tests/ contiene ejemplos básicos para cada modelo.

Documentación Automática:
Gracias a Flask-RESTx, se genera automáticamente documentación de la API, que puedes revisar navegando a la URL configurada en la documentación (por ejemplo, /api/v1/).
