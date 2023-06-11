from pydantic import BaseSettings

class Config(BaseSettings):
    # General
    GITHUB_ID: str
    GITHUB_SECRET: str
    GITHUB_CALLBACK: str
    GITHUB_SCOPE: str = "user:email|read:user"
    CLI_REDIRECT_URL: str = "http://localhost:2929/auth/github/callback"
    DASHBOARD_REDIRECT_URL: str = "http://localhost:3000/auth/github/callback"

    # Database
    DB_URL: str

    # Server
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9999
    OAUTHLIB_INSECURE_TRANSPORT: str = "1"
    SECRET_KEY: str = "secret"
    

    # Mqtt
    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_USERNAME: str
    MQTT_PASSWORD: str


    class Config:
        env_file = ".env"


def get_config():
    return Config()