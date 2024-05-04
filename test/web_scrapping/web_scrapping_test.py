import os 
from app.database.base_test import BaseTest, init_testing
from starlette.testclient import TestClient
from app.routers.web_scraping import app
from app.utils import generate_fake_token

class TestWebScrapping(BaseTest):
    """
    Clase que contiene los tests para web_scrapping.
    """

    @classmethod
    def setUpClass(cls):
        init_testing("web_scrapping")

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
        Configuración inicial para los tests web_scrapping.
        """
        super().setUp()
        os.environ["FUNCTION_NAME"] = "web_scrapping_test"
        os.environ["DB_NAME"] = "web_scrapping_test"  
        token = generate_fake_token()
        self.headers = {"Authorization": token}
        self.client = TestClient(app)

    def test_investment_creation(self):
        data_json = {
            "actor": {
                "cedulaActor": "0968599020001",
                "nombreActor": ""
                },
            "demandado": {
                "cedulaDemandado": "",
                "nombreDemandado": ""
                },
            "numeroCausa": "",
            "materia": "",
            "numeroFiscalia": "",
            "provincia": "",
            "recaptcha": "verdad"
        } 
        response = self.client.post(
            "/web_scraping/",json=data_json,
            headers=self.headers,
        )
        assert response.status_code == 200