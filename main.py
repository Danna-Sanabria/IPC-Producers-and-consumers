# main.py
import tkinter as tk
from tkinter import ttk
from view.app_gui import AppGUI  # Import the AppGUI class

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    app.run_app()