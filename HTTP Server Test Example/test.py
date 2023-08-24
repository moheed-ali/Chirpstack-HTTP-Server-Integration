import http.server
import socketserver

# Define the handler for the HTTP server
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print("Received POST data:")
        print(post_data)
        
        self.send_response(200)
        self.end_headers()

# Create an HTTP server with the defined handler
PORT = 8081  # Choose a suitable port number
httpd = socketserver.TCPServer(("", PORT), RequestHandler)

print(f"Listening on port {PORT}")
httpd.serve_forever()
