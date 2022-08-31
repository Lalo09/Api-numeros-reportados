template = {
    "swagger": "2.0",
    "info": {
        "title": "Number Reports API",
        "description": "API for search number reported by citizens",
        "contact": {
            "responsibleOrganization": "SSP",
            "responsibleDeveloper": "Eduardo Espinoza",
            "email": "mail@gmail.com",
            "url": "",
        },
        "termsOfService": "",
        "version": "1.1"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}