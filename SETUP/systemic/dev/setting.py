import os
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

ACCOUNTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'accounts.json')
BANNER_DIR = os.path.join(os.path.dirname(__file__), '..', 'banner')

def load_accounts():
    """بارگذاری حساب‌ها از فایل"""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_accounts(accounts):
    """ذخیره حساب‌ها در فایل"""
    with open(ACCOUNTS_FILE, 'w') as file:
        json.dump(accounts, file, indent=4)

def create_account():
    """ایجاد حساب جدید"""
    console.print("[bold cyan]Create an Account[/bold cyan]")
    username = Prompt.ask("Enter username")
    password = Prompt.ask("Enter password", password=True)

    accounts = load_accounts()
    if username in accounts:
        console.print("[bold red]Error:[/bold red] Username already exists!")
    else:
        accounts[username] = password
        save_accounts(accounts)
        console.print("[bold green]Account created successfully![/bold green]")

def login_account():
    """ورود به حساب کاربری"""
    console.print("[bold cyan]Login to your Account[/bold cyan]")
    username = Prompt.ask("Enter username")
    password = Prompt.ask("Enter password", password=True)

    accounts = load_accounts()
    if accounts.get(username) == password:
        console.print("[bold green]Login successful![/bold green]")
    else:
        console.print("[bold red]Login failed:[/bold red] Incorrect username or password.")

def change_banner():
    """تغییر بنر PyDOS"""
    console.print("[bold cyan]Select a Banner[/bold cyan]")
    
    if not os.path.exists(BANNER_DIR):
        console.print("[bold red]Error:[/bold red] Banner folder not found!")
        return

    banners = [f for f in os.listdir(BANNER_DIR) if os.path.isfile(os.path.join(BANNER_DIR, f))]
    
    if not banners:
        console.print("[bold yellow]No banners found in the folder.[/bold yellow]")
        return

    table = Table(title="Available Banners")
    table.add_column("ID", style="bold yellow")
    table.add_column("Banner Name", style="bold white")

    for idx, banner in enumerate(banners, start=1):
        table.add_row(str(idx), banner)

    console.print(table)

    choice = Prompt.ask("Select a banner by ID", choices=[str(i) for i in range(1, len(banners) + 1)])
    selected_banner = banners[int(choice) - 1]

    with open(os.path.join(BANNER_DIR, 'current_banner.txt'), 'w') as file:
        file.write(selected_banner)

    console.print(f"[bold green]Banner '{selected_banner}' selected successfully![/bold green]")

def show_pydos_info():
    """نمایش اطلاعات PyDOS"""
    console.print("[bold cyan]PyDOS System Information[/bold cyan]")
    console.print("[bold yellow]Version:[/bold yellow] 1.5 ADVANCED")
    console.print("[bold yellow]Developer:[/bold yellow] T7280H")
    console.print("[bold yellow]GitHub:[/bold yellow] [blue]https://github.com/T7280H/PyDOS[/blue]")

def setting_command():
    """منوی تنظیمات PyDOS"""
    options = {
        "1": ("Create an Account", create_account),
        "2": ("Login to your Account", login_account),
        "3": ("Change PyDOS Banner", change_banner),
        "4": ("Show PyDOS Info", show_pydos_info),
        "5": ("Exit Settings", lambda: None),
    }

    while True:
        console.print("\n[bold cyan]PyDOS Settings[/bold cyan]")
        table = Table(title="Options")
        table.add_column("ID", style="bold yellow")
        table.add_column("Description", style="bold white")

        for key, (desc, _) in options.items():
            table.add_row(key, desc)

        console.print(table)

        choice = Prompt.ask("Select an option", choices=options.keys())
        if choice == "5":
            console.print("[bold yellow]Returning to PyDOS...[/bold yellow]")
            break

        options[choice][1]()  # اجرای تابع مربوطه

if __name__ == "__main__":
    setting_command()