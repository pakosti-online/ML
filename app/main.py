from http.server import SimpleHTTPRequestHandler, HTTPServer
from models import categorizer, finances
import json
import urllib.parse

class RequestHandler(SimpleHTTPRequestHandler):
            
    def do_POST(self):
        # /predict/recomendate
        if self.path.startswith("/predict/recomendate"):
            self.handle_recomendate()
            
        elif self.path.startswith("/predict/categorizer"):
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                word = data.get("word", "default") 
                print(f"Extracted word: {word}") 
                self.handle_predict(categorizer, word)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON data")
                
        elif self.path.startswith("/predict/forecast"):
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length)
            try:
                text = json.loads(post_data)
                data = text.get("data")
                n = text.get("days")
                print(n)
                if isinstance(n, int) and n > 0:
                    self.handle_forecast(data, n)
                else:
                    self.send_error(400, "'days' should be a positive integer")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON data")
        else:
            self.send_error(404, "Not Found")
            
    def handle_predict(self, model, word):
        try:
            result = model.predict(product_name=word)
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def handle_recomendate(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length)
            text = json.loads(data)
            result = finances.recomendate(text)
            if isinstance(result, list):
                result = json.dumps(result, ensure_ascii=False, indent=4)
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))
            
    def handle_forecast(self, data, n):
        try:
            result = finances.predict_balance_on_days(data, n)

            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            
            self.wfile.write(str(result).encode('utf-8'))
        
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))


def run_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, RequestHandler)

    print("Starting HTTP server on port 3000...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
