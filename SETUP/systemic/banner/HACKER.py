# کدهای رنگ ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_banner():
    # بنر HACKER با جلوه برجسته
    banner = f"""{RED}{BOLD}
██   ██  █████   ██████ ██   ██ ███████ ██████  
 ██ ██  ██   ██ ██      ██  ██  ██      ██   ██ 
  ███   ███████ ██      █████   █████   ██████  
 ██ ██  ██   ██ ██      ██  ██  ██      ██   ██ 
██   ██ ██   ██  ██████ ██   ██ ███████ ██   ██ 
{RESET}
"""
    print(banner)

# اجرای تابع
if __name__ == "__main__":
    print_banner()