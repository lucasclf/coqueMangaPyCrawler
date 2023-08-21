import logging.config
import time
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from config.config_manga_crawler import ConfigMangaCrawler
from enums.output_format_enum import OutputFormatEnum

logging.config.fileConfig("./config/logging_config.ini")
logger = logging.getLogger('cqnLogger')


class ConfigurationUI:
    def __init__(self):
        self.process_button = None
        self.destiny_button = None
        self.json_button = None
        self.root = tk.Tk()
        self.root.title("Configurações do Manga Crawler")

        self.json_path_var = tk.StringVar()
        self.destiny_path_var = tk.StringVar()

        self.output_format_var = tk.StringVar(value=OutputFormatEnum.CBZ.value)

        self.create_widgets()

        self.should_terminate = False

        self.log_text = tk.Text(self.root, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_widgets(self):
        tk.Label(self.root, text="Configurações do Manga Crawler", font=("Helvetica", 16)).pack(pady=10)

        self.json_button = self.create_input("Caminho do JSON:", self.json_path_var, "Selecionar Arquivo JSON",
                                             self.choose_json_file)

        self.destiny_button = self.create_input("Pasta de destino:", self.destiny_path_var,
                                                "Selecionar Pasta de Destino", self.choose_destiny_folder)

        self.process_button = tk.Button(self.root, text="Iniciar processo", command=self.toggle_process)
        self.process_button.pack(pady=20)

        self.create_radio("Escolha o formato de saída do manga:",
                          [OutputFormatEnum.CBZ, OutputFormatEnum.IMAGE], OutputFormatEnum.CBZ)

    def create_input(self, label_text, variable, button_text, command):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text=label_text).pack(side="left", padx=5)
        tk.Entry(frame, textvariable=variable, state=tk.DISABLED).pack(side="left", padx=5, expand=True, fill="x")
        button = tk.Button(frame, text=button_text, command=command)
        button.pack(side="left", padx=5)

        return button

    def choose_json_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Arquivo JSON",
            filetypes=[("JSON Files", "*.json")]
        )
        self.json_path_var.set(file_path)

    def choose_destiny_folder(self):
        folder_path = filedialog.askdirectory(title="Selecionar Pasta de Destino")
        self.destiny_path_var.set(folder_path)

    def create_radio(self, label_text, options, default_value):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text=label_text).pack(side="left", padx=5)

        for option in options:
            ttk.Radiobutton(frame, text=option.name, variable=self.output_format_var,
                            value=option.value, command=self.change_output_format).pack(side="left")

    def change_output_format(self):
        selected_option = self.output_format_var.get()
        ConfigMangaCrawler.output_format = selected_option
        logger.info(f"Formato de saída alterado para: {ConfigMangaCrawler.output_format}")

    def toggle_process(self):
        if self.process_button["text"] == "Iniciar processo":
            ConfigMangaCrawler.json_path = self.json_path_var.get()
            ConfigMangaCrawler.destiny_path = self.destiny_path_var.get()

            self.json_button.config(state=tk.DISABLED)
            self.destiny_button.config(state=tk.DISABLED)

            self.process_button["text"] = "Encerrar processo"
            self.process_button["command"] = self.confirm_end_process
        else:
            self.confirm_end_process()

    def confirm_end_process(self):
        confirmed = messagebox.askyesno("Encerrar Processo", "Deseja encerrar o processo?")
        if confirmed:
            self.should_terminate = True
            ConfigMangaCrawler.script_is_ending = True
            while ConfigMangaCrawler.script_is_ending:
                logger.info(f"Encerrado? {ConfigMangaCrawler.script_is_ending}")
                time.sleep(1)

            self.root.destroy()


if __name__ == "__main__":
    config_ui = ConfigurationUI()
    config_ui.root.mainloop()
