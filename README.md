# CALLBACKIN

## Description
Callbackin is a simple solution to forward requests to a local server from a public URL. It is useful for testing webhooks and other services that require a public URL to send requests to.

## Usage
1. Install the package globall using pip: `pip install callbackin`
2. Run the command `callbackin init` to initialize
3. Run the command `callbackin login` to login using github
3. Create a new callback using the command `callbackin create` and fill in the details
```bash
$ callbackin create
Name of the callback: Callback 2
Local endpoint: http://localhost:8000/handle-error
Description: Simple Local Handle error
Creating callback Callback 2 for http://localhost:8000/handle-error
Using This URL to use your endpoint: https://api.callbackin.my.id/handle/2b4edbf0-3c71-473c-97ad-1c34978ca7f9
```
name: Name of the callback
local endpoint: The local endpoint to forward requests to
description: A description of the callback
Copy the URL and use it as the URL to send requests to
4. Run the command `callbackin list` to list all callbacks
5. Run the command `callbackin run {ID}` to start listening for requests

## Commands
- `callbackin init` - Initialize the callbackin server
- `callbackin login` - Login using github
- `callbackin create` - Create a new callback
- `callbackin list` - List all callbacks
- `callbackin run {ID}` - Start listening for requests on a callback


## How it works
Callbackin uses a public server to forward requests to a local server. It uses a public URL to forward requests to a local server. The public URL is generated using a UUID. When a request is sent to the public URL, the server forwards the request to the local server using mqtt.
The callbackin cli is used for creating callbacks and listening mqtt messages. When a request is received, server sends a mqtt message to the cli. The cli then forwards the request to the local server.
