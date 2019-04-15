import os

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)

# the values of those depend on your setup
POSTGRES_URL = get_env_variable("DATABASE_URI")
POSTGRES_USER = get_env_variable("DATABASE_USER")
POSTGRES_PW = get_env_variable("DATABASE_PASSWD")
POSTGRES_DB = get_env_variable("DATABASE_DB_NAME")
