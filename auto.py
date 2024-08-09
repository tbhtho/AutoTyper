import pygetwindow as gw
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import threading
import keyboard
import sys

# Global variable to control the typing loop
stop_typing = True

# Global variable for custom click position
custom_position = None

# Function to calculate the center of the screen
def get_screen_center():
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    return center_x, center_y

# Function to find and focus the window
def focus_window(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.activate()  # Focus the window
        time.sleep(0.2)  # Short delay to ensure focus
    else:
        messagebox.showerror("Error", f'Window "{window_title}" not found.')

# Function to select custom click position
def select_click_position():
    global custom_position
    messagebox.showinfo("Info", "Move your mouse to the desired position and press 'S' to select.")
    while True:
        if keyboard.is_pressed('s'):
            custom_position = pyautogui.position()
            messagebox.showinfo("Position Selected", f"Selected position: {custom_position}")
            break
        time.sleep(0.1)

# Function to type, enter, and clear text
def type_and_clear(name, line_number):
    global custom_position
    print(f"Processing line {line_number}: {name}")  # Print the current line number and name
    if custom_position:
        pyautogui.click(custom_position)
    else:
        center_x, center_y = get_screen_center()
        pyautogui.click(center_x, center_y)
    time.sleep(0.15)  # Reduced delay for quicker response
    
    pyautogui.typewrite(name, interval=0.05)  # Fast but readable typing speed
    pyautogui.press('enter')
    time.sleep(0.2)  # Slight delay after pressing enter
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.2)  # Slight delay before moving to the next action

# Function to start the process
def start_typing():
    global stop_typing, custom_position
    stop_typing = False
    
    file_path = file_path_entry.get()
    keybind = keybind_combo.get()
    window_title = window_title_entry.get()

    if not file_path or not keybind or not window_title:
        messagebox.showwarning("Warning", "Please enter a file path, window title, and select a keybind.")
        return

    # Focus the window
    focus_window(window_title)

    # Read the names from the file
    try:
        with open(file_path, 'r') as file:
            names = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please check the file path.")
        return

    keyboard.add_hotkey(keybind, toggle_typing)

    messagebox.showinfo("Info", f"Press '{keybind}' to start or stop typing.")
    while True:
        if not stop_typing:
            for line_number, name in enumerate(names, start=1):  # Enumerate to get line numbers
                if stop_typing:
                    break
                name = name.strip()
                type_and_clear(name, line_number)
                time.sleep(0.25)  # Adjusted delay before moving to the next name
        time.sleep(0.05)

    messagebox.showinfo("Done", "Typing process completed or stopped.")

# Function to toggle the typing process
def toggle_typing():
    global stop_typing
    stop_typing = not stop_typing
    if stop_typing:
        print("Typing process stopped.")
    else:
        print("Typing process started.")

# Function to browse and select a file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

# Function to exit the program
def exit_program():
    global stop_typing
    stop_typing = True
    sys.exit()

# Create the main window
root = tk.Tk()
root.title("Auto Typer")

# Create labels and entries
tk.Label(root, text="File Path:").grid(row=0, column=0, padx=10, pady=5)
file_path_entry = tk.Entry(root, width=40)
file_path_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Window Title:").grid(row=1, column=0, padx=10, pady=5)
window_title_entry = tk.Entry(root, width=40)
window_title_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Keybind:").grid(row=2, column=0, padx=10, pady=5)
keybind_combo = ttk.Combobox(root, values=["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"], state="readonly", width=37)
keybind_combo.grid(row=2, column=1, padx=10, pady=5)
keybind_combo.set("F1")  # Default value

# Create a browse button
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=5)

# Create a button to select custom position
select_position_button = tk.Button(root, text="Select Position", command=select_click_position)
select_position_button.grid(row=3, column=0, padx=10, pady=10)

# Create a start button
start_button = tk.Button(root, text="Start Typing", command=lambda: threading.Thread(target=start_typing).start())
start_button.grid(row=3, column=1, padx=10, pady=10)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.grid(row=4, column=1, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
