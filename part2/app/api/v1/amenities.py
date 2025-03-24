from flask_restx import Namespace, Resource, fields
from app.services import facade

# Creamos un namespace específico para las amenidades
api = Namespace('amenities', description='Amenity operations')

# Definimos un modelo de datos para amenidades para la validación y documentación.
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201,'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        POST /api/v1/amenities/
        Registra una nueva amenidad.
        """

        amenity_data = api.payload

        try:
            # Se llama al método create_amenity de la fachada para crear la amenidad.
            new_amenity = facade.create_amenity(amenity_data)

        except ValueError as e:
            # Captura el error de validación y retorna un 400
            return {'error': str(e)}, 400
        
        # Se retorna la info de la amenity creada y el código 201

        return  {'id': new_amenity.id, 'name': new_amenity.name}, 201
    
    @api.response(200, 'List of amenities retrieved successfully')

    def get(self):
        """
        GET /api/v1/amenities/
        Recupera una lista de todas las amenidades.
        """

        # Se recuperan todas las amenidades usando el método get_all_amenities.
        amenities = facade.get_all_amenities()

        # Construimos una lista de diccionarios

        amenity_list =[{'id': amenity.id, 'name': amenity.name} for amenity in amenities]
        return amenity_list, 200

# Definición de la ruta para operaicones sobre una amenity específica.
@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        GET /api/v1/amenities/<amenity_id>
        Recupera los detalles de una amenidad por su ID.
        """

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200
    
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        PUT /api/v1/amenities/<amenity_id>
        Actualiza la información de una amenidad existente.
        """

        amenity_data = api.payload

        # Se llama al método update_amenity de la facade.
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)

        if not updated_amenity:
             return {'error': 'Amenity not found'}, 404
        
        
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200