from dotenv import load_dotenv
from google.cloud import secretmanager
import os


def set_gcp_secrets_as_env_vars() -> None:
    """
    Query all secrets accessible to the application from Secret Manager
    and set them as environment variables.
    """

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = secretmanager.SecretManagerServiceClient()

    # Build the parent path for all secrets in the project
    parent = f"projects/{project_id}"

    # List all secrets in the project
    for secret in client.list_secrets(request={"parent": parent}):
        secret_name = secret.name.split("/")[-1]

        # Access the latest version of each secret
        version_path = f"{secret.name}/versions/latest"
        response = client.access_secret_version(request={"name": version_path})

        # Set the secret as an environment variable
        os.environ[secret_name] = response.payload.data.decode("UTF-8")


def setup_environment_variables() -> None:

    if os.getenv("GAE_ENV", "").startswith("standard"):
        # We are running in Google App Engine, set secrets as env vars
        set_gcp_secrets_as_env_vars()
    else:
        load_dotenv()  # take environment variables from .env if they exist
