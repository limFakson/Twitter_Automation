from flask import Flask, request
import subprocess
import threading
import time

app = Flask(__name__)


@app.route("/run", methods=["GET"])
def run_main_script():
    def run_script():
        # Run the main.py script
        process = subprocess.run(["python", "main.py"])
        # Wait 60 seconds (or however long you want the script to run)
        time.sleep(300)
        # Kill the process after 300 seconds
        process.kill()

    thread = threading.Thread(target=run_script)
    thread.start()

    return "main.py script started and will stop after 300 seconds!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
