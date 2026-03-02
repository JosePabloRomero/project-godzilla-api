import pytest


def _import_app():
    try:
        from app.main import app

        return app, "app.main", None
    except Exception as e:
        return None, None, e


def test_app_importable():
    app, source, err = _import_app()
    assert app is not None, f"No se pudo importar 'app' desde 'app.main'. Error: {err}"


def test_app_has_routes():
    app, source, err = _import_app()
    if app is None:
        pytest.fail(
            "No se pudo importar 'app'. "
            "Verifica que el módulo principal esté en 'app/main.py'."
        )
    assert hasattr(app, "routes"), (
        f"El objeto 'app' importado desde '{source}' no tiene atributo 'routes'."
        f"Error: {err}"
    )
