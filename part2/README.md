# HBnB Application API

Este proyecto es la parte 3 del proyecto HBnB y consiste en el desarrollo de una API RESTful para gestionar diversas entidades (usuarios, lugares, reseñas y amenidades) utilizando un enfoque modular con separación en capas:

- **Presentación (API):** Endpoints implementados con Flask-RESTx que validan y documentan las peticiones.
- **Lógica de Negocio (Modelos):** Clases que encapsulan la validación, relaciones y reglas de negocio de cada entidad.
- **Persistencia:** Un repositorio en memoria que simula el almacenamiento de datos y que, en futuras versiones, podrá reemplazarse por una base de datos real.
- **Patrón Facade:** La clase `HBnBFacade` centraliza la lógica de negocio y la comunicación entre la capa de presentación y la persistencia, simplificando la implementación de los endpoints.

---

## Estructura del Proyecto

```
hbnb/
├── app/                          # Código fuente de la aplicación
│   ├── __init__.py               # Configuración y creación de la app Flask, registro de extensiones y blueprints
│   ├── api/                      # Endpoints de la API
│   │   ├── __init__.py
│   │   └── v1/                   # Versión 1 de la API
│   │       ├── __init__.py
│   │       ├── admin.py         # Endpoints para operaciones administrativas (usuarios, amenities y places)
│   │       ├── amenities.py     # Endpoints para gestión de amenidades
│   │       ├── auth.py          # Endpoints para autenticación (login y rutas protegidas)
│   │       ├── places.py        # Endpoints para gestión de lugares
│   │       ├── reviews.py       # Endpoints para gestión de reseñas
│   │       └── users.py         # Endpoints para gestión de usuarios
│   ├── models/                   # Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── base_model.py        # Clase base con atributos comunes (id, created_at, updated_at)
│   │   ├── user.py              # Modelo de Usuario
│   │   ├── place.py             # Modelo de Lugar
│   │   ├── review.py            # Modelo de Reseña
│   │   └── amenity.py           # Modelo de Amenidad
│   ├── services/                 # Capa de servicios (Facade)
│   │   ├── __init__.py          # Instancia singleton de la fachada
│   │   └── facade.py            # Implementación del patrón Facade para operaciones (crear, actualizar, etc.)
│   └── persistence/              # Capa de persistencia
│       ├── __init__.py
│       └── repository.py        # Repositorio en memoria (implementa CRUD básico)
├── tests/                        # Pruebas unitarias para modelos y endpoints
│   ├── __init__.py
│   ├── test_user.py             # Tests para el modelo User y endpoints
│   ├── test_place.py            # Tests para el modelo Place y sus relaciones
│   ├── test_review.py           # Tests para el modelo Review y endpoints
│   └── test_amenity.py          # Tests para el modelo Amenity y endpoints
├── run.py                        # Punto de entrada para ejecutar la aplicación
├── config.py                     # Configuración global (SECRET_KEY, DEBUG, etc.)
├── requirements.txt              # Lista de dependencias (Flask, flask-restx, flask-jwt_extended, bcrypt, etc.)
└── README.md                     # Este documento

```

---

## Características Principales

### Endpoints de Autenticación (Auth)

- **POST /api/v1/auth/login:**
    
    Autentica a un usuario y devuelve un token JWT.
    
- **GET /api/v1/auth/protected:**
    
    Endpoint protegido que requiere un token JWT válido.
    

### Endpoints de Usuario (User)

- **POST /api/v1/users/:**
    
    Crea un nuevo usuario, verificando que el email no esté registrado.
    
- **GET /api/v1/users/<user_id>:**
    
    Recupera los detalles de un usuario por su ID.
    
- **GET /api/v1/users/:**
    
    Lista todos los usuarios registrados.
    
- **PUT /api/v1/users/<user_id>:**
    
    Actualiza la información de un usuario existente (solo se permiten cambios en `first_name` y `last_name`).
    

### Endpoints de Amenidad (Amenity)

- **POST /api/v1/amenities/:**
    
    Registra una nueva amenidad.
    
- **GET /api/v1/amenities/:**
    
    Recupera una lista de todas las amenidades.
    
- **GET /api/v1/amenities/<amenity_id>:**
    
    Recupera los detalles de una amenidad específica.
    
- **PUT /api/v1/amenities/<amenity_id>:**
    
    Actualiza la información de una amenidad existente.
    

### Endpoints de Lugar (Place)

- **POST /api/v1/places/:**
    
    Registra un nuevo lugar. El `owner_id` se asigna automáticamente al usuario autenticado.
    
- **GET /api/v1/places/:**
    
    Lista todos los lugares con información básica.
    
- **GET /api/v1/places/<place_id>:**
    
    Recupera los detalles completos de un lugar, incluyendo su propietario, amenities y reseñas.
    
- **PUT /api/v1/places/<place_id>:**
    
    Actualiza un lugar. Solo el propietario (usuario autenticado) puede modificarlo.
    

### Endpoints de Reseña (Review)

- **POST /api/v1/reviews/:**
    
    Registra una nueva reseña, validando que el usuario no reseñe su propio lugar y que no se repita la reseña para el mismo lugar.
    
- **GET /api/v1/reviews/:**
    
    Lista todas las reseñas.
    
- **GET /api/v1/reviews/<review_id>:**
    
    Recupera los detalles de una reseña específica.
    
- **PUT /api/v1/reviews/<review_id>:**
    
    Actualiza una reseña (solo el autor puede hacerlo).
    
- **DELETE /api/v1/reviews/<review_id>:**
    
    Elimina una reseña (solo el autor puede eliminarla).
    
- **GET /api/v1/places/<place_id>/reviews:**
    
    Lista todas las reseñas asociadas a un lugar específico.
    

### Endpoints Administrativos (Admin)

- **POST /api/v1/admin/users/:**
    
    Permite a un administrador crear un nuevo usuario.
    
- **PUT /api/v1/admin/users/<user_id>:**
    
    Permite a un administrador modificar cualquier usuario.
    
- **POST /api/v1/admin/amenities/:**
    
    Permite a un administrador crear una nueva amenidad.
    
- **PUT /api/v1/admin/amenities/<amenity_id>:**
    
    Permite a un administrador actualizar una amenidad.
    
- **PUT /api/v1/admin/places/<place_id>:**
    
    Permite a un administrador modificar un lugar sin restricciones de propiedad.
    

---

## Patrón Facade

La clase `HBnBFacade` (en `app/services/facade.py`) centraliza la lógica de negocio y la comunicación con los repositorios. Esto permite que los endpoints se mantengan ligeros y enfocados en la interacción HTTP, mientras que la validación y el manejo de datos se realizan en un único lugar.

---

## Persistencia en Memoria

La capa de persistencia está implementada a través de un repositorio en memoria (`InMemoryRepository` en `app/persistence/repository.py`) que simula las operaciones CRUD. Esta implementación puede ser sustituida en el futuro por una solución basada en bases de datos, como SQLAlchemy.

---

## Validación de Datos

- **A nivel de API:**
    
    Se utilizan modelos y validaciones proporcionadas por Flask-RESTx para asegurar que el formato de las peticiones sea correcto.
    
- **A nivel de Modelos:**
    
    Cada clase valida sus datos en el constructor y utiliza excepciones (`ValueError`) para evitar la creación de instancias con datos inválidos.
    

---

## Cómo Ejecutar la Aplicación

1. **Clonar o descargar el proyecto:**
    
    Asegúrate de tener el proyecto en tu máquina.
    
2. **Instalar las dependencias:**
    
    Desde el directorio raíz del proyecto (donde se encuentra `requirements.txt`), ejecuta:
    
    ```
    pip install -r requirements.txt
    
    ```
    
    Esto instalará Flask, flask-restx, flask-jwt_extended, bcrypt y otras dependencias necesarias.
    
3. **Ejecutar la aplicación:**
    
    Desde la raíz del proyecto, ejecuta:
    
    ```
    python run.py
    
    ```
    
    Flask se iniciará en el puerto 5000 por defecto y verás un mensaje similar a:
    
    ```
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    
    ```
    
4. **Probar los Endpoints:**
    
    Puedes usar Postman, cURL o tu navegador para hacer peticiones. Algunos ejemplos:
    
    - Crear un usuario:
        
        ```bash
        curl -X POST http://localhost:5000/api/v1/users/ \
          -H "Content-Type: application/json" \
          -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
        
        ```
        
    - Crear una amenidad:
        
        ```bash
        curl -X POST http://localhost:5000/api/v1/amenities/ \
          -H "Content-Type: application/json" \
          -d '{"name": "Wi-Fi"}'
        
        ```
        
    - Autenticarse (login) y obtener un token:
        
        ```bash
        curl -X POST http://localhost:5000/api/v1/auth/login \
          -H "Content-Type: application/json" \
          -d '{"email": "john.doe@example.com", "password": "yourpassword"}'
        
        ```
        
    
    Utiliza el token obtenido para acceder a rutas protegidas, agregándolo en el header `Authorization` como `Bearer <token>`.
    

---

## Testing

Se han implementado pruebas unitarias para cubrir la funcionalidad de los modelos y endpoints. Las pruebas se encuentran en el directorio `tests/` y pueden ejecutarse mediante:

```
python -m unittest discover tests

```

Esto permitirá validar la creación, actualización y eliminación de usuarios, lugares, reseñas y amenidades.

---

## Documentación Automática

Gracias a Flask-RESTx, la documentación de la API se genera automáticamente. Navega a la URL base (por ejemplo, `http://127.0.0.1:5000/api/v1/`) para explorar la documentación interactiva de la API.

---

## Notas Adicionales

- **Evolución del Proyecto:**
    
    Aunque inicialmente se enfocó en la gestión de usuarios, la misma estructura modular se ha extendido a lugares, reseñas y amenidades. Además, se han agregado endpoints administrativos y de autenticación para mejorar la funcionalidad y seguridad.
    
- **Seguridad:**
    
    Se utiliza JWT para proteger las rutas sensibles y bcrypt para el hash de contraseñas, asegurando que la información de los usuarios se maneje de forma segura.