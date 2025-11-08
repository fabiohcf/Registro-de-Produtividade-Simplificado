# app/extensions.py


from flask_cors import CORS

def init_extensions(app):
    # Permite requests do frontend (Vite/Lovable)
    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]}})
