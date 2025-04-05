from http.server import SimpleHTTPRequestHandler, HTTPServer
from models import categorizer, finances
import json
import urllib.parse

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # /predict/categorizer/advanced)
        if self.path.startswith("/predict/categorizer"):
            word = self.path.split("/")[-1]
            self.handle_predict(categorizer, word)
        else:
            # /predict/categorizer?word=advanced)
            parsed_url = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed_url.query)
            word = params.get("word", ["default"])[0]

            if self.path.startswith("/predict/categorizer"):
                self.handle_predict(categorizer, word)
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
            
    def do_POST(self):
        # /predict/recomendate
        if self.path.startswith("/predict/recomendate"):
            self.handle_recomendate()
        else:
            self.send_error(404, "Not Found")

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

def run_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, RequestHandler)

    print("Starting HTTP server on port 3000...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
