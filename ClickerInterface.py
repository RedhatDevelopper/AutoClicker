import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import ctypes
import keyboard
from pynput import mouse

# Fonction pour effectuer un clic à la position actuelle du curseur
def autoclick():
    global autoclick_paused
    while autoclick_running:
        if not autoclick_paused:
            try:
                if hitbox_active:
                    keyboard.press('F3')
                    keyboard.press('B')
                    keyboard.release('B')
                    keyboard.release('F3')
                
                # Vérifier si le bouton gauche de la souris est enfoncé
                if mouse_controller.current_button == mouse.Button.left:
                    # Effectuer le clic
                    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Appui sur le bouton gauche de la souris
                    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Relâchement du bouton gauche de la souris
            except Exception as e:
                print(f"Erreur lors de l'autoclick : {e}")
        time.sleep(click_interval)  # Attendre le délai spécifié avant de cliquer à nouveau

# Fonction pour arrêter l'autoclick
def stop_autoclick():
    global autoclick_running
    autoclick_running = False

# Fonction pour démarrer l'autoclick
def start_autoclick():
    global autoclick_running
    if not autoclick_running:
        autoclick_running = True
        autoclick_thread = threading.Thread(target=autoclick)
        autoclick_thread.start()

# Fonction pour changer la vitesse du clic
def change_click_speed():
    global click_interval
    speed = float(speed_entry.get())
    click_interval = 1 / speed

# Fonction pour mettre en pause l'autoclick
def pause_autoclick():
    global autoclick_paused
    autoclick_paused = not autoclick_paused

# Fonction pour activer la hitbox
def activer_hitbox():
    global hitbox_active
    hitbox_active = True

# Fonction pour désactiver la hitbox
def desactiver_hitbox():
    global hitbox_active
    hitbox_active = False

# Classe de rappel pour détecter les clics de souris
class MouseController:
    def __init__(self):
        self.current_button = None

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            self.current_button = button

    def on_release(self, x, y, button):
        if button == mouse.Button.left:
            self.current_button = None

# Créer une instance de la classe MouseController
mouse_controller = MouseController()

# Créer un écouteur de souris
mouse_listener = mouse.Listener(on_click=mouse_controller.on_click, on_release=mouse_controller.on_release)

# Fonction pour démarrer l'écoute de la souris
def start_mouse_listener():
    mouse_listener.start()

# Démarrer l'écoute de la souris dans un thread séparé
mouse_listener_thread = threading.Thread(target=start_mouse_listener)
mouse_listener_thread.start()

# Fonction pour gérer l'appui sur les touches clavier
def on_key_press(event):
    if event.name == 'x':
        start_autoclick()
    elif event.name == 'c':
        stop_autoclick()

# Associer la fonction de gestion des touches à l'événement d'appui sur une touche
keyboard.on_press(on_key_press)

# Création de la fenêtre principale
root = tk.Tk()
root.title("RedHat")

# Variables de contrôle
autoclick_running = False
click_interval = 1.0 / 10000  # 20 clics par seconde
autoclick_paused = False
hitbox_active = False

# Style
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", foreground="white", background="#4CAF50")
style.map("TButton", foreground=[('pressed', 'black'), ('active', 'black')],
          background=[('pressed', '!disabled', '#45a049'), ('active', '#45a049')])

# Conteneur principal
container = ttk.Frame(root, padding="20", relief="groove", borderwidth=2)
container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Titre
title_label = ttk.Label(container, text="RedHat", font=("Segoe UI", 18))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Vitesse du clic
speed_label = ttk.Label(container, text="Vitesse du clic:")
speed_label.grid(row=1, column=0, pady=5, sticky=tk.E)
speed_entry = ttk.Entry(container)
speed_entry.grid(row=1, column=1, pady=5)
speed_entry.insert(0, "1.0")

# Bouton pour changer la vitesse
change_speed_button = ttk.Button(container, text="Changer la vitesse", command=change_click_speed)
change_speed_button.grid(row=2, column=0, columnspan=2, pady=5)

# Bouton pour démarrer l'autoclick
start_button = ttk.Button(container, text="Démarrer Autoclick", command=start_autoclick)
start_button.grid(row=3, column=0, pady=5)

# Bouton pour arrêter l'autoclick
stop_button = ttk.Button(container, text="Arrêter Autoclick", command=stop_autoclick)
stop_button.grid(row=3, column=1, pady=5)

# Bouton pour activer la hitbox
activate_hitbox_button = ttk.Button(container, text="Activer la hitbox", command=activer_hitbox)
activate_hitbox_button.grid(row=4, column=0, pady=5)

# Bouton pour désactiver la hitbox
deactivate_hitbox_button = ttk.Button(container, text="Désactiver la hitbox", command=desactiver_hitbox)
deactivate_hitbox_button.grid(row=4, column=1, pady=5)

# Crédits
credits_label = ttk.Label(container, text="by Empereur", font=("Segoe UI", 10))
credits_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

# Exécution de la boucle principale
root.mainloop()
