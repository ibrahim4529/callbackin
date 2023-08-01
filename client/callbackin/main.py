import typer
from callbackin.handler.callback import CallbackHanler
from callbackin.handler.login import LoginHandler
from pathlib import Path
from callbackin.schemas.callback import Callback
from callbackin.utils.config import create_config, CONFIG_FILE, get_config, is_authenticated
from callbackin.utils.request import post, get, delete, put, get_base_url
from rich.table import Table
from rich.console import Console



APP_NAME = "callbackin"

app = typer.Typer()


@app.command()
def login():
    login_handler = LoginHandler()
    login_handler.run()

@app.command()
def init():
    base_url = typer.prompt("Callbackin server URL", default="https://api.callbackin.my.id")
    mqtt_host =  typer.prompt("MQTT broker URL", default="test.mosquitto.org")
    mqtt_port = typer.prompt("MQTT broker port", default="1883")
    mqtt_user = typer.prompt("MQTT broker username", default="")
    mqtt_pasword = typer.prompt("MQTT broker password", default="", hide_input=True)
    create_config(
        base_url=base_url,
        mqtt_host=mqtt_host,
        mqtt_port=mqtt_port,
        mqtt_user=mqtt_user,
        mqtt_pasword=mqtt_pasword,
    )
    typer.echo("Initialized successfully, please login to continue using callbackin login command")

@app.command("create")
def create_callback():
    name = typer.prompt("Name of the callback")
    local_endpoint = typer.prompt("Local endpoint")
    description = typer.prompt("Description")
    typer.echo(f"Creating callback {name} for {local_endpoint}")

    response = post("/callbacks", data={
        "name": name,
        "local_endpoint": local_endpoint,
        "description": description,
    })
    if response.status_code == 200:
        callback = Callback(**response.json())
        typer.echo(f"Using This URL to use your endpoint: {get_base_url()}/handle/{callback.path}")
        typer.echo(f"Start callback with this command: callbackin run {callback.id}")
    else:
        typer.echo("Error creating callback")

@app.command("list")
def list_callbacks():
    typer.echo("Listing callbacks")
    response = get("/callbacks")
    if response.status_code == 200:
        callbacks = response.json()
        table = Table("ID", "Name", "Local Endpoint", "Server Endpoint")
        for callback in callbacks:
            table.add_row(str(callback["id"]), 
                          callback["name"], 
                          callback["local_endpoint"],
                          f"{get_base_url()}/handle/{callback['path']}"
                          )
        console = Console()
        console.print(table)



@app.command("delete")
def delete_callback(id: int = typer.Argument(..., help="ID of the callback to delete")):
    typer.echo("Deleting callback")
    response = delete(f"/callbacks/{id}")
    if response.status_code == 204:
        typer.echo("Callback deleted successfully")
    else:
        typer.echo("Error deleting callback")
        typer.echo(response.json()["detail"])


@app.command("edit")
def edit_callback(id: int = typer.Argument(..., help="ID of the callback to edit")):
    typer.echo("Editing callback")
    response = get(f"/callbacks/{id}")
    if response.status_code == 200:
        callback: Callback = Callback(**response.json())
        name = typer.prompt("Name of the callback", default=callback.name)
        local_endpoint = typer.prompt("Local endpoint", default=callback.local_endpoint)
        description = typer.prompt("Description", default=callback.description)
        typer.echo(f"Editing callback {name} for {local_endpoint}")

        response = put(f"/callbacks/{id}", data={
            "name": name,
            "local_endpoint": local_endpoint,
            "description": description,
        })
        if response.status_code == 200:
            callback = Callback(**response.json())
            typer.echo(f"Callback edited successfully with ID {callback.id}")
            typer.echo("Callback edited successfully")
        else:
            typer.echo("Error editing callback")
    else:
        typer.echo("Error editing callback")
        typer.echo(response.json()["detail"])

@app.command("run")
def run(id: int = typer.Argument(..., help="ID of the callback to run")):
    response = get(f"/callbacks/{id}")
    if response.status_code == 200:
        callback: Callback = Callback(**response.json())
        callback_handler = CallbackHanler(callback)
        try:
            callback_handler.run()
        except KeyboardInterrupt:
            callback_handler.client.disconnect()
            typer.echo("Exiting...")
            exit(0)
    else:
        typer.echo("Error running callback")
        typer.echo(response.json()["detail"])

@app.callback()
def main():
    if not Path(CONFIG_FILE).exists():
        typer.echo("Please run `callbackin init` first")
    else:
        if not is_authenticated():
            typer.echo("Please run `callbackin login` first")
    


