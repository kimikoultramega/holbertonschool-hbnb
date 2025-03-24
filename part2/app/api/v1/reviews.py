from flask_restx import Namespace, Resource, fields
from app.services import facade

# Creamos un namespace para las operaciones relacionadas con reviews.
api = Namespace('reviews', description='Review operations')

# Definimos el modelo de datos
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        POST /api/v1/reviews/
        Registra una nueva review.
        Se valida que user_id y place_id existan y que la calificación esté en el rango correcto.
        """
        review_data = api.payload  # Extraemos los datos enviados en la solicitud
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        # Se retorna la review creada con un código 201
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user.id,
            'place_id': new_review.place.id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        GET /api/v1/reviews/
        Recupera una lista de todas las reviews.
        """
        reviews = facade.get_all_reviews()
        review_list = []
        for review in reviews:
            review_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            })
        return review_list, 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        GET /api/v1/reviews/<review_id>
        Recupera los detalles de una review por su ID.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        PUT /api/v1/reviews/<review_id>
        Actualiza la información de una review existente.
        """
        review_data = api.payload
        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Review not found or invalid input'}, 404
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user.id,
            'place_id': updated_review.place.id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        DELETE /api/v1/reviews/<review_id>
        Elimina una review.
        """
        result = facade.delete_review(review_id)
        if not result:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        GET /api/v1/places/<place_id>/reviews
        Recupera todas las reviews asociadas a un place específico.
        """
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        review_list = []
        for review in reviews:
            review_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            })
        return review_list, 200