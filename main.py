# autoclicker.py
import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import threading
import configparser
import time
import os
import requests

# Default configuration settings
default_config = {
    'settings': {
        'hotkey': 'f6',
        'current_version': '0.0.0'
    },
    'window': {
        'size': '400x400'
    }
}

# Load or create configuration
config = configparser.ConfigParser()
config_path = 'config.ccof'

if not os.path.exists(config_path):
    config.read_dict(default_config)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
else:
    config.read(config_path)

# Function to compare versions
def compare_versions(current, latest):
    return tuple(map(int, current.split('.'))) < tuple(map(int, latest.split('.')))

# Function to check for updates
def check_for_updates():
    try:
        latest_version = requests.get('https://creeperjaegermax.github.io/CClicker/Latest.txt').text.strip()
        current_version = config['settings'].get('current_version', '0.0.0')
        if compare_versions(current_version, latest_version):
            update_code(latest_version)
        else:
            print("You are using the latest version.")
    except Exception as e:
        print(f"Error checking for updates: {e}")

# Function to update the code
def update_code(latest_version):
    try:
        response = requests.get('https://creeperjaegermax.github.io/CClicker/CClicker.py')
        with open('CClicker.py', 'w') as file:
            file.write(response.text)
        config['settings']['current_version'] = latest_version
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        print(f"Updated to version {latest_version}.")
    except Exception as e:
        print(f"Error updating code: {e}")

check_for_updates()

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        window_size = config['window']['size']
        self.root.geometry(window_size)
        self.root.configure(bg="lightgrey")
        
        self.running = False
        self.click_type = 'left'
        
        self.create_widgets()

    def create_widgets(self):
        font_style = ("Comic Sans MS", 12)
        
        tk.Label(self.root, text="AutoClicker", font=("Comic Sans MS", 16), bg="lightgrey").pack(pady=10)
        
        self.left_click_btn = tk.Button(self.root, text="Left Click", font=font_style, command=lambda: self.set_click_type('left'))
        self.left_click_btn.pack(pady=5)
        
        self.right_click_btn = tk.Button(self.root, text="Right Click", font=font_style, command=lambda: self.set_click_type('right'))
        self.right_click_btn.pack(pady=5)
        
        self.start_stop_btn = tk.Button(self.root, text="Start/Stop", font=font_style, command=self.toggle_autoclick)
        self.start_stop_btn.pack(pady=20)
        
        self.status_label = tk.Label(self.root, text="Status: Stopped", font=font_style, bg="lightgrey")
        self.status_label.pack(pady=5)
        
        hotkey = config['settings']['hotkey']
        self.hotkey_entry = tk.Entry(self.root, font=font_style)
        self.hotkey_entry.insert(0, hotkey)
        self.hotkey_entry.pack(pady=10)

        self.save_hotkey_btn = tk.Button(self.root, text="Save Hotkey", font=font_style, command=self.save_hotkey)
        self.save_hotkey_btn.pack(pady=5)
        
        keyboard.add_hotkey(hotkey, self.toggle_autoclick)

    def set_click_type(self, click_type):
        self.click_type = click_type
        messagebox.showinfo("Click Type Set", f"Click type set to: {click_type}")
    
    def toggle_autoclick(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Stopped")
        else:
            self.running = True
            self.status_label.config(text="Status: Running")
            self.start_clicking()
    
    def start_clicking(self):
        def click():
            while self.running:
                if self.click_type == 'left':
                    pyautogui.click()
                elif self.click_type == 'right':
                    pyautogui.click(button='right')
                time.sleep(0.1)
        
        threading.Thread(target=click).start()
    
    def save_hotkey(self):
        new_hotkey = self.hotkey_entry.get()
        config['settings']['hotkey'] = new_hotkey
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        messagebox.showinfo("Hotkey Saved", f"New hotkey: {new_hotkey}")
        keyboard.add_hotkey(new_hotkey, self.toggle_autoclick)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
