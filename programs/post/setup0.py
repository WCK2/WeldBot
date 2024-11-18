import json
import os
import requests
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from socketserver import BaseServer
from urllib.parse import urlparse, parse_qs
from jaka.nos.jakabot import *
from wplc import *



#~ Static settings
class SETTINGS:
    def __new__(cls, *args, **kw):
         if not hasattr(cls, '_instance'):
             orig = super(SETTINGS, cls)
             cls._instance = orig.__new__(cls, *args, **kw)
         return cls._instance
    
    def __init__(self):
        #? network
        self.plc_ip = '192.168.69.181'

        self.jaka_ip = '192.168.69.50'
        self.jaka_server_port = 42000

        self.rpi_ip = '192.168.69.120' if os.name == 'nt' else '192.168.69.53'
        self.rpi_port = 42001
        self.rpi_url = f'http://{self.rpi_ip}:{self.rpi_port}/'


settings = SETTINGS()

robot = jakabot(settings.jaka_ip)

plc = PLC(settings.plc_ip)


def post_req_async(path, data):
    """Send a POST request asynchronously."""
    url = settings.rpi_url + path

    def send_post_request():
        try:
            response = requests.post(url, json=data, timeout=5)
            print(f'POST response: {response.status_code}, {response.text}')
        except requests.Timeout:
            print("The request timed out.")
            return None
        except requests.RequestException as e:
            print(f'Error sending POST request: {e}')

    # Create and start a new thread for the POST request
    threading.Thread(target=send_post_request, daemon=True).start()



#~ MEMORY
class MEMORY:
    def __new__(cls, *args, **kw):
         if not hasattr(cls, '_instance'):
             orig = super(MEMORY, cls)
             cls._instance = orig.__new__(cls, *args, **kw)
         return cls._instance
    
    def __init__(self):
        self.lock = threading.Lock()
        self._status = 'Booting'
        self._log = ''
        self._start = False
        self._program = 0

        self.thread_mem_start = None

    def _get_status(self):
        with self.lock:
            return self._status
    def _set_status(self, s: str):
        print(f'new_status: {s}')
        with self.lock:
            self._status = s
        post_req_async(path='mem', data={'name': 'status', 'value': self._status})
    status = property(_get_status, _set_status)

    def _get_log(self):
        with self.lock:
            return self._log
    def _set_log(self, s: str):
        print(f'log: {s}')
        with self.lock:
            self._log = s
        post_req_async(path='mem', data={'name': 'log', 'value': self._log})
    log = property(_get_log, _set_log)

    def _get_start(self):
        with self.lock:
            return self._start
    def _set_start(self, b: bool):
        if self.thread_mem_start is None or not self.thread_mem_start.is_alive():
            with self.lock:
                self._start = b
                if b:
                    self.thread_mem_start = threading.Thread(target=self._reset_start, daemon=True)
                    self.thread_mem_start.start()
    start = property(_get_start, _set_start)

    def _get_program(self):
        with self.lock:
            return self._program
    def _set_program(self, n: int):
        with self.lock:
            self._program = n
    program = property(_get_program, _set_program)

    def _reset_start(self):
        time.sleep(1.5)
        self._start = False

mem = MEMORY()



#~ Server handler
class JakaHttpHandler(SimpleHTTPRequestHandler):
    def text_response(self, code: int, text: str = ""):
        """Send a plain text response."""
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(text.encode())
        return
        
    def json_response(self, code: int, data: dict = {}):
        """Send a JSON response."""
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
        return

    def do_GET(self):
        """Handle GET requests."""
        url = urlparse(self.path)
        path = url.path
        query_params = parse_qs(url.query)

        try:
            if path == "/hello":
                self.json_response(200, {"state": True})
            elif path == "/mem":
                self.handle_mem_get(query_params)
            elif path == "/robot":
                self.handle_robot_get(query_params)
            else:
                self.text_response(404, "Not Found")
        except Exception as e:
            self.text_response(500, f"Internal Server Error: {str(e)}")

    def do_POST(self):
        """Handle POST requests."""
        url = urlparse(self.path)
        path = url.path
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length).decode("utf-8")

        print(f"POST request: path={path}, body={body}")

        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return self.text_response(400, "Invalid JSON format")

        try:
            if path == "/mem":
                self.handle_mem_set(body_data)
            else:
                self.text_response(404, "Not Found")
        except Exception as e:
            self.json_response(500, {"error": f"Internal Server Error: {str(e)}"})

    #~ GET request handlers
    def handle_mem_get(self, query_params):
        """Handle GET /mem with query parameters."""
        try:
            name = query_params.get("name", [None])[0]

            if not name:
                return self.json_response(400, {"error": "Missing 'name' in query parameters"})

            if name == "status":
                return self.json_response(200, {"status": mem.status})
            else:
                return self.json_response(400, {"error": f"Invalid 'name' value: {name}"})
        except Exception as e:
            self.json_response(500, {"error": f"Internal Server Error: {str(e)}"})

    def handle_robot_get(self, query_params):
        """Handle GET /robot with query parameters."""
        try:
            name = query_params.get("name", [None])[0]

            if not name:
                return self.json_response(400, {"error": "Missing 'name' in query parameters"})

            if name == "frame":
                frame = [round(value, 3) for value in robot.get_frame(isdegs=True)[1]]
                return self.json_response(200, {"frame": frame})
            elif name == "tool":
                tool = [round(value, 3) for value in robot.get_tool(isdegs=True)[1]]
                return self.json_response(200, {"tool": tool})
            elif name == "tcp_pose":
                pose = [round(value, 3) for value in robot.get_tcp_pose()]
                return self.json_response(200, {"pose": pose})
            elif name == "transformation_data":
                frame = [round(value, 3) for value in robot.get_frame(isdegs=True)[1]]
                tool = [round(value, 3) for value in robot.get_tool(isdegs=True)[1]]
                pose = [round(value, 3) for value in robot.get_tcp_pose()]

                data_package = {
                    "frame": frame,
                    "tool": tool,
                    "pose": pose,
                    "camera_tool": settings.camera_tool,
                    "x_boundary_range": settings.x_boundary_range,
                    "y_boundary_range": settings.y_boundary_range,
                    "z_boundary_range": settings.z_boundary_range
                }
                return self.json_response(200, data_package)
            elif name == "is_in_pos":
                is_in_pos = robot.is_in_pos()[1]
                return self.json_response(200, {"is_in_pos": is_in_pos})
            else:
                self.json_response(400, {"error": "Invalid or missing 'name' parameter"})
        except Exception as e:
            self.json_response(500, {"error": f"Internal Server Error: {str(e)}"})

    #~ POST request handlers
    def handle_mem_set(self, body_data):
        """Handle setting memory values via POST request."""
        try:
            name = body_data.get("name")
            value = body_data.get("value")

            if not name or value is None:
                self.json_response(400, {"error": "Missing 'name' or 'value' in request body"})
                return

            if name == "start":
                value = bool(int(value))    
                mem.start = value
                self.json_response(200, {"status": "success"})
            elif name == "program":
                value = int(value)    
                mem.program = value
                self.json_response(200, {"status": "success"})
            else:
                self.json_response(404, {"error": f"Variable '{name}' Not Found"})
        except Exception as e:
            self.json_response(500, {"error": f"Internal Server Error: {str(e)}"})

    # def log_message(self, format, *args):
    #     """Suppress default HTTP logging (optional)."""
    #     return

#~ Server
class JakaHttpServer(HTTPServer):
    def __init__(self, port=settings.jaka_server_port):
        super().__init__(('', port), JakaHttpHandler)

    def run_server(self):
        """ Run the server in a new thread """
        print(f"Server started at port {self.server_port}")
        threading.Thread(target=self.serve_forever, daemon=True).start()

    def stop_server(self):
        """ Stop the server gracefully """
        self.shutdown()  # This will stop serve_forever() loop
        self.server_close()
        print("Server stopped")


server = JakaHttpServer()









if __name__ == '__main__':
    robot.init()
    server.run_server()

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass

    server.stop_server()


