import sys
import os
import colorama
from colorama import Fore, Style, Back
from cmd import Cmd
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
import readline
import subprocess

# Add the path to the dev folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import commands from the dev folder
from dev.exit import exit_command
from dev.dir import dir_command
from dev.ping import ping_command
from dev.calc import calc_command
from dev.date import date_command
from dev.edit import edit_command
from dev.find import find_command
from dev.help import help_command
from dev.mkdir import mkdir_command
from dev.rd import rd_command
from dev.time import time_command
from dev.ver import ver_command
from dev.backup import backup_command
from dev.restore import restore_command
from dev.reminder import reminder_command
from dev.cIP import cIP_command
from dev.ifconfig import ifconfig_command
from dev.appmgr import appmgr_command
from dev.bomb import bomb_command
from dev.pyrun import pyrun_command
from dev.cls import cls_command
from dev.echo import echo_command
from dev.bootinf import bootinf_command
from dev.defpath import defpath_command
from dev.cd import cd_command
from dev.dash import dash_command
from dev.xcopy import xcopy_command
from dev.zip import zip_command
from dev.unzip import unzip_command
from dev.setting import setting_command
from dev.wenda import wenda_command
from dev.bashrc import bashrc_command
from dev.ipfinder import ipfinder_command
from dev.tracker import tracker_command

console = Console()

def load_banner():
    try:
        # Read current_banner.txt from the banner folder
        banner_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'banner'))
        current_banner_path = os.path.join(banner_dir, 'current_banner.txt')

        with open(current_banner_path, 'r') as f:
            banner_file = f.read().strip()
        banner_path = os.path.join(banner_dir, banner_file)
        
        # Execute the banner file and only display the output
        with open(banner_path, 'r') as f:
            banner_code = f.read()
        exec(banner_code, {'__name__': '__main__'})
        
    except FileNotFoundError:
        pass
    except Exception as e:
        pass

class PyDOSCmd(Cmd):
    prompt = Back.RED + Fore.BLACK + 'PyDOS> ' + Style.RESET_ALL
    intro = Fore.GREEN + 'PyDOS 1.5 ADVANCED | PYTHON CMD PROJECT' + Style.RESET_ALL
    gulie = Fore.BLUE + 'TO SEE COMMAND TYPE (help)' + Style.RESET_ALL

    def preloop(self):
        load_banner()

    def do_exit(self, line):
        exit_command()
        return True

    def do_dir(self, line):
        dir_command()

    def do_ping(self, line):
        with Progress() as progress:
            task = progress.add_task("[cyan]Pinging...", total=100)
            while not progress.finished:
                progress.update(task, advance=1)
                ping_command(line)
                break

    def do_calc(self, line):
        calc_command(line)

    def do_date(self, line):
        date_command()

    def do_edit(self, line):
        edit_command()

    def do_find(self, line):
        find_command()

    def do_help(self, line):
        help_command()

    def do_mkdir(self, line):
        mkdir_command()

    def do_rd(self, arg):
        if not arg:
            print("Error: Please specify a file or directory to remove.")
        else:
            rd_command(arg)

    def do_time(self, line):
        time_command()

    def do_ver(self, line):
        ver_command()

    def do_restore(self, line):
        args = line.split()
        if len(args) < 1:
            return
        restore_path = args[0]
        restore_command(restore_path)

    def do_reminder(self, line):
        args = line.split()
        if len(args) < 2:
            return
        message = args[0]
        delay = int(args[1])
        reminder_command(message, delay)

    def do_cIP(self, line):
        cIP_command(line)

    def do_ifconfig(self, line):
        ifconfig_command()

    def do_appmgr(self, line):
        args = line.split()
        if len(args) < 2:
            return
        appmgr_command(args[0], args[1])

    def do_bomb(self, line):
        bomb_command()

    def do_pyrun(self, line):
        pyrun_command(line)

    def do_cls(self, line):
        cls_command()

    def do_echo(self, line):
        echo_command(line)

    def do_bootinf(self, line):
        bootinf_command()

    def do_cd(self, line):
        cd_command(line)
    	
    def do_defpath(self, line):
        defpath_command()
    
    def do_dash(self, line):
        dash_command()
    
    def do_backup(self, line):
        args = line.split()
        if len(args) < 2:
            return
        backup_command(args[0], args[1])
    
    def do_xcopy(self, line):
        args = line.split()
        if len(args) < 2:
            return
        xcopy_command(args[0], args[1])

    def do_setting(self, line):
        setting_command()
     
    def do_zip(self, line):
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] You need to provide both source and destination.")
            return

        source = args[0]
        destination = args[1]

        zip_command(source, destination)
        
    def do_unzip(self, line):
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] You need to provide both source and destination.")
            return

        source = args[0]
        destination = args[1]

        unzip_command(source, destination)
        
    def do_wenda(self, line):
        subprocess.run(['clear'])
        wenda_command()
    	
    def do_bashrc(self, line):
        subprocess.run(['clear'])
        bashrc_command()
    	
    def do_ipfinder(self, line):
        subprocess.run(['clear'])
        ipfinder_command()
    	
    def do_tracker(self, line):
        subprocess.run(['clear'])
        tracker_command()

    def complete(self, text, state):
        commands = [command[3:] for command in dir(self.__class__) if command.startswith('do_')]
        matches = [command for command in commands if command.startswith(text)]
        try:
            return matches[state]
        except IndexError:
            return None

    def default(self, line):
        pass

if __name__ == '__main__':
    colorama.init()
    PyDOSCmd().cmdloop()
    colorama.deinit()