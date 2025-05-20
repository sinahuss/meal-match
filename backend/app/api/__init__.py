from .recipes import recipes_bp


def register_blueprints(app):
    app.register_blueprint(recipes_bp)
