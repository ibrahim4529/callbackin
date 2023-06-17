import paho.mqtt.client as mqtt
import typer
import json
from callbackin.schemas.callback import Callback
from callbackin.utils.config import get_mqtt_config
from rich import print_json
import requests


class CallbackHanler:
    def __init__(self, callback: Callback):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.callback = callback
    
    def on_connect(self, client, userdata, flags, rc):
        typer.echo("Listening for requests")
        self.client.subscribe(topic=self.callback.path)
    

    def on_message(self, client, userdata, msg):
        if msg.topic == self.callback.path:
            request_data = json.loads(msg.payload)
            headers = json.loads(request_data["header"])
            method = request_data["method"]
            typer.echo(f"Received Request with method {method}  for -> {self.callback.local_endpoint}")
            body = {}
            if request_data["body"]:
                typer.echo("Body")
                print_json(request_data["body"])
                body = json.loads(request_data["body"])
            
            typer.echo(f"Fowarding request to -> [{method}] {self.callback.local_endpoint}")
            try:
                match method:
                    case "GET":
                        response = requests.get(self.callback.local_endpoint, headers=headers)
                    case "POST":
                        response = requests.post(self.callback.local_endpoint, data=body, headers=headers)
                    case "PUT":
                        response = requests.put(self.callback.local_endpoint, data=body, headers=headers)
            except Exception as e:
                typer.echo(f"Error when fowarding request to {self.callback.local_endpoint}")
                typer.echo(e)
                return
            typer.echo(f"Response from {self.callback.local_endpoint} -> {response.status_code}")

    def run(self):
        typer.echo(f"Running callback {self.callback.name} -> {self.callback.local_endpoint}")
        mqtt_config = get_mqtt_config()
        self.client.connect(mqtt_config["host"], int(mqtt_config["port"]), 60)
        self.client.loop_forever()


