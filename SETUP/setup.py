import os
import shutil
import subprocess
import time
import curses
from rich.console import Console

# Initialize rich console for better output
console = Console()

VALID_LICENSE_CODE = "PYDOS-8190-3671-BN82"  # کد لایسنس معتبر

def print_center(stdscr, text, delay=0.01):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x = width // 2 - len(text) // 2
    y = height // 2
    for char in text:
        stdscr.addstr(y, x, char)
        stdscr.refresh()
        time.sleep(delay)
        x += 1
    time.sleep(1)
    stdscr.clear()
    stdscr.refresh()

def print_slow(stdscr, text, delay=0.01):
    height, width = stdscr.getmaxyx()
    lines = []
    for i in range(0, len(text), width - 1):
        lines.append(text[i:i + width - 1])
    for line in lines:
        stdscr.addstr(line + "\n")
        stdscr.refresh()
        time.sleep(delay)
    stdscr.refresh()

def draw_menu(stdscr, selected_row_idx, menu):
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h - 2 - len(menu) + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def create_message_box(stdscr, message, display_time=2):
    h, w = stdscr.getmaxyx()
    box_width = min(max(len(message) + 4, 50), w - 2)  # Width set to max 50
    box_height = min(5, h - 2)  # Height set to max 5
    box_x = w // 2 - box_width // 2
    box_y = h // 2 - box_height // 2

    # Create the message box background
    stdscr.attron(curses.color_pair(2))
    for i in range(box_height + 1):
        stdscr.addstr(box_y + i + 1, box_x + 1, " " * box_width)
    stdscr.attroff(curses.color_pair(2))

    stdscr.attron(curses.color_pair(1))
    for i in range(box_height):
        stdscr.addstr(box_y + i, box_x, " " * box_width)

    # Split the message if it's too long
    message_lines = message.splitlines()
    for idx, line in enumerate(message_lines):
        if idx >= box_height - 2:  # Leave space for borders
            break  # Prevent overflow
        if len(line) > box_width - 4:  # Truncate if too long
            line = line[:box_width - 4]
        # Ensure we do not exceed the window size
        if box_y + 1 + idx < h and box_x + 2 + len(line) < w:  # Check row and column limits
            stdscr.addstr(box_y + 1 + idx, box_x + 2, line)

    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(display_time)  # نمایش پیام به مدت معین
    stdscr.clear()  # پاک کردن صفحه پس از نمایش پیام

def check_files(files, base_path):
    missing_files = []
    for file in files:
        if not os.path.exists(os.path.join(base_path, file)):
            missing_files.append(file)
    return missing_files

def spin_loader(stdscr, message, duration=2):
    h, w = stdscr.getmaxyx()
    box_width = min(max(len(message) + 4, 50), w - 2)  # Ensure box fits within window width
    box_height = 5
    box_x = w // 2 - box_width // 2
    box_y = h // 2 - box_height // 2

    stdscr.attron(curses.color_pair(2))
    for i in range(box_height + 1):
        stdscr.addstr(box_y + i + 1, box_x + 1, " " * box_width)
    stdscr.attroff(curses.color_pair(2))

    stdscr.attron(curses.color_pair(1))
    for i in range(box_height):
        stdscr.addstr(box_y + i, box_x, " " * box_width)

    stdscr.addstr(box_y + 1, box_x + 2, message)
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()

    spinner = ['|', '/', '-', '\\']
    for _ in range(duration * 10):
        for char in spinner:
            stdscr.addstr(box_y + 3, box_x + 2, char)
            stdscr.refresh()
            time.sleep(0.1)

    stdscr.clear()
    stdscr.refresh()

def select_install_path(stdscr):
    create_message_box(stdscr, "Please select the installation path.")
    return input_window(stdscr, "Enter the installation path (e.g., /storage/emulated/0): ")

def enter_name_and_company(stdscr):
    create_message_box(stdscr, "Please enter your name and company information.")
    name = input_window(stdscr, "Enter your name: ")
    company = input_window(stdscr, "Enter your company: ")
    return name, company

def input_window(stdscr, prompt):
    h, w = stdscr.getmaxyx()
    input_height = 5
    input_width = min(max(len(prompt) + 4, 50), w - 2)  # Width set to max 50
    input_win = curses.newwin(input_height, input_width, h // 2 - input_height // 2, w // 2 - input_width // 2)
    input_win.box()
    input_win.addstr(1, 1, prompt)
    input_win.refresh()
    curses.echo()
    user_input = input_win.getstr(1, len(prompt) + 1).decode().strip()
    curses.noecho()
    return user_input

def license_agreement(stdscr):
    license_text = """
    PyDOS License Agreement
    ------------------------
    By using this software, you agree to the following terms and conditions:
    1. You may use this software for personal and commercial purposes.
    2. Redistribution of this software is prohibited without prior written consent.
    3. The author is not responsible for any damage caused by the use of this software.
    """
    print_slow(stdscr, license_text)
    menu = ["Yes", "No"]
    current_row = 0
    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_row == 0

def input_license_code(stdscr):
    while True:
        license_code = input_window(stdscr, "Enter the license code: ")

        # Validate the license code
        if license_code == VALID_LICENSE_CODE:
            return license_code
        else:
            create_message_box(stdscr, "Invalid license code. Please try again.")

def save_user_info(stdscr, name, company, install_path, license_code):
    user_info_path = os.path.join(install_path, "usr.txt")
    with open(user_info_path, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Company: {company}\n")
        file.write(f"License Code: {license_code}\n")  # Save the license code
    create_message_box(stdscr, f"User information saved to {user_info_path}")

def check_memory(stdscr):
    create_message_box(stdscr, "Checking memory...")
    spin_loader(stdscr, "Checking memory", duration=2)
    create_message_box(stdscr, "Memory check complete.")

def format_directory(stdscr, path):
    create_message_box(stdscr, f"Formatting directory: {path}")
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))
    create_message_box(stdscr, f"Directory {path} formatted successfully")

def create_directories(stdscr, destination):
    directories = ["dev", "main", "banner", "apps"]
    for directory in directories:
        os.makedirs(os.path.join(destination, directory), exist_ok=True)
    create_message_box(stdscr, "Directories created successfully")

def copy_files(stdscr, files, base_path, destination):
    create_message_box(stdscr, "Copying files...")
    for file, target_dir in files.items():
        target_path = os.path.join(destination, target_dir)
        
        # نمایش نام فایل در حال کپی شدن
        create_message_box(stdscr, f"Writing: {file.split('/')[-1]}", display_time=1)  # فقط نام فایل را نمایش می‌دهیم

        try:
            shutil.copy(os.path.join(base_path, file), target_path)
        except FileNotFoundError:
            create_message_box(stdscr, f"Error: {file} not found. Skipping...")
    create_message_box(stdscr, "Files copied successfully")

def copy_boot_file(stdscr, base_path, install_path):
    create_message_box(stdscr, "Copying boot.py...")
    shutil.copy(os.path.join(base_path, "boot.py"), install_path)
    create_message_box(stdscr, "boot.py copied successfully")

def install_requirements(stdscr, base_path):
    create_message_box(stdscr, "Installing required packages...")
    try:
        subprocess.check_call(["pip", "install", "-r", os.path.join(base_path, "requirements.txt")])
        create_message_box(stdscr, "Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        create_message_box(stdscr, f"Error installing requirements: {e}")

def display_readme(stdscr, base_path):
    readme_path = os.path.join(base_path, "read", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as file:
            readme_lines = file.readlines()
        current_line = 0
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            for i, line in enumerate(readme_lines[current_line:current_line + height - 1]):
                stdscr.addstr(i, 0, line.strip())
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_DOWN and current_line < len(readme_lines) - height + 1:
                current_line += 1
            elif key == curses.KEY_UP and current_line > 0:
                current_line -= 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
    else:
        create_message_box(stdscr, "README.md file not found in 'read' folder.")

    menu = ["Return"]
    current_row = 0
    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                return

def setup_complete(stdscr):
    create_message_box(stdscr, "Setup is complete. PyDOS is installed, please wait...")

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    stdscr.bkgd(' ', curses.color_pair(2))
    current_row = 0

    base_path = "systemic"
    required_files = [
        "dev/__init__.py", "dev/help.py", "dev/echo.py", "dev/rd.py", "dev/cIP.py", 'dev/ifconfig.py', "dev/edit.py",
        "dev/appmgr.py", "dev/bootinf.py", "dev/dir.py", "dev/reminder.py", "dev/time.py", "dev/date.py", "dev/dash.py",
        "dev/zip.py", "dev/unzip.py", "dev/setting.py", "dev/pyrun.py", "dev/ping.py", "dev/defpath.py", "dev/mkdir.py",
        "dev/cd.py", "dev/xcopy.py", "dev/calc.py", "dev/find.py", "dev/backup.py", "dev/restore.py", "dev/ver.py",
        "dev/exit.py", "dev/cls.py", "dev/ipfinder.py", "dev/tracker.py", "dev/wenda.py", "dev/bashrc.py", "main/pydos.py", "banner/banner.py", "banner/HACKER.py", "banner/logo.py",
        "banner/PyDOSbanner.py", "banner/__init__.py", "apps/__init__.py", "apps/editor.py", "apps/pybomber.py", "apps/IPFINDER.py", "boot.py", "apps/wendaconverter.py", "apps/bashconverter.py", "apps/iptracker.py", 
        "requirements.txt"
    ]

    files = {
        "main/pydos.py": "main",
        "dev/echo.py": "dev",
        "dev/dir.py": "dev",
        "dev/cd.py": "dev",
        "dev/rd.py": "dev",
        "dev/appmgr.py": "dev",
        "dev/bootinf.py": "dev",
        "dev/help.py": "dev",
        "dev/defpath.py": "dev",
        "dev/mkdir.py": "dev",
        "dev/time.py": "dev",
        "dev/date.py": "dev",
        "dev/ifconfig.py": "dev",
        "dev/cIP.py": "dev",
        "dev/dash.py": "dev",
        "dev/bootinf.py": "dev",
        "dev/xcopy.py": "dev",
        "dev/ping.py": "dev",
        "dev/pyrun.py": "dev",
        "dev/find.py": "dev",
        "dev/calc.py": "dev",
        "dev/unzip.py": "dev",
        "dev/zip.py": "dev",
        "dev/setting.py": "dev",
        "dev/backup.py": "dev",
        "dev/restore.py": "dev",
        "dev/reminder.py": "dev",
        "dev/ver.py": "dev",
        "dev/exit.py": "dev",
        "dev/cls.py": "dev",
        "dev/bomb.py": "dev",
        "dev/edit.py": "dev",
        "dev/ipfinder.py": "dev", 
        "dev/tracker.py": "dev", 
        "dev/wenda.py": "dev", 
        "dev/bashrc.py": "dev", 
        "dev/__init__.py": "dev",
        "banner/banner.py": "banner",
        "banner/HACKER.py": "banner",
        "banner/logo.py": "banner",
        "banner/PyDOSbanner.py": "banner",
        "banner/__init__.py": "banner",
        "apps/editor.py": "apps",
        "apps/pybomber.py": "apps",
        "apps/IPFINDER.py": "apps", 
        "apps/wendaconverter.py": "apps", 
        "apps/bashconverter.py": "apps", 
        "apps/iptracker.py": "apps", 
        "apps/__init__.py": "apps"
    }

    try:
        print_center(stdscr, "SETUP IS STARTING...")
        print_slow(stdscr, "Checking required files...")
        missing_files = check_files(required_files, base_path)
        if missing_files:
            print_slow(stdscr, "Required files are missing. Setup cannot proceed.")
            print_slow(stdscr, f"Missing files: {', '.join(missing_files)}")
            return
        spin_loader(stdscr, "Checking files", duration=2)

        welcome_message = "Welcome to PyDOS!, press the Install PyDOS button.\n"
        create_message_box(stdscr, welcome_message)
        menu = ["Install PyDOS", "Exit"]
        while True:
            draw_menu(stdscr, current_row, menu)
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 1:
                    return
                break

        print_center(stdscr, "Select Installation Path")
        install_path = select_install_path(stdscr)

        while True:
            print_center(stdscr, "Enter Name and Company")
            name, company = enter_name_and_company(stdscr)
            if name and company:
                break
            menu = ["Retry", "Back"]
            current_row = 0
            while True:
                draw_menu(stdscr, current_row, menu)
                key = stdscr.getch()
                if key == curses.KEY_UP and current_row > 0:
                    current_row -= 1
                elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                    current_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if current_row == 1:
                        return
                    break

        if not license_agreement(stdscr):
            create_message_box(stdscr, "You must accept the license agreement to proceed.")
            return

        # دریافت کد لایسنس از کاربر
        license_code = input_license_code(stdscr)

        # ذخیره اطلاعات کاربر و کد لایسنس
        save_user_info(stdscr, name, company, install_path, license_code)

        print_center(stdscr, "SETUP IS CHECKING YOUR MEMORY...")
        check_memory(stdscr)

        display_readme(stdscr, base_path)

        print_center(stdscr, "SETUP IS FORMATTING INSTALLATION DIRECTORY...")
        format_directory(stdscr, install_path)

        print_center(stdscr, "SETUP IS CREATING DICTIONARIES...")
        create_directories(stdscr, install_path)

        print_center(stdscr, "SETUP IS COPYING SYSTEM FILES...")
        copy_files(stdscr, files, base_path, install_path)

        print_center(stdscr, "SETUP IS COPYING BOOT.PY...")
        copy_boot_file(stdscr, base_path, install_path)

        print_center(stdscr, "SETUP IS INSTALLING REQUIREMENTS...")
        install_requirements(stdscr, base_path)

        print_center(stdscr, "Setup Complete")
        setup_complete(stdscr)
        menu = ["Exit"]
        current_row = 0
        while True:
            draw_menu(stdscr, current_row, menu)
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 0:
                    return

    except Exception as e:
        create_message_box(stdscr, f"An error occurred: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main)