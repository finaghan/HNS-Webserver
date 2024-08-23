Welcome to the most basic and modular web server made in python.

=========================================
SHN Webserver V0.2.1
Added the addons!
and I added some documentation to this
read me!
=========================================

how to add your addons!
I have made 2 for you guys please go ahead and make your own
and you can share them to the community!

I use a debian 12 server so I will be using what I normally use
if you are using any other system please use the commands that
your os uses or if you are using a desktop add the folders there.

mkdir /etc/webserver/addons
cd /etc/webserver/addons

Now lets get into the addons I have made!

Discord webhook this tells you that a user is viewing your site and what directory/file they are viewing!

nano /etc/webserver/addons/discord_webhook.py

The contents of that file should match below

import requests

DISCORD_WEBHOOK_URL = "Your webhook goes here"

def send_discord_notification(requested_path):
    message = f"Someone has viewed your site! They are viewing the directory: `{requested_path}`"
    data = {
        "content": message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print("Failed to send data to Discord webhook")
    except Exception as e:
        print(f"Error: {e}")


PHP Addon! Make sure you have php installed!

nano /etc/webserver/addons/php.py

import subprocess

def handle_php_request(script_path):
    try:
        # Run the PHP script using subprocess
        result = subprocess.run(
            ['php', script_path], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            # Return the output of the PHP script
            return result.stdout
        else:
            # Handle errors by returning the stderr output
            return f"PHP Error: {result.stderr}"
    except Exception as e:
        return f"Error executing PHP script: {str(e)}"

cd
cd /etc/webserver
nano /etc/webserver/main.py

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Capture the requested path
        requested_path = self.path
        
        requested_file = requested_path.strip("/")  
        if requested_file == "":
            requested_file = DEFAULT_INDEX  
        
        # Full path to the file
        full_path = os.path.join(DIRECTORY, requested_file)
        
        # Check if the file is a PHP script
        if full_path.endswith(".php"):
            if os.path.isfile(full_path):
                output = handle_php_request(full_path)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(output.encode())
            else:
                self.send_error(404, "File not found")
            return
        
        # If not a PHP file, serve as a normal HTML file
        self.path = f"/{requested_file}"
        super().do_GET()

thats it! have fun!
