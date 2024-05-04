import os 
from app.database.base_test import BaseTest, init_testing
from starlette.testclient import TestClient
from app.routers.auth import app 
from app.database.session import RoutingSession as Database
from app.database.models import models
from app.utils import Hasher as Hash

class TestAuth(BaseTest):
    """
    Clase que contiene los tests para Auth.
    """

    @classmethod
    def setUpClass(cls):
        init_testing("auth")

    class mock_requests_retry_session:
        class mocked_response:
            def __init__(self, *args, **kwargs):
                self.status_code = 409

            def json(self, *args, **kwargs):
                return "Some error"

        def post(self, *args, **kwargs):
            return self.mocked_response()

    class mock_requests_retry_session_exception:
        class mocked_response:
            """
            Clase que simula la respuesta de una petición HTTP.
            """

            def __init__(self, *args, **kwargs):
                self.status_code = 200

            def json(self, *args, **kwargs):
                raise Exception("Some error")

        def post(self, *args, **kwargs):
            return self.mocked_response()

    def setUp(self):
        """
        Configuración inicial para los tests auth.
        """
        super().setUp()
        os.environ["FUNCTION_NAME"] = "auth_test"
        os.environ["DB_NAME"] = "auth_test"    
        self.client = TestClient(app) 
        with Database() as db:
            db.query(models.User).filter(models.User.email == "test_user").delete()
            db.commit()

            hashed_password = Hash.get_password_hash("TestPassword123")
            user = models.User( 
                email="test_user@example.com",
                password=hashed_password, 
            )
            db.add(user)
            db.commit()

    def test_login(self):
        data_json = {
            "signin_username": "test_user@example.com",
            "signin_value": "TestPassword123"
        }
        response = self.client.post(
            "/auth/signin",json=data_json, 
        )
        assert response.status_code == 200