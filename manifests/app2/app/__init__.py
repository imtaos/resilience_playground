from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from prometheus_flask_exporter import PrometheusMetrics

print('********', Config.SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    metrics = PrometheusMetrics(app)

    db.init_app(app)

    from .routes.blog import blog_bp
    app.register_blueprint(blog_bp)

    @app.route('/health')
    def health():
        return {"status": "healthy"}

    from .models.blog import Blog
    with app.app_context():
        db.create_all()

    return app
