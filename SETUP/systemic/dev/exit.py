import sys
import time
import os
from rich.console import Console

console = Console()

def loading_animation(message):
    """
    نمایش لودینگ چرخشی کوتاه‌تر
    """
    for _ in range(5):  # به جای 10 دور، 5 دور بچرخه
        for char in "|/-\\":
            sys.stdout.write(f'\r{message} {char}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\rDone!       \n')

def exit_command():
    """
    خروج از PyDOS با تاییدیه کاربر و پاک‌سازی صفحه
    """
    console.print("[bold red]Are you sure you want to exit PyDOS? (Y/N)[/bold red]", end=" ")
    user_input = input().strip().upper()
    
    if user_input == 'Y':
        loading_animation("Exiting PyDOS")
        os.system('cls' if os.name == 'nt' else 'clear')  # پاک کردن صفحه
        console.print("[bold green]Goodbye![/bold green]")
        sys.exit(0)
    elif user_input == 'N':
        console.print("[bold yellow]Exit cancelled.[/bold yellow]")
    else:
        console.print("[bold red]Invalid input. Exit cancelled.[/bold red]")

if __name__ == "__main__":
    exit_command()