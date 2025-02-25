from rich.console import Console
from rich.table import Table

console = Console()

def help_command():
    """
    نمایش لیست دستورات موجود با توضیحات
    """
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
        "dash": "Dashborad", 
        "xcopy": "Copy files",
        "zip": "ZIP a file"
    }

    table = Table(title="PyDOS Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command", style="bold yellow", justify="left")
    table.add_column("Description", style="bold white", justify="left")

    for command, description in sorted(commands.items()):
        table.add_row(command, description)

    console.print(table)
    console.print(f"[bold cyan]Total Commands:[/bold cyan] {len(commands)}")

if __name__ == "__main__":
    help_command()