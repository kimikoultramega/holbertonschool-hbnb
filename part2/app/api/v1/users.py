from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='Operaciones relacionadas con usuarios')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Email del usuario')
})

# Endpoint para manejar la creación de usuarios y la lista de usuarios

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'Usuario creado con éxito')
    @api.response(400, 'Email ya registrado o datios inválidos')

    def post(self):
        """
        Registra un nuevo usuario
        """
        # Obtenemos el payload (los datos enviados en la petición)
        user_data = api.payload

        # Verificamos si el email ya está registrado.
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email ya registrado'}, 400
        
        # Creamos el usuario utilizando la capa de servicios.
        new_user = facade.create_user(user_data)
        # Retornamos los datos del usuario creado
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201
    @api.response(200, 'Lista de usuarios recuperada con éxito')
    def get(self):
        """
        Recupera la lista de todos los usuarios
        """
        # Recuperamos todos los usuarios desde el repositorio.

        users = facade.user_repo.get_all()

        # Transformamos la lista de objetos en una lista de diccionarios.

        user_list = []

        for user in users:
            user_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                })
        return user_list, 200
    
# Endpoint para manejar la obtención y actualización de un usuario específico
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'Detalles del usuario recuperados correctamente')
    @api.response(404, 'Usuario no encontrado')

    def get(self, user_id):
        """
        Recupera los detalles del usuario por ID
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'Usuario actualizado con éxito')
    @api.response(404, 'Usuario no encontrado')
    def put(self, user_id):
        """
        Actualiza la información de un usuario existente
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404

        # Obtenemos los nuevos datos

        user_data = api.payload

        # Actualizamos el usuario utilizando el método update del modelo (heredado de BaseModel)

        user.update(user_data)

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
