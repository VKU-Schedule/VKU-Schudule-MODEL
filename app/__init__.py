from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    CORS(app)  # Cho phép cross-origin requests

    # Cấu hình Swagger UI
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api-docs"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Model Server API",
            "description": "API documentation for Model Server - Convert prompt và tạo lịch học",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"]
    }

    swagger = Swagger(app, config=swagger_config, template=swagger_template)

    # Import routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
