import pytest
import sys
sys.path.append('/Users/daltyboy11/School/3b/se390/internal_mini_project/')

from flaskr import create_app


@pytest.fixture
def app():
    app = create_app( { 'TESTING' : True } )
    yield app

@pytest.fixture
def client( app ):
    return app.test_client()

