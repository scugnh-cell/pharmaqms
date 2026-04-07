import datetime
import typing as t
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask.json.provider import DefaultJSONProvider, _default

db = SQLAlchemy()
migrate = Migrate()


class PharmaJSONProvider(DefaultJSONProvider):
    @staticmethod
    def _mydefault(o: t.Any) -> t.Any:
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, set):
            return list(o)
        return _default(o)

    default: t.Callable[[t.Any], t.Any] = staticmethod(_mydefault)


def create_app():
    from config import Config

    app = Flask(
        __name__,
        static_folder=Config.static_folder,
        template_folder=Config.template_folder,
    )
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)
    app.json = PharmaJSONProvider(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.change_management.view import bp as change_bp
    app.register_blueprint(change_bp)

    # Catch-all: serve frontend SPA for non-API routes
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        from flask import send_from_directory, send_file
        import os

        # If the path matches a static file, serve it
        full_path = os.path.join(Config.template_folder, path)
        if path and os.path.isfile(full_path):
            return send_from_directory(Config.template_folder, path)
        # Otherwise serve index.html (SPA routing)
        index_file = os.path.join(Config.template_folder, "index.html")
        if os.path.isfile(index_file):
            return send_file(index_file)
        return "Frontend not built. Run: cd frontend && pnpm run build", 404

    # Create tables on first run
    with app.app_context():
        from app.change_management.model import ChangeRequest, ActionItem
        db.create_all()

    from app.utils import logger
    logger.init_logger()

    return app
