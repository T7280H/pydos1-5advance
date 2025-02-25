import os
import sys
import time
import subprocess
from colorama import init, Fore, Style
from rich.progress import Progress, SpinnerColumn, TextColumn
import pyfiglet

# ✅ بررسی مسیر اسکریپت برای Pydroid 3
script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) if "__file__" not in globals() else os.path.dirname(os.path.abspath(__file__))

# ✅ لیست فایل‌های ضروری
REQUIRED_FILES = [
    "dev/__init__.py", "dev/exit.py", "dev/dir.py", "dev/ping.py", "dev/calc.py",
    "dev/date.py", "dev/edit.py", "dev/find.py", "dev/help.py", "dev/mkdir.py",
    "dev/rd.py", "dev/time.py", "dev/ver.py", "dev/restore.py", "dev/reminder.py",
    "dev/cIP.py", "dev/ifconfig.py", "dev/appmgr.py", "dev/bomb.py", "dev/pyrun.py",
    "dev/cls.py", "dev/echo.py", "dev/bootinf.py", "dev/cd.py", "dev/defpath.py",
    "dev/backup.py", "dev/xcopy.py", "dev/zip.py", "dev/unzip.py", "dev/wenda.py",
    "dev/ipfinder.py", "dev/tracker.py", "dev/bashrc.py", "dev/defpath.py", 
    "banner/__init__.py", "banner/banner.py",
    "main/pydos.py"
]

# ✅ بررسی فایل‌های ضروری
def check_files():
    all_files_present = True
    print(Fore.CYAN + "\n[✔] Checking required files...\n" + Style.RESET_ALL)
    
    for f in REQUIRED_FILES:
        file_path = os.path.join(script_dir, f)
        if os.path.exists(file_path):
            print(Fore.GREEN + f"[✔] {f} - OK" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[✘] {f} - Missing" + Style.RESET_ALL)
            all_files_present = False

    if not all_files_present:
        print(Fore.RED + "\n[ERROR] Some required files are missing. Boot process stopped.\n" + Style.RESET_ALL)
        sys.exit(1)

# ✅ لودینگ خطی با rich
def display_loading(message="Initializing..."):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task(f"[cyan]{message}", total=100)
        for _ in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

# ✅ نمایش بنر PyDOS همراه با لودینگ بعد از آن
def show_banner():
    os.system('clear')
    banner = pyfiglet.figlet_format("PYDOS 1.5 ADVANCED")
    print(Fore.BLUE + banner + Style.RESET_ALL)
    print(Fore.CYAN + "       T7280H | PYTHON CMD PROJECT\n" + Style.RESET_ALL)
    
    # ✅ اجرای لودینگ بعد از نمایش بنر
    display_loading("Booting PyDOS...")

# ✅ اجرای pydos.py
def run_pydos():
    time.sleep(1)
    os.system('clear')

    pydos_path = os.path.join(script_dir, "main", "pydos.py")

    if not os.path.exists(pydos_path):
        print(Fore.RED + f"\n[ERROR] File not found: {pydos_path}" + Style.RESET_ALL)
        sys.exit(1)

    try:
        subprocess.run(["python", pydos_path], check=True)
    except Exception as e:
        print(Fore.RED + f"\n[ERROR] Failed to run PyDOS: {e}" + Style.RESET_ALL)
        sys.exit(1)

# ✅ اجرای اصلی
if __name__ == "__main__":
    init(autoreset=True)
    check_files()
    display_loading("Checking System Files...")
    show_banner()
    run_pydos()