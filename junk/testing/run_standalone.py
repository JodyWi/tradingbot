import subprocess
import os

# Define paths to directories and Python virtual environment
backend_dir = os.path.expanduser("~/tradingbot/Backend")
frontend_dir = os.path.expanduser("~/tradingbot/Frontend")
venv_python = os.path.expanduser("~/tradingbot/venv/bin/python")

# Function to run a command in the background
def run_command(command, cwd=None):
    process = subprocess.Popen(command, cwd=cwd)
    return process

# Run the backend server
print("Starting backend server...")
backend_process = run_command([venv_python, "main.py"], cwd=backend_dir)

# Run the frontend server
print("Starting frontend server on port 5014...")
frontend_process = run_command([venv_python, "-m", "http.server", "5014"], cwd=frontend_dir)

# Keep the script alive and wait for both processes
try:
    print("Backend and frontend are running. Press CTRL+C to stop.")
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("Shutting down servers...")
    backend_process.terminate()
    frontend_process.terminate()
