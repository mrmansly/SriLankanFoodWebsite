import time
import hvac
import os

# Associated with the secret-id-role in Vault (Will require manual environment variable update when token expires)
VAULT_PRIVILEGED_TOKEN = os.getenv('VAULT_PRIVILEGED_TOKEN')

# Maps to sld-role
VAULT_ROLE_NAME = "sld-role"


class VaultClient:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VaultClient, cls).__new__(cls)
            return cls._instance
        return cls._instance

    def __init__(self):
        self.client = hvac.Client()
        self.secret_id = None
        self.secret_id_created_at = None
        self.secret_id_ttl = 24 * 60 * 60  # 24 hours in seconds

    def _generate_secret_id(self):
        self.client.token = VAULT_PRIVILEGED_TOKEN
        response = self.client.auth.approle.generate_secret_id(role_name=VAULT_ROLE_NAME)
        self.client.token = None
        self.secret_id = response['data']['secret_id']
        self.secret_id_created_at = time.time()

    def _is_secret_id_expired(self):
        """Check if the secret ID has expired."""
        if self.secret_id_created_at is None:
            return True
        return (time.time() - self.secret_id_created_at) >= self.secret_id_ttl

    def authenticate(self):
        """Authenticate using AppRole and retrieve a token."""
        if self._is_secret_id_expired():
            self._generate_secret_id()

        try:
            role_id = self._get_role_id()
            response = self.client.auth.approle.login(role_id, self.secret_id)
            self.client.token = response['auth']['client_token']
            return self.client.token
        except Exception as e:
            print(f"Failed to authenticate with Vault: {e}")
            raise e

    def _get_role_id(self):
        self.client.token = VAULT_PRIVILEGED_TOKEN
        response = self.client.auth.approle.read_role_id(role_name=VAULT_ROLE_NAME)
        self.client.token = None
        return response['data']['role_id']

    def get_token(self):
        """Return the current token."""
        return self.client.token

    # Currently using a vault server on the EC2 instance
    def get_vault_secret(self, secret_path):
        # Ensure you authenticate with Vault (you may need to adjust this based on your authentication method)
        # self.client.token = os.getenv('VAULT_TOKEN')  # or use another method like AppRole

        # Fetch the secret
        secret_response = self.client.secrets.kv.v1.read_secret(path=secret_path)
        return secret_response['data']
