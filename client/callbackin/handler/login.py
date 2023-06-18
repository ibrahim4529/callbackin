from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import webbrowser
import typer
from callbackin.utils.config import is_authenticated, get_config, CONFIG_FILE
from callbackin.utils.request import get_base_url

class CallbackHandler(BaseHTTPRequestHandler):
    token = None

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        pass

    def do_GET(self):
        if self.path.startswith('/auth/github/callback'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Extract the token from the URL query parameters
            query_params = self.path.split('?')[1]
            token = query_params.split('=')[1]

            # Store the token in the class variable
            CallbackHandler.token = token

            self.wfile.write(b'Login successfully, you can close this tab now')
            return
    
    @staticmethod
    def get_token():
        return CallbackHandler.token

class LoginHandler:
    def __init__(self) -> None:
        self.server = HTTPServer(('localhost', 2929), CallbackHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def run(self):
        config = get_config()
        if not is_authenticated():
            self.server_thread.start()
            typer.echo("Login to GitHub")
            webbrowser.open(f'{get_base_url()}/auth/github/login/cli')
            while CallbackHandler.get_token() is None:
                pass
            typer.echo("Login successful")
            self.server.shutdown()
            self.server.server_close()
            config["DEFAULT"]["user_token"] = CallbackHandler.get_token()
            config["DEFAULT"]["is_authenticated"] = "True"
            with open(CONFIG_FILE, "w") as f:
                config.write(f)
        # stop thread
        