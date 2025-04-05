from http.server import SimpleHTTPRequestHandler, HTTPServer
from models import categorizer, finances
import json
import urllib.parse

class RequestHandler(SimpleHTTPRequestHandler):
    
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
        elif self.path.startswith("/predict/categorizer"):
            # Читаем данные из тела запроса
            content_length = int(self.headers['Content-Length'])  # Получаем длину тела запроса
            post_data = self.rfile.read(content_length)  # Читаем данные из тела запроса

            # Преобразуем данные в формат JSON (предполагаем, что данные передаются в формате JSON)
            try:
                data = json.loads(post_data)
                word = data.get("word", "default")  # Извлекаем значение параметра "word" или "default"
                print(f"Extracted word: {word}")  # Выводим слово в консоль

                # Обрабатываем предсказание с этим словом
                self.handle_predict(categorizer, word)

            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON data")
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
