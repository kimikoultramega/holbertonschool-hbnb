from flask import Flask
from flask_restx import Api
from config import config
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns
from app.extensions import bcrypt
from flask_jwt_extended import JWTManager

# Crear la instancia de JWTManager
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):

    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    jwt.init_app(app)

    # Se crea la instancia de Api con configuración básica.
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    
    # Se registran los namespaces de usuarios y amenidades.
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    # Bootstrap: Crear un admin si no hay usuarios
    # from app.services.facade import HBnBFacade
    # facade = HBnBFacade()
    from app.services import facade

    if not facade.user_repo.get_all():
        # Crea un admin predeterminado
        from app.models.user import User
        admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": "admin_password"
        }
        admin_user = User(**admin_data)
        admin_user.is_admin = True
        facade.user_repo.add(admin_user)
        print("Bootstrap: Admin user created with id:", admin_user.id)

    users = facade.user_repo.get_all()
    print("Usuarios en el repositorio:", [user.email for user in users])
    
    return app