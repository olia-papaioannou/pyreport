# messages.py
B, G, Y, R, E = "\033[1;34m", "\033[1;32m", "\033[1;33m", "\033[1;31m", "\033[0m"
WIDTH = 65 
VERSION = "v1.0.0"

def get_header(host, time_str):
    """Creates a perfectly aligned header banner."""
    spaces = " " * (WIDTH - len(host) - len(time_str) - 4)
    return f"  {B}{host}{E}{spaces}{Y}{time_str}{E}"

CONSOLE_TEMPLATE = f"""
{B}{"━" * WIDTH}{E}
{{header_line}}
{B}{"━" * WIDTH}{E}
{B}pyreport {VERSION}{E} | OS: {{os_ver}}
STATUS: {{alerts}}

{G}▶ PROCESSOR & DISPLAY:{E}
  Model: {{cpu_name}}
  Load:  {{cpu_pct}}% | Temp: {Y}{{cpu_temp}}{E} | Freq: {{cpu_max_ghz}} GHz
  Cores: {{cpu_cores}}
  Disp:  {{screen}}

{G}▶ GRAPHICS & NETWORK:{E}
  GPU:   {{gpu}}
  Net:   ↑{{net_up}} MB/s | ↓{{net_down}} MB/s | IP: {{ip}}

{G}▶ MEMORY & STORAGE:{E}
  RAM:   {{ram_used}}/{{ram_total}} GB ({{ram_pct}}%)
  Disk:  {{disk_used}}/{{disk_total}} GB ({{disk_pct}}%) | Tmp: {{tmp_mb}} MB

{G}▶ TOP 5 PROCESSES (BY RAM):{E}
{{top_procs}}

{G}▶ SCHEDULED CRON JOBS:{E}
{{cron_jobs}}

{G}▶ RECENT LOGINS & SERVICES:{E}
{{logins}}
{B}{"━" * WIDTH}{E}
"""

SUCCESS_HTML = "✅ pyreport {VERSION} updated: {{path}}".format(VERSION=VERSION)
ERROR_TEMPLATE = "❌ Error: template.html not found!"
