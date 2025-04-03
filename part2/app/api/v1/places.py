from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

# Creamos un namespace para agrupar los endpoints relacionados con places.
api = Namespace('places', description='Place operations')

# Modelo para las reviews dentro de un place.
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the review (1-5)'),
    'user_id': fields.String(description='ID of the user who wrote the review')
})

# Modelo para el owner (User) asociado a un place.
user_model = api.model(
    'PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Modelo para las amenities asociadas a un place.
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Modelo principal para Place, usado para la validación de entrada.
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenity IDs"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required() # Solo usuarios autenticados pueden crear places
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        POST /api/v1/places/
        Registra un nuevo place. Se fuerza que el owner_id sea el del usuario autenticado.
        """
        current_user = get_jwt_identity()
        place_data = api.payload  # Extraemos el payload (datos enviados en la solicitud)
        place_data['owner_id'] = current_user['id']
        try:
            new_place = facade.create_place(place_data)

        except ValueError as e:

            # Si ocurre un error (por ejemplo, owner no encontrado), devolvemos un error 400.
            return {'error': str(e)}, 400
        
        # Retornamos los datos del place creado con un código 201.
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner.id  # Se retorna el id del owner
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        GET /api/v1/places/
        Recupera una lista de todos los places.
        Se retornan atributos básicos de cada place.
        """
        places = facade.get_all_places()
        # Se transforma la lista de objetos en una lista de diccionarios.
        place_list = []
        for place in places:
            place_list.append({
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            })
        return place_list, 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        GET /api/v1/places/<place_id>
        Recupera los detalles de un place específico.
        Se incluyen detalles del owner y de las amenities asociadas.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Construimos la respuesta incluyendo información del owner y las amenities
        response = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities],
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in place.reviews]
        }
        return response, 200


    @jwt_required() # Solo el propietario puede actualizar
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        PUT /api/v1/places/<place_id>
        Actualiza la información de un place existente.
        Se permite actualizar atributos como title, description, price, latitude y longitude.
        """
        current_user = get_jwt_identity()

        print("Place ID recibido para actualizar:", place_id)

        place = facade.get_place(place_id)

        print("Resultado de facade.get_place:", place)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Validar que el usuario autenticado es el propietario
        
        if str(place.owner.id) != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        place_data = api.payload
        # Forzar que el owner_id sea el del usuario autenticado
        place_data['owner_id'] = current_user['id']

        try:
            updated_place = facade.update_place(place_id, place_data)

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
