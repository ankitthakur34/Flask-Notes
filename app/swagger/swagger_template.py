swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Notes API",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using Bearer <token>"
        }
    }
}