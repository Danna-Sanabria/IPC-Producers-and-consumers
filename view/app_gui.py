import tkinter as tk
from random import random
from tkinter import ttk
import threading
import random
import time
from model.limited_buffer import LimitedBuffer
from view.validator import validate_numeric


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x600")
        self.root.title("Simulación de Productores y Consumidores")

        self.style = ttk.Style()
        self.style.configure('TLabel', background='#E0E0E0')
        self.style.configure('TButton', background='#4CAF50', foreground='black')

        self.frame = tk.Frame(master=self.root, bg="#E0E0E0")
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create a label to fill the width of the window
        self.blank_label = ttk.Label(self.frame, text="")
        self.blank_label.grid(row=0, column=0, columnspan=3)  # Span all 3 columns

        self.buffer_size_label = ttk.Label(self.frame, text="Tamaño del Búfer:")
        self.buffer_size_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.buffer_size_entry = ttk.Entry(self.frame)
        self.buffer_size_entry.grid(row=1, column=1, padx=10, pady=10,
                                    sticky="ew")  # Use "ew" to make it fill horizontally

        self.producer_label = ttk.Label(self.frame, text="Número de Productores:")
        self.producer_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.producer_entry = ttk.Entry(self.frame)
        self.producer_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.consumer_label = ttk.Label(self.frame, text="Número de Consumidores:")
        self.consumer_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.consumer_entry = ttk.Entry(self.frame)
        self.consumer_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Adjust the labels and buttons
        self.start_simulation_button = ttk.Button(self.frame, text="Start Simulation", command=self.start_simulation)
        self.start_simulation_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.stop_simulation_button = ttk.Button(self.frame, text="Stop Simulation", command=self.stop_simulation,
                                                 state=tk.DISABLED)
        self.stop_simulation_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.grid(row=6, column=3, rowspan=5, padx=5, pady=5, sticky="nsw")

        self.binary_representation_label = tk.Listbox(self.frame, yscrollcommand=self.scrollbar.set,
                                                      selectbackground="#4CAF50", selectmode=tk.SINGLE,
                                                      background="#E0E0E0")
        self.binary_representation_label.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        self.scrollbar.config(command=self.binary_representation_label.yview)

        self.stats_label = ttk.Label(self.frame, text="", font=("Helvetica", 12))
        self.stats_label.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.buffer = None
        self.running = [False]
        self.producer_times = []
        self.consumer_times = []

    def start_simulation(self):
        if not self.running[0]:
            self.binary_representation_label.delete(0, tk.END)
            self.start_simulation_button.config(state=tk.DISABLED)
            self.stop_simulation_button.config(state=tk.NORMAL)
            self.running[0] = True
            buffer_size = int(self.buffer_size_entry.get())
            num_producers = int(self.producer_entry.get())
            num_consumers = int(self.consumer_entry.get())

            self.buffer = LimitedBuffer(buffer_size)

            # Pasamos la variable compartida "running" a los hilos
            for _ in range(num_producers):
                threading.Thread(target=self.producer, args=(self.buffer, self.running)).start()

            for _ in range(num_consumers):
                threading.Thread(target=self.consumer, args=(self.buffer, self.running)).start()

            self.update_labels()

    def stop_simulation(self):
        if self.running[0]:
            self.running[0] = False  # Detenemos los hilos estableciendo la variable compartida a False
            self.start_simulation_button.config(state=tk.NORMAL)
            self.stop_simulation_button.config(state=tk.DISABLED)
            self.calculate_statistics()  # Calcula las estadísticas cuando se detiene la simulación
            self.update_statistics_label()  # Actualiza la etiqueta de estadísticas

    def producer(self, buffer, running):
        while running[0]:
            start_time = time.time()  # Registra el tiempo de inicio
            item = random.randint(1, 100)
            buffer.add(item)
            time.sleep(random.random())
            end_time = time.time()  # Registra el tiempo de finalización
            self.producer_times.append(end_time - start_time)

    def consumer(self, buffer, running):
        while running[0]:
            start_time = time.time()  # Registra el tiempo de inicio
            buffer.remove()
            time.sleep(random.random())
            end_time = time.time()  # Registra el tiempo de finalización
            self.consumer_times.append(end_time - start_time)

    def calculate_statistics(self):
        # Calcula estadísticas sobre los tiempos de producción y consumo
        self.max_producer_time = max(self.producer_times)
        self.min_producer_time = min(self.producer_times)
        self.avg_producer_time = sum(self.producer_times) / len(self.producer_times) if self.producer_times else 0

        self.max_consumer_time = max(self.consumer_times)
        self.min_consumer_time = min(self.consumer_times)
        self.avg_consumer_time = sum(self.consumer_times) / len(self.consumer_times) if self.consumer_times else 0

    def update_statistics_label(self):
        # Actualiza la etiqueta de estadísticas
        stats_text = "Estadísticas:\n"
        stats_text += f"Tiempo máximo de producción: {self.max_producer_time:.2f} segundos\n"
        stats_text += f"Tiempo mínimo de producción: {self.min_producer_time:.2f} segundos\n"
        stats_text += f"Tiempo promedio de producción: {self.avg_producer_time:.2f} segundos\n\n"
        stats_text += f"Tiempo máximo de consumo: {self.max_consumer_time:.2f} segundos\n"
        stats_text += f"Tiempo mínimo de consumo: {self.min_consumer_time:.2f} segundos\n"
        stats_text += f"Tiempo promedio de consumo: {self.avg_consumer_time:.2f} segundos"

        self.stats_label.config(text=stats_text)

    def update_labels(self):
        if self.buffer is not None:
            while self.buffer.event_log:
                event = self.buffer.event_log.pop(0)
                self.binary_representation_label.insert(tk.END, event)
        if self.running[0]:
            self.root.after(1000, self.update_labels)  # Solo actualizamos si la simulación está en marcha

    def run_app(self):
        self.root.mainloop()