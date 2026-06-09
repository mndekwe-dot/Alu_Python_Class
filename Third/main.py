def do_POST(self):
        """POST /rides - Create new ride (with authentication)"""
        if self.path == "/rides":
            
            # ===== STEP 1: CHECK AUTHENTICATION (NEW!) =====
            auth_header = self.headers.get("Authorization", None)
            if not check_auth(auth_header):
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.send_header("WWW-Authenticate", 'Basic realm="Access to /rides"')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid username or password"}).encode())
                return
            
            # ===== STEP 2: CHECK CONTENT TYPE =====
            content_type = self.headers.get("Content-Type", "")
            if content_type != "application/json":
                self._set_headers(415)
                self.wfile.write(json.dumps({"error": "Content must be json"}).encode("utf-8"))
                return

            # ===== STEP 3: CHECK CONTENT LENGTH =====
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Content must be json"}).encode("utf-8"))
                return

            # ===== STEP 4: READ AND PARSE REQUEST BODY =====
            try:
                content = self.rfile.read(content_length)
                data = json.loads(content)

                # ===== STEP 5: CREATE NEW RIDE =====
                new_ride = {
                    "id": len(rides) + 1,
                    "driver": data.get("driver", "Unknown"),
                    "dest": data.get("dest", "Unknown"),
                    "status": "pending"
                }

                rides.append(new_ride)

                # ===== STEP 6: SEND SUCCESS RESPONSE =====
                self._set_headers(201)
                self.wfile.write(json.dumps(new_ride).encode("utf-8"))
                
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode("utf-8"))
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Path not found"}).encode("utf-8"))
    
    # Suppress logging
    def log_message(self, format, *args):
        pass