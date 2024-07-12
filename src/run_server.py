from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class CustomHandler(SimpleHTTPRequestHandler):
    public_dir = os.path.abspath('public')

    def translate_path(self, path):
        original_path = super().translate_path(path)
        
        # Log original and modified paths for debugging
        print(f"Original path requested: {path}")
        
        # Ensure path is within the public directory
        relative_path = os.path.relpath(original_path, os.getcwd())
        full_path = os.path.join(self.public_dir, relative_path)
        
        # Special handling for /majesty
        if path == "/majesty":
            full_path = os.path.join(full_path, "post1.html")

        print(f"Modified path: {full_path}")
        
        return full_path

    def do_GET(self):
        if self.path == "/majesty":
            self.send_response(301)  # Redirect
            self.send_header('Location', f'{self.path}/post1.html')
            self.end_headers()
        else:
            super().do_GET()

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving from {handler_class.public_dir} on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()