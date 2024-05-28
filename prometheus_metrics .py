import random
import time
import psutil
from flask import Flask
from prometheus_client import (
    Counter,
    generate_latest,
    Histogram,
    REGISTRY,
)



PYTHON_CPU_USAGE_GAUGE = Gauge("python_cpu_usage_percent", "CPU usage percent")
PYTHON_MEMORY_USAGE_GAUGE = Gauge("python_memory_usage_bytes", "Memory usage in bytes")

@app.route("/metrics", methods=["GET"])
def stats():
    return generate_latest(REGISTRY), 200

def monitor_system_metrics():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().used
        PYTHON_CPU_USAGE_GAUGE.set(cpu_percent)
        PYTHON_MEMORY_USAGE_GAUGE.set(memory_usage)
        time.sleep(5)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)