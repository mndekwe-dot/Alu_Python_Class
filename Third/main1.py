import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64

rides = [
    {"id": 1, "driver": "Jayz", "dest": "market", "status": "active"},
    {"id": 2, "driver": "Beni", "dest": "airport", "status": "ended"}
]

USERNAME=[
    {"username":'Eric','password':'1234567'},
    {"username":'Dieu Merci','password':'1234643'}
]

def check_auth(header):
    if not header or not header startswith("Basic"):
        return False

    encoded = header.split("")[1] # header.replace("Basic","")
    decoded = base64.b64decode(encoded).decode()
    #user,password,role=[Eric,123456,admin]
    user,password = decoded.split(":")

    return user == USERNAME and password== PASSWORD

class MotorTaxiHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        # http://localhost:8080/rides
        if self.path == "/rides":
            auth_header = self.headers.get("Authorization", None)
            if not check_auth(auth_header):
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.send_header("WWW-Authenticate", 'Basic realm="Access to /rides"')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid username or password"}).encode())
                return

            self._set_headers(200)
            self.wfile.write(json.dumps(rides).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Path not found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/rides":
            
            def check_auth(header):
                if not header or not header.startswith("Basic"):  # Added dot
                    return False
    
                try:
                    encoded = header.split(" ")[1]  # Split by space
                    decoded = base64.b64decode(encoded).decode()
                    username, password = decoded.split(":")
                    
                    # Loop through USERS list to find match
                    for user in USERS:
                        if user["username"] == username and user["password"] == password:
                            return True
                    
                    return False
                except:
                    return False
                
            content_type = self.headers.get("Content-Type","Authorization")
            if content_type != "application/json":
                self._set_headers(415)
                self.wfile.write(json.dumps({"error": "Content must be json"}).encode("utf-8"))
                return

            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Content must be json"}).encode("utf-8"))
                return

            try:
                content = self.rfile.read(content_length)
                data = json.loads(content)

                new_ride = {
                    "id": len(rides) + 1,
                    "driver": data.get("driver", "Unknown"),
                    "dest": data.get("dest", "Unknown"),
                    "status": "pending"
                }

                rides.append(new_ride)

                self._set_headers(201)
                self.wfile.write(json.dumps(new_ride).encode("utf-8"))
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Path not found"}).encode("utf-8"))
            
    def do_PUT(self):
        if self.path.startswith("/rides/"):
            try:
                ride_id = int(self.path.split("/")[-1])
                ride = None   # default if nothing is found

                for r in rides:                      # loop through each ride
                    if r["id"] == ride_id:            # check if the id matches
                        ride = r                      # store the matching ride
                        break                         # stop after the first match

                if not ride:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Ride not found"}).encode("utf-8"))
                    return

                content_length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(content_length))

                # Update fields
                ride["driver"] = data.get("driver", ride["driver"])
                ride["dest"] = data.get("dest", ride["dest"])
                ride["status"] = data.get("status", ride["status"])

                self._set_headers(200)
                self.wfile.write(json.dumps(ride).encode("utf-8"))
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid request"}).encode("utf-8"))

    def do_DELETE(self):
        if self.path.startswith("/rides/"):
            try:
                ride_id = int(self.path.split("/")[-1])
                ride = None   # default if nothing is found

                for r in rides:                      # loop through each ride
                    if r["id"] == ride_id:            # check if the id matches
                        ride = r                      # store the matching ride
                        break                         # stop after the first match

                if not ride:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Ride not found"}).encode("utf-8"))
                    return

                rides.remove(ride)
                self._set_headers(200)
                self.wfile.write(json.dumps({"message": f"Ride with id {ride_id} deleted successfully"}).encode("utf-8"))
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid ride ID"}).encode("utf-8"))


def run():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, MotorTaxiHandler)
    print(f"Moto-Taxi, server running on port {server_address[1]}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()