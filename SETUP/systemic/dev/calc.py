import ast
import sys
from colorama import Fore, Style, init
from rich.console import Console

# فعال‌سازی Colorama
init(autoreset=True)
console = Console()

def safe_eval(expression):
    """ محاسبه امن عبارت ریاضی با استفاده از AST """
    try:
        node = ast.parse(expression, mode='eval').body
        allowed_types = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow)
        
        if not all(isinstance(n, allowed_types) for n in ast.walk(node)):
            raise ValueError("Unsupported operation!")
        
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

def calc_command(expression):
    result = safe_eval(expression)
    console.print(f"[bold cyan]Result:[/bold cyan] {result}")

if __name__ == "__main__":
    console.print("[bold yellow]Simple Calculator - PyDOS[/bold yellow]")
    expression = input(Fore.CYAN + "Enter expression: " + Style.RESET_ALL)
    calc_command(expression)