import unittest
import azure.functions as func

from HttpWeatherData import main


class TestFunction(unittest.TestCase):
    def test_HttpWeatherData(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/HttpTrigger',
            params={'name': 'Test'})

        # Call the function.
        resp = main(req)

        # Check the output.
        self.assertEqual(
            resp.get_body(),
            b"Hello, Test. This HTTP triggered function executed successfully.",
        )