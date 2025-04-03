from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

# Creamos un namespace para operaciones administrativas
api = Namespace('admin', description='Admin operations')

# Modelo para actualizar un usuario (permite cambiar email y password)
admin_update_user_model = api.model('AdminUpdateUser', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Email del usuario'),
    'password': fields.String(required=True, description='Password for the user')
})

# Modelo para crear un usuario (similar al de usuarios regulares)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Email del usuario'),
    'password': fields.String(required=True, description='Password for the user')
})

# Modelo para Amenity
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Endpoint para que el admin cree un nuevo usuario
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """
        POST /api/v1/admin/users/
        Permite a un administrador crear un nuevo usuario.
        Se verifica que el usuario autenticado tenga privilegios de admin.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        if facade.get_user_by_email(data.get('email')):
            return {'error': 'Email already registered'}, 400
        
        try:
            new_user = facade.create_user(data)
        except ValueError as e:
            return {'error': str(e)}, 400
        
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

# Endpoint para que el admin modifique cualquier usuario
@api.route('/users/<string:user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """
        PUT /api/v1/admin/users/<user_id>
        Permite a un administrador actualizar los datos de cualquier usuario,
        incluyendo email y password. Se asegura que el email no se duplique.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        if 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
            
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        user.update(data)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

# Endpoint para que el admin cree una nueva amenidad
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()  # Asegúrate de usar jwt_required() con paréntesis
    def post(self):
        """
        POST /api/v1/admin/amenities/
        Permite a un administrador crear una nueva amenidad.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        try:
            new_amenity = facade.create_amenity(data)
        except ValueError as e:
            return {'error': str(e)}, 400
        
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

# Endpoint para que el admin modifique una amenidad existente
@api.route('/amenities/<string:amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        """
        PUT /api/v1/admin/amenities/<amenity_id>
        Permite a un administrador actualizar los detalles de una amenidad.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        updated_amenity = facade.update_amenity(amenity_id, data)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200

# Endpoint para que el admin modifique un place sin restricciones de propiedad
@api.route('/places/<string:place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        """
        PUT /api/v1/admin/places/<place_id>
        Permite a un administrador actualizar un place sin restricciones de propiedad.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        try:
            updated_place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': updated_place.owner.id
        }, 200
