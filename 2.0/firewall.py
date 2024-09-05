import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys

# Función para comprobar si el usuario es administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Funciones del firewall
def rule_exists():
    rule_name = "Bloquear Steam"
    result = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=' + rule_name], capture_output=True, text=True)
    return "No se encontró ninguna regla" not in result.stdout

def create_firewall_rule():
    rule_name = "Bloquear Steam"
    program_path = r"C:\Program Files (x86)\Steam\steam.exe"
    
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 
                    'name=' + rule_name, 'dir=out', 'program=' + program_path,
                    'action=block', 'profile=any', 'description=Regla para bloquear Steam'])
    
    messagebox.showinfo(messages['rule_created_title'], messages['rule_created_msg'])

def enable_firewall_rule():
    rule_name = "Bloquear Steam"
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'set', 'rule', 'name=' + rule_name, 'new', 'enable=yes'])
    messagebox.showinfo(messages['rule_enabled_title'], messages['rule_enabled_msg'])

def disable_firewall_rule():
    rule_name = "Bloquear Steam"
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'set', 'rule', 'name=' + rule_name, 'new', 'enable=no'])
    messagebox.showinfo(messages['rule_disabled_title'], messages['rule_disabled_msg'])

# Diccionarios para almacenar textos en diferentes idiomas
texts = {
    'es': {
        'title': "Gestión de Reglas de Firewall para Steam",
        'create_btn': "Crear y habilitar regla",
        'enable_btn': "Habilitar regla existente",
        'disable_btn': "Deshabilitar regla",
        'exit_btn': "Salir",
        'rule_created_title': "Regla creada",
        'rule_created_msg': "Regla de Firewall creada y habilitada.",
        'rule_enabled_title': "Regla habilitada",
        'rule_enabled_msg': "Regla de Firewall habilitada.",
        'rule_disabled_title': "Regla deshabilitada",
        'rule_disabled_msg': "Regla de Firewall deshabilitada."
    },
    'en': {
        'title': "Firewall Rule Management for Steam",
        'create_btn': "Create and enable rule",
        'enable_btn': "Enable existing rule",
        'disable_btn': "Disable rule",
        'exit_btn': "Exit",
        'rule_created_title': "Rule created",
        'rule_created_msg': "Firewall rule created and enabled.",
        'rule_enabled_title': "Rule enabled",
        'rule_enabled_msg': "Firewall rule enabled.",
        'rule_disabled_title': "Rule disabled",
        'rule_disabled_msg': "Firewall rule disabled."
    }
}

# Variable para almacenar los textos actuales
messages = texts['es']

# Función para cambiar el idioma
def change_language(lang):
    global messages
    messages = texts[lang]
    # Actualizar textos en la interfaz
    title_label.config(text=messages['title'])
    create_btn.config(text=messages['create_btn'])
    enable_btn.config(text=messages['enable_btn'])
    disable_btn.config(text=messages['disable_btn'])
    exit_btn.config(text=messages['exit_btn'])

def create_gui():
    global title_label, create_btn, enable_btn, disable_btn, exit_btn

    # Crear ventana
    root = tk.Tk()
    root.title("Firewall Management")
    root.geometry("400x300")
    root.configure(bg='#1a1a3d')  # Fondo azul oscuro

    # Selector de idioma en el lado izquierdo
    language_frame = tk.Frame(root, bg='#1a1a3d')
    language_frame.pack(side=tk.LEFT, padx=10)

    language_label = tk.Label(language_frame, text="Idioma / Language:", bg='#1a1a3d', fg='white')
    language_label.pack(anchor='w')

    language_var = tk.StringVar(value="es")
    language_menu = tk.OptionMenu(language_frame, language_var, "es", "en", command=change_language)
    language_menu.pack(anchor='w')

    # Crear etiquetas y botones en la interfaz principal
    main_frame = tk.Frame(root, bg='#1a1a3d')
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)

    # Etiqueta de título
    title_label = tk.Label(main_frame, text=messages['title'], bg='#1a1a3d', fg='#b366ff', font=("Helvetica", 14, "bold"))
    title_label.pack(pady=20)

    # Botón para crear y habilitar la regla
    create_btn = tk.Button(main_frame, text=messages['create_btn'], bg='#b366ff', fg='white', width=25, command=create_firewall_rule)
    create_btn.pack(pady=10)

    # Botón para habilitar la regla
    enable_btn = tk.Button(main_frame, text=messages['enable_btn'], bg='#b366ff', fg='white', width=25, command=enable_firewall_rule)
    enable_btn.pack(pady=10)

    # Botón para deshabilitar la regla
    disable_btn = tk.Button(main_frame, text=messages['disable_btn'], bg='#b366ff', fg='white', width=25, command=disable_firewall_rule)
    disable_btn.pack(pady=10)

    # Botón para salir
    exit_btn = tk.Button(main_frame, text=messages['exit_btn'], bg='#ff4d4d', fg='white', width=25, command=root.quit)
    exit_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    if is_admin():
        create_gui()
    else:
        messagebox.showerror("Error de permisos", "El programa necesita permisos de administrador.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
