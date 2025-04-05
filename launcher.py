import subprocess
import threading
import webbrowser
import time
from src.backend import app

def start_backend():
    """
    Start the Flask backend.
    """
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def start_frontend():
    """
    Open the React frontend in the default web browser.
    """
    time.sleep(2)  # Wait for the backend to start
    webbrowser.open("http://127.0.0.1:3000")

def start_react_build():
    """
    Serve the React build folder using a lightweight HTTP server.
    """
    subprocess.run(["npx", "serve", "-s", "frontend/build", "-l", "3000"])

if __name__ == "__main__":
    # Start the backend in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Start the React frontend
    start_react_build()
