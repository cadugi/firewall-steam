import ctypes
import subprocess
import sys
import os
from colorama import init, Fore, Style

# Inicializa colorama para que funcione en Windows
init(autoreset=True)

def is_admin():
    """Comprueba si el script se está ejecutando con privilegios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def print_color(text, color):
    colors = {
        "cyan": Fore.CYAN,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
    }
    print(f"{colors[color]}{text}{Style.RESET_ALL}")

def rule_exists():
    rule_name = "Bloquear Steam"
    result = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=' + rule_name], capture_output=True, text=True)
    return "No se encontró ninguna regla" not in result.stdout

def create_firewall_rule():
    rule_name = "Bloquear Steam"
    program_path = r"C:\Program Files (x86)\Steam\steam.exe"
    
    # Crear regla de salida
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 
                    'name=' + rule_name, 'dir=out', 'program=' + program_path,
                    'action=block', 'profile=any', 'description=Regla para bloquear Steam'])
    
    print_color("Regla de Firewall creada y habilitada.", "green")

def enable_firewall_rule():
    rule_name = "Bloquear Steam"
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'set', 'rule', 'name=' + rule_name, 'new', 'enable=yes'])
    print_color("Regla de Firewall habilitada.", "green")

def disable_firewall_rule():
    rule_name = "Bloquear Steam"
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'set', 'rule', 'name=' + rule_name, 'new', 'enable=no'])
    print_color("Regla de Firewall deshabilitada.", "green")

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    while True:
        # Limpia la pantalla antes de mostrar el menú
        clear_screen()

        print_color("\nSelecciona una opción:", "cyan")
        print("1. Crear y habilitar la regla de Firewall")
        print("2. Habilitar la regla de Firewall")
        print("3. Deshabilitar la regla de Firewall")
        print("4. Salir")
        opcion = input("Introduce el número de la opción: ")

        # Limpia la pantalla antes de ejecutar cualquier opción
        clear_screen()

        if opcion == '1':
            if not rule_exists():
                create_firewall_rule()
            else:
                print_color("La regla ya existe.", "yellow")
                enable_firewall_rule()

        elif opcion == '2':
            if rule_exists():
                enable_firewall_rule()
            else:
                print_color("La regla no existe, primero debes crearla.", "red")

        elif opcion == '3':
            if rule_exists():
                disable_firewall_rule()
            else:
                print_color("La regla no existe, primero debes crearla.", "red")

        elif opcion == '4':
            print_color("Saliendo...", "cyan")
            break

        else:
            print_color("Opción no válida.", "red")

        input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    if is_admin():
        print_color("Gestión de Reglas de Firewall para Steam", "cyan")
        show_menu()
    else:
        # Si no se están ejecutando con permisos de administrador, relanzamos el script con esos permisos.
        print_color("El programa necesita permisos de administrador.", "red")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
