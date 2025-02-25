import socket
import platform
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def dash_command():
    """
    نمایش داشبورد اطلاعات سیستم و دستورات PyDOS
    """
    try:
        # اطلاعات دستگاه
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        os_info = platform.system() + " " + platform.release()
        cpu_info = platform.processor() or "Unknown"
        ram_info = f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 1)} GB"
        cpu_usage = f"{psutil.cpu_percent()}%"
        ram_usage = f"{psutil.virtual_memory().percent}%"

        # نمایش پنل اطلاعات سیستم
        system_panel = Panel(
            f"[bold cyan]Hostname:[/bold cyan] {hostname}\n"
            f"[bold yellow]IP Address:[/bold yellow] {ip_address}\n"
            f"[bold magenta]OS:[/bold magenta] {os_info}\n"
            f"[bold green]Processor:[/bold green] {cpu_info}\n"
            f"[bold blue]RAM:[/bold blue] {ram_info} ([bold red]{ram_usage} used[/bold red])\n"
            f"[bold blue]CPU Usage:[/bold blue] [bold red]{cpu_usage}[/bold red]",
            title="[bold green]System Information[/bold green]", expand=False
        )
        console.print(system_panel)

        # لیست دستورات PyDOS
        commands = {
            "backup": "Backup all files",
            "bashrc": "Bash Converter",
            "bomb": "Run SMS bomber (pybomb.py in apps folder)",
            "bootinf": "Show boot version",
            "calc": "Calculator",
            "cd": "Change directory",
            "cls": "Clear the screen",
            "date": "Show date",
            "defpath": "Show current directory path",
            "dir": "List directories",
            "echo": "Print a message",
            "edit": "Text editor",
            "exit": "Exit PyDOS",
            "help": "Display command help",
            "ifconfig": "Show IP address",
            "ipfinder": "Find IP information",
            "mkdir": "Create directory",
            "ping": "Ping test",
            "pyrun": "Run Python applications",
            "rd": "Remove file or directory",
            "reminder": "Set a reminder",
            "restore": "Restore all files",
            "setting": "Config settings",
            "time": "Show time",
            "tracker": "IP Tracker",
            "unzip": "Unzip a file",
            "wenda": "Run Wenda Converter",
            "xcopy": "Copy files",
            "zip": "ZIP a file"
        }

        # نمایش لیست دستورات در جدول
        table = Table(title="PyDOS Commands", show_header=True, header_style="bold cyan")
        table.add_column("Command", style="bold yellow", justify="left")
        table.add_column("Description", style="bold white", justify="left")

        for command, description in sorted(commands.items()):
            table.add_row(command, description)

        console.print(table)
        console.print(f"[bold cyan]Total Commands:[/bold cyan] {len(commands)}")

    except PermissionError as e:
        console.print(f"[bold red]Error:[/bold red] Permission denied while accessing system information. Please run PyDOS with elevated privileges.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    dash_command()