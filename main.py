import http.server
import socketserver
import os
import threading

# Configuration
HTTP_PORTS = [80, 8080, 8008]
HTTPS_PORTS = [443, 4433, 8443]
DIRECTORY = "public_html"


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        requested_path = self.path
        

        requested_file = self.path.strip("/") 
        if requested_file == "":
            requested_file = "index.html"  
        
        self.path = f"/{requested_file}"
        super().do_GET()


def start_server_on_port(port, handler_class):
    server = socketserver.TCPServer(("", port), handler_class)
    print(f"Serving on port {port}...")
    server.serve_forever()


def start_all_servers():
    os.chdir(DIRECTORY)
    handler = CustomHTTPRequestHandler
    

    for port in HTTP_PORTS:
        thread = threading.Thread(target=start_server_on_port, args=(port, handler))
        thread.start()
    

    for port in HTTPS_PORTS:

        thread = threading.Thread(target=start_server_on_port, args=(port, handler))
        thread.start()

if __name__ == "__main__":
    start_all_servers()

# Confused? Please read the readme.md file.