# ======================================
# pyreport v1.0.0
#
# Created by Olympia Papaioannou 
# ======================================

import os, psutil, shutil, subprocess, socket, time, platform
from datetime import datetime, timedelta
import messages as msg

def get_detailed_hardware():
    cpu = subprocess.getoutput("lscpu | grep 'Model name' | cut -d ':' -f2").strip()
    gpu = "Integrated Graphics"
    if shutil.which("nvidia-smi"):
        gpu_name = subprocess.getoutput("nvidia-smi --query-gpu=gpu_name --format=csv,noheader")
        gpu_stats = subprocess.getoutput("nvidia-smi --query-gpu=utilization.gpu,temperature.gpu --format=csv,noheader,nounits").replace(',', '% |')
        gpu = f"{gpu_name} ({gpu_stats}°C)"
    return cpu, gpu

def get_hybrid_cpu():
    p_phys = psutil.cpu_count(logical=False)
    logical = psutil.cpu_count(logical=True)
    try:
        e_cores = (p_phys * 2) - logical
        p_cores = p_phys - e_cores
        if p_cores <= 0: return f"{p_phys} Physical / {logical} Logical"
        return f"{p_cores} Performance / {e_cores} Efficient"
    except: return f"{p_phys} Physical"

def get_system_data():
    # Network Speed (0.5s sample)
    n1 = psutil.net_io_counters()
    time.sleep(0.5)
    n2 = psutil.net_io_counters()
    net_up = round((n2.bytes_sent - n1.bytes_sent) / (1024 * 1024) / 0.5, 2)
    net_down = round((n2.bytes_recv - n1.bytes_recv) / (1024 * 1024) / 0.5, 2)
    
    mem = psutil.virtual_memory()
    disk = shutil.disk_usage("/")
    cpu_name, gpu_name = get_detailed_hardware()
    
    # Temp
    temp = "N/A"
    try:
        t = psutil.sensors_temperatures()
        for n in ['coretemp', 'cpu_thermal', 'acpitz']:
            if n in t: temp = f"{int(t[0].current)}°C"; break
    except: pass

    # Screen
    screen = "Headless"
    try:
        for c in os.listdir('/sys/class/drm/'):
            if os.path.exists(f'/sys/class/drm/{c}/modes'):
                with open(f'/sys/class/drm/{c}/modes') as f:
                    screen = f.readline().strip() or screen; break
    except: pass

    # Cron Jobs
    cron = subprocess.getoutput("crontab -l 2>/dev/null")
    cron = cron if (cron and "no crontab" not in cron) else "No scheduled cron jobs."

    # Alerts
    ssh = subprocess.getoutput("who | grep 'pts/' | wc -l").strip()
    alerts = []
    if psutil.cpu_percent() > 90: alerts.append("HIGH CPU")
    if mem.percent > 90: alerts.append("LOW RAM")
    if int(ssh or 0) > 0: alerts.append(f"{ssh} ACTIVE SSH")

    return {
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "host": socket.gethostname(),
        "os_ver": f"{platform.system()} {platform.release()}",
        "ip": socket.gethostbyname(socket.gethostname()),
        "uptime": str(timedelta(seconds=int(datetime.now().timestamp() - psutil.boot_time()))),
        "cpu_name": cpu_name,
        "cpu_pct": psutil.cpu_percent(),
        "cpu_cores": get_hybrid_cpu(),
        "cpu_max_ghz": round(psutil.cpu_freq().current / 1000, 2) if psutil.cpu_freq() else "N/A",
        "cpu_temp": temp,
        "ram_pct": mem.percent,
        "ram_used": round(mem.used / (1024**3), 2),
        "ram_total": round(mem.total / (1024**3), 2),
        "ram_color": "#ef4444" if mem.percent > 90 else "#3b82f6",
        "disk_pct": round((disk.used / disk.total) * 100, 1),
        "disk_used": disk.used // (2**30),
        "disk_total": disk.total // (2**30),
        "disk_color": "#ef4444" if (disk.used/disk.total)*100 > 90 else "#f59e0b",
        "net_up": net_up, "net_down": net_down,
        "gpu": gpu_name,
        "gpu_badge": "bg-green" if "NVIDIA" in gpu_name else "bg-orange",
        "gpu_status": "ACTIVE" if "NVIDIA" in gpu_name else "OFF",
        "alerts": " | ".join(alerts) if alerts else "SYSTEM HEALTHY",
        "cron_jobs": cron,
        "tmp_mb": round(sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk('/tmp') for f in fs if not os.path.islink(os.path.join(d, f))) / 1048576, 2) if os.path.exists('/tmp') else 0,
        "top_procs": subprocess.getoutput("ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -n 6"),
        "logins": subprocess.getoutput("last -n 5"),
        "services": subprocess.getoutput("systemctl list-units --type=service --state=running --no-legend | head -n 5"),
        "screen": screen
    }

def generate():
    d = get_system_data()
    d['header_line'] = msg.get_header(d['host'], d['time'])
    print(msg.CONSOLE_TEMPLATE.format(**d))
    try:
        with open("template.html", "r") as f: t = f.read()
        for k, v in d.items(): t = t.replace(f"{{{{{k}}}}}", str(v))
        with open("system_report.html", "w") as f: f.write(t)
        print(msg.SUCCESS_HTML.format(path=os.path.abspath("system_report.html")))
    except: print(msg.ERROR_TEMPLATE)

if __name__ == "__main__": 
    print("pyreport v1.0.0.0 | Created by Olympia Papaioannou.")    
    print("Creating report.....")
    generate()
