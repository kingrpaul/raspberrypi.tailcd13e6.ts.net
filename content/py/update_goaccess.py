#!/usr/bin/env python3
import subprocess
import glob
import gzip
from datetime import datetime
import os

LOG_FILE = "/tmp/goaccess_python.log"

def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()}: {msg}\n")
    except Exception:
        pass
    print(msg)

def is_valid_gz(filepath):
    try:
        with gzip.open(filepath, "rb") as f:
            f.read(1)
        return True
    except:
        return False


log("=== Starting GoAccess update ===")

# logs = sorted(glob.glob("/var/log/nginx/access.log*"))
logs = sorted(
    glob.glob("/var/log/nginx/access.log*"),
    key=lambda x: os.path.getmtime(x)
)

plain_logs = []
gz_logs = []

for f in logs:
    if f.endswith(".gz"):
        if is_valid_gz(f):
            gz_logs.append(f)
        else:
            log(f"Skipping corrupted gz: {f}")
    else:
        plain_logs.append(f)

log(f"Plain logs: {plain_logs}")
log(f"GZ logs: {gz_logs}")

# Build decompression command
decompress_cmd = []

if gz_logs:
    decompress_cmd.append(f"/bin/zcat {' '.join(gz_logs)}")

if plain_logs:
    decompress_cmd.append(f"/bin/cat {' '.join(plain_logs)}")

# pipeline = " ; ".join(decompress_cmd)

# goaccess_cmd = f"""( {pipeline} ) | /usr/local/bin/goaccess - \    
# --log-format=COMBINED \
# --no-global-config \
# --with-output-resolver \
# --geoip-database=/usr/share/GeoIP/GeoLite2-City.mmdb \
# --invalid-requests=/tmp/goaccess_invalid.log \
# -o /var/www/html/stats.html
# """

all_logs = gz_logs + plain_logs

pipeline = f"/bin/zcat {' '.join(gz_logs)}; /bin/cat {' '.join(plain_logs)}"

goaccess_cmd = (
    f"( {pipeline} ) | "
    "/usr/local/bin/goaccess - "
    "--log-format=COMBINED "
    "--no-global-config "
    "--with-output-resolver "
    "--geoip-database=/usr/share/GeoIP/GeoLite2-City.mmdb "
    "--invalid-requests=/tmp/goaccess_invalid.log "
    "-o /var/www/html/stats.html"
)

log(f"Running pipeline: {goaccess_cmd}")

result = subprocess.run(
    goaccess_cmd,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if result.returncode != 0:
    log(result.stderr.decode("utf-8", errors="replace"))
else:
    log("GoAccess completed successfully.")
