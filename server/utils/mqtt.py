from fastapi_mqtt import FastMQTT, MQTTConfig
from utils.config import get_config


config = get_config()
mqtt_config = MQTTConfig(
    host=config.MQTT_HOST,
    port=config.MQTT_PORT,
    username=config.MQTT_USERNAME,
    password=config.MQTT_PASSWORD,
    reconnect_retries=10
)

mqtt = FastMQTT(
    config=mqtt_config
)


def init_app(app):
    mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    print("Connected to MQTT broker")


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print(f"Received message '{payload.decode()}' on topic '{topic}'")


def publish_message(topic: str, payload: str):
    mqtt.client.publish(topic, payload)


def subscribe(topic: str):
    mqtt.client.subscribe(topic)