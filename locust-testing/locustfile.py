from faker import Faker
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from locust import HttpUser, between, task, events, constant

fake = Faker()


@events.init_command_line_parser.add_listener
def _(parser):
    """Allows to provide an argument via UI or command-line"""

    parser.add_argument(
        "--client-id",
        type=str,
        default="",
        help="IAP OAuth 2.0 Client ID - Leave blank for local testing",
    )


def get_iap_authorization_header(IAP_CLIENT_ID):
    return id_token.fetch_id_token(Request(), IAP_CLIENT_ID)


class BaseUser(HttpUser):
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        IAP_CLIENT_ID = self.environment.parsed_options.client_id
        if IAP_CLIENT_ID:
            self.iap_authorization_token = get_iap_authorization_header(IAP_CLIENT_ID)
            self.client.headers[
                "Authorization"
            ] = f"Bearer {self.iap_authorization_token}"


class MainUser(BaseUser):
    wait_time = between(1, 5)

    @task(10)
    def api_get(self):
        self.client.get("/")

    @task(1)
    def api_post(self):
        self.client.post(
            "/",
            json={"message": fake.sentence(nb_words=6)},
        )


class SecondaryUser(BaseUser):
    wait_time = constant(1)

    @task(5)
    def api_get(self):
        with self.client.get("/deadpeople",  catch_response=True) as response:
            if "Jacques Chirac" not in response.text:
                response.failure(f"Jacques Chirac not found: {response.text}")

    @task(1)
    def api_post(self):
        self.client.post(
            "/",
            json={"message": fake.sentence(nb_words=6)},
        )
