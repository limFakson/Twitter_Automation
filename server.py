from flask import Flask, request
import subprocess
import threading
import time

app = Flask(__name__)


def run_script():
    while True:
        # Start the process in the background
        process = subprocess.Popen(["python", "main.py"])

        # Let it run for 1 hour (3600 seconds)
        time.sleep(3600)

        # Kill the process
        process.terminate()
        process.wait()  # Ensure the process is properly stopped


@app.route("/run", methods=["GET"])
def run_main_script():
    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()
    return "main.py script started and will restart every hour!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
