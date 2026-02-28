import pytest


def _import_app():
    try:
        from app.main import app
        return app, "app.main"
    except ImportError:
        pass

    return None, None


def test_app_importable():
    app, source = _import_app()
    assert app is not None, (
        "No se pudo importar 'app' desde 'app.main'. "
        "Asegúrate de que el archivo 'app/main.py' existe y define la variable 'app'."
    )


def test_app_has_routes():
    app, source = _import_app()
    if app is None:
        pytest.fail(
            "No se pudo importar 'app'. "
            "Verifica que el módulo principal esté en 'app/main.py'."
        )
    assert hasattr(app, "routes"), (
        f"El objeto 'app' importado desde '{source}' no tiene atributo 'routes'."
    )
