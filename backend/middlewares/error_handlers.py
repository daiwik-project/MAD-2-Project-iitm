from flask import jsonify

def register_error_handlers(app):
    """
    Register error handlers for the Flask app.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized", "message": str(error)}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden", "message": str(error)}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404
    
    
    @app.errorhandler(409)
    def conflict(error):
        return jsonify({"error": "Conflict", "message": str(error)}), 409
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        return jsonify({"error": "Content Not Provided", "message": str(error)}), 415


    # @app.errorhandler()


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500