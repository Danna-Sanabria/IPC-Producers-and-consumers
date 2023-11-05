import customtkinter as ctk
import presenter.Presenter as appPresenter


def start_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.geometry("900x600")
    root.title("Hamming calculator")
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    return frame


def clear_fields(frame):
    """Function to clear the content of the widgets."""
    widgets = [
        frame.binary_representation_label,
        frame.bit_matrix_label,
        frame.erroneous_data_label,
        frame.hamming_corrected_label,
        frame.ascii_corrected_label,
        frame.corrected_text_display,
        frame.error_positions_display
    ]
    for widget in widgets:
        widget.configure(text="")


def calculate_prod_cons(frame, buffer_size, producer_number, consumer_number):
    buffer = buffer_size.get()
    producer = producer_number.get()
    consumer = consumer_number.get()
    results = appPresenter(buffer, producer, consumer)
    clear_fields(frame)

    labels_widgets = [
        frame.binary_representation_label,
        frame.bit_matrix_label,
        frame.erroneous_data_label,
        frame.hamming_corrected_label,
        frame.ascii_corrected_label,
        frame.corrected_text_display,
        frame.error_positions_display
    ]

    def update_all_widgets(index=0):
        for i, widget in enumerate(labels_widgets):
            data_list = results[i]
            if index < len(data_list):
                current_text = widget.cget("text")
                new_text = current_text + "\n" + data_list[index] if current_text else data_list[index]
                widget.configure(text=new_text)
        if index < max(len(data) for data in results) - 1:
            frame.after(1000, update_all_widgets, index + 1)

    update_all_widgets()


def app_fields(frame):
    chain_field = ctk.CTkEntry(master=frame, placeholder_text="Please input your chain")
    chain_field.grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky='nsew')

    calculate_button = ctk.CTkButton(master=frame, corner_radius=20, text="Send")
    calculate_button.configure(command=lambda: calculate_prod_cons(frame, chain_field))
    calculate_button.grid(row=1, column=0, columnspan=4, padx=30, pady=30, sticky='nsew')


def start_app(frame):

    # Initialization of the components
    frame.produced_label = ctk.CTkLabel(master=frame, text="")
    frame.buffer_label = ctk.CTkLabel(master=frame, text="")
    frame.error_positions_display = ctk.CTkLabel(master=frame, text="")
    frame.binary_representation_label = ctk.CTkLabel(master=frame, text="")
    frame.erroneous_data_label = ctk.CTkLabel(master=frame, text="")
    frame.hamming_corrected_label = ctk.CTkLabel(master=frame, text="")
    frame.ascii_corrected_label = ctk.CTkLabel(master=frame, text="")

    # Configuration of the layout
    labels = [
        ("Produced:", frame.produced_label),
        ("Buffer:", frame.buffer_label)
    ]

    for index, (label_text, widget) in enumerate(labels):
        label = ctk.CTkLabel(master=frame, text=label_text)

        # Determine the row based on the index
        row = 3 + (index // 4) * 2
        label.grid(row=row, column=index % 4, padx=20, pady=5, sticky='nsew')
        widget.grid(row=row + 1, column=index % 4, padx=20, pady=5, sticky='nsew')

    # Centering the elements using column and row weights
    for i in range(4):  # Assuming 4 columns
        frame.grid_columnconfigure(i, weight=1)


    # Add the new widgets and set their row and column
    buffer_size = ctk.CTkEntry(master=frame, placeholder_text="Buffer Size")
    buffer_size.grid(row=1, column=0, columnspan=1, padx=20, pady=10, sticky='nsew')

    producer_number = ctk.CTkEntry(master=frame, placeholder_text="Producer Number")
    producer_number.grid(row=1, column=1, columnspan=1, padx=20, pady=10, sticky='nsew')

    consumer_number = ctk.CTkEntry(master=frame, placeholder_text="Consumer Number")
    consumer_number.grid(row=1, column=2, columnspan=1, padx=20, pady=10, sticky='nsew')

    calculate_button = ctk.CTkButton(master=frame, corner_radius=20, text="Start simulation")
    calculate_button.configure(command=lambda: calculate_prod_cons(frame, buffer_size,producer_number,consumer_number))
    calculate_button.grid(row=2, column=0, columnspan=3, padx=30, pady=30, sticky='nsew')


def run_app():
    app_frame = start_window()
    start_app(app_frame)
    app_frame.master.mainloop()
