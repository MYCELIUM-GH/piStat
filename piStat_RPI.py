# =================================================
# Script for sending internal readings to ESP32 for
# further fan control and displaying on SSD1306.
# =================================================
# @author MYCELIUM
# =================================================
import time
import subprocess
import psutil
from flask import Flask, jsonify
from flask_cors import CORS
# =================================================
# ==== ==== ==== ==== MAIN CONF ==== ==== ==== ====
# =================================================
app = Flask(__name__)
CORS(app)
# =================================================
# ==== ==== ==== ====  GLOBALS  ==== ==== ==== ====
# =================================================
prev_bytes_sent = 0
prev_bytes_recv = 0
last_net_time = time.time()
# =================================================
# ==== ==== ==== ==== STATS FUN ==== ==== ==== ====
# =================================================
def get_stats():
	global prev_bytes_sent, prev_bytes_recv, last_net_time
    # ==== ==== MEMORY ==== ====
	nvme = psutil.disk_usage('/')
	nvme_total = nvme.total / (1024 * 1024 * 1024)
	nvme_used = nvme.used / (1024 * 1024 * 1024)
	hdd = psutil.disk_usage('/mnt/cloud')
	hdd_total = hdd.total / (1024 * 1024 * 1024)
	hdd_used = hdd.used / (1024 * 1024 * 1024)
	# ==== ====  RAM   ==== ====
	ram = psutil.virtual_memory()
	ram_total = round(ram.total / (1024 * 1024 * 1024 * 1024), 2)
	ram_used = round(ram.used / (1024 * 1024 * 1024 * 1024), 2)
	ram_percent = ram.percent
	# ==== ====  CPU   ==== ====
	cpu_percent = psutil.cpu_percent(interval=None)
	try:
		temp_out = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8')
		cpu_temp = float(temp_out.split('=')[1].split('\'')[0])
	except:
		cpu_temp = 0.0
	# ==== ====  NET   ==== ====
	net_io = psutil.net_io_counters()
	curr_t = time.time()
	diff = curr_t - last_net_time
	up = (net_io.bytes_sent - prev_bytes_sent) / diff / 1024
	down = (net_io.bytes_recv - prev_bytes_recv) / diff / 1024

	prev_bytes_sent, prev_bytes_recv, last_net_time = net_io.bytes_sent, net_io.bytes_recv, curr_t

	return {
 		"cpu_temp": round(cpu_temp, 1),
		"cpu_percent": cpu_percent,
		"ram_total_gb": round(ram.total / (1024 * 1024 *1024), 2),
		"ram_used_gb": round(ram.used / (1024 * 1024 * 1024), 2),
		"ram_percent": round(ram.percent, 1),
		"lan_download": round(down, 1),
		"lan_upload": round(up, 1),
		"nvme_total": round(nvme_total, 1),
		"nvme_used": round(nvme_used, 1),
		"hdd_total": round(hdd_total, 1),
		"hdd_used": round(hdd_used, 1)
	}

@app.route('/api/stats')
def api_stats():
	return jsonify(get_stats())

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)
