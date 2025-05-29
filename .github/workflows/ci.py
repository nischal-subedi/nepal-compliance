#!/usr/bin/env python3
# filepath: ci_server.py

import http.server
import socketserver
import subprocess
import argparse
import logging
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CIRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request by running CI command"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'CI process triggered\n')
        
        # Log the request
        client_address = self.client_address[0]
        logger.info(f"CI request received from {client_address}")
        
        # Run CI command in a separate thread
        thread = threading.Thread(target=self.run_ci_command)
        thread.daemon = True
        thread.start()
        
    def do_POST(self):
        """Handle POST request by running CI command"""
        # POST handlers are often used by webhook services
        self.do_GET()  # Reuse the GET handler logic
    
    def run_ci_command(self):
        """Run the CI command"""
        ci_command = "git pull && npm run start"
        logger.info(f"Running CI command: {ci_command}")
        
        try:
            result = subprocess.run(ci_command, shell=True, check=True, 
                                   capture_output=True, text=True)
            logger.info("CI command completed successfully")
            logger.info(f"Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"CI command failed with exit code {e.returncode}")
            logger.error(f"Error output: {e.stderr}")

def run_server(host='0.0.0.0', port=8000):
    """Run the HTTP server"""
    # Allow server to reuse the address (useful for quick restarts)
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer((host, port), CIRequestHandler) as httpd:
        logger.info(f"CI server listening on {host}:{port}")
        logger.info("Send a GET or POST request to trigger CI")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped by user")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CI webhook server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to listen on (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on (default: 8000)')
    
    args = parser.parse_args()
    run_server(args.host, args.port)