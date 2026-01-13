import keyring
import platform

class CredentialManager:
    SERVICE_NAME = "PromptForge"

    @staticmethod
    def save_credential(key: str, value: str):
        try:
            keyring.set_password(CredentialManager.SERVICE_NAME, key, value)
            return True
        except Exception as e:
            print(f"Error saving credential: {e}")
            return False

    @staticmethod
    def get_credential(key: str) -> str:
        try:
            val = keyring.get_password(CredentialManager.SERVICE_NAME, key)
            return val if val else ""
        except Exception as e:
            print(f"Error retrieving credential: {e}")
            return ""

    @staticmethod
    def delete_credential(key: str):
        try:
            keyring.delete_password(CredentialManager.SERVICE_NAME, key)
        except Exception:
            pass
