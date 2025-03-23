import configparser
import os
from cryptography.fernet import Fernet

class PropertyLoader:
    CONFIG_FILE = r"Resources\config.cfg"
    KEY_FILE = r"Resources\secret.key"

    @staticmethod
    def generate_key():
        """Generate an encryption key if not already present."""
        if not os.path.exists(PropertyLoader.KEY_FILE):
            key = Fernet.generate_key()
            with open(PropertyLoader.KEY_FILE, "wb") as key_file:
                key_file.write(key)
            print("Encryption key generated and saved.")

    @staticmethod
    def load_key():
        """Load the encryption key from file."""
        if not os.path.exists(PropertyLoader.KEY_FILE):
            PropertyLoader.generate_key()  # Auto-generate if missing
        with open(PropertyLoader.KEY_FILE, "rb") as key_file:
            return key_file.read()

    @staticmethod
    def is_encrypted():
        """Check if config.cfg is encrypted."""
        try:
            with open(PropertyLoader.CONFIG_FILE, "rb") as file:
                content = file.read()
                return not content.startswith(b"[")  # Normal config starts with '[section]'
        except FileNotFoundError:
            raise FileNotFoundError(f"{PropertyLoader.CONFIG_FILE} not found!")

    @staticmethod
    def encrypt_config():
        """Encrypt the config file if it's not already encrypted."""
        if PropertyLoader.is_encrypted():
            return  # Already encrypted, no need to do it again
        
        key = PropertyLoader.load_key()
        cipher = Fernet(key)

        with open(PropertyLoader.CONFIG_FILE, "rb") as file:
            file_data = file.read()

        encrypted_data = cipher.encrypt(file_data)

        with open(PropertyLoader.CONFIG_FILE, "wb") as file:
            file.write(encrypted_data)

        print("Config file encrypted successfully.")

    @staticmethod
    def decrypt_config():
        """Decrypt the config file for reading."""
        if not PropertyLoader.is_encrypted():
            with open(PropertyLoader.CONFIG_FILE, "r") as file:
                return file.read()  # Already in plaintext

        key = PropertyLoader.load_key()
        cipher = Fernet(key)

        with open(PropertyLoader.CONFIG_FILE, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        return decrypted_data.decode()

    @staticmethod
    def get_prop_file(sectionName, propertyName):
        """Retrieve a property from the decrypted config file."""
        decrypted_content = PropertyLoader.decrypt_config()

        config = configparser.RawConfigParser()
        config.read_string(decrypted_content)  # Read from decrypted content

        return config.get(sectionName, propertyName)

    @staticmethod
    def get_url():
        return PropertyLoader.get_prop_file('url_details', 'url')

    @staticmethod
    def get_user_name():
        return PropertyLoader.get_prop_file('testdata', 'userName')

    @staticmethod
    def get_user_email():
        return PropertyLoader.get_prop_file('testdata', 'email')

# use to decrypt config.cfg file
# if __name__ == "__main__":
#     PropertyLoader.generate_key() 
#     PropertyLoader.decrypt_config()

# Automatically ensure encryption before running tests
if __name__ != "__main__":
    PropertyLoader.generate_key()  # Ensure key exists
    PropertyLoader.encrypt_config()  # Ensure config is encrypted
