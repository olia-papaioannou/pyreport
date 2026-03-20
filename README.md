# 🚀 Ubuntu System Monitor Automator

A lightweight, professional-grade system monitoring tool for Linux. This tool generates an interactive **Full-Width HTML Dashboard** and a real-time **Console Report**.

![text message](/images/pyreport_1.jpg)
![text message](/images/pyreport_2.jpg)


## ✨ Features

-   **Hybrid CPU Detection:** Reports Performance (P) vs Efficient (E) cores and current GHz.
-   **Hardware Identity:** Automatically detects CPU model (e.g., i7-12700H) and NVIDIA GPU (e.g., RTX 3060).
-   **Live Metrics:** Network I/O (MB/s), RAM/Disk usage with CSS-only gauges (no JS bloat).
-   **Deep Insights:** Top 5 RAM-heavy processes, active Cron Jobs, and Systemd services.
-   **Security Alerts:** Highload warnings and active SSH session tracking.
-   **Dual Output:** Beautiful ANSI-colored console banner and a modern HTML dashboard.

## 🛠️ Installation

### Prerequisites
Ensure you have `smartmontools` installed for disk health reporting:
```
bash
sudo apt update && sudo apt install smartmontools nvidia-utils-535 -y
```


## Setup with uv (recommended)
Install uv python package manager at  https://docs.astral.sh/uv/getting-started/installation/

```
# Run the monitor
uv sync
uv run main.py
```
