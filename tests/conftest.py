import pytest
from app import create_app
from app import store as _store


@pytest.fixture(autouse=True)
def clean_store():
    _store.clear()
    yield
    _store.clear()


@pytest.fixture
def app():
    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()
