import configparser
from pathlib import Path
import typer

CONFIG_DIR = Path(typer.get_app_dir("callbackin"))
CONFIG_FILE = CONFIG_DIR / "config.ini"


def get_config() -> configparser.ConfigParser:
    if not CONFIG_FILE.exists():
        create_config(
            typer.prompt("Base URL"),
            typer.prompt("MQTT Host"),
            typer.prompt("MQTT Port"),
            typer.prompt("MQTT Username"),
            typer.prompt("MQTT Password", hide_input=True),
        )
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def create_config(
    base_url: str,
    mqtt_host: str,
    mqtt_port: str,
    mqtt_user: str,
    mqtt_pasword: str,
) -> None:
    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "user_token": "",
        "is_authenticated": "False",
        "base_url": base_url,
        "mqtt_host": mqtt_host,
        "mqtt_port": mqtt_port,
        "mqtt_user": mqtt_user,
        "mqtt_pasword": mqtt_pasword,
    }
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)


def get_token() -> str:
    config = get_config()
    return config["DEFAULT"]["user_token"]

def get_mqtt_config() -> dict:
    config = get_config()
    return {
        "host": config["DEFAULT"]["mqtt_host"],
        "port": config["DEFAULT"]["mqtt_port"],
        "user": config["DEFAULT"]["mqtt_user"],
        "password": config["DEFAULT"]["mqtt_pasword"],
    }

def is_authenticated() -> bool:
    config = get_config()
    return config["DEFAULT"]["is_authenticated"] == "True"
