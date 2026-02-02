import http.server
import socketserver
import json
import subprocess
import os
import tempfile

PORT = 8000
SCANNER_PATH = os.environ.get("RGB_SCANNER_PATH", "../rgb-tools/target/debug/rgb-scanner")

class RGBRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Create temp file with the content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rgba', delete=False) as f:
                f.write(post_data)
                temp_path = f.name
            
            try:
                # Run rgb-scanner --analyze
                # Note: We need to traverse up to find the binary if run from 'explorer' dir
                result = subprocess.run(
                    [SCANNER_PATH, temp_path, "--analyze"], 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    # Parse stdout JSON
                    response_data = result.stdout
                else:
                    response_data = json.dumps({
                        "valid": False,
                        "error": f"Scanner failed: {result.stderr}"
                    })
            except Exception as e:
                response_data = json.dumps({
                    "valid": False,
                    "error": str(e)
                })
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_data.encode())
        else:
            self.send_error(404)

if __name__ == "__main__":
    # Ensure scanner exists
    if not os.path.exists(SCANNER_PATH):
        print(f"WARNING: Scanner binary not found at {SCANNER_PATH}")
        print("Please run `cargo build --bin rgb-scanner` in rgb-tools/ first.")
    
    with socketserver.TCPServer(("", PORT), RGBRequestHandler) as httpd:
        print(f"Serving RGB Explorer at http://localhost:{PORT}")
        print(f"API Endpoint: POST http://localhost:{PORT}/api/analyze")
        httpd.serve_forever()
