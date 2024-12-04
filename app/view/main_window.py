import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox


class MainWindow(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.pdf_list_wypisy = []
        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        self._create_extracts_section()
        self._create_project_name_section()
        self._create_kind_of_work_section()
        self._create_investor_button()
        self._create_process_button()
        self._configure_drag_and_drop()

    def _create_extracts_section(self):
        self._create_label_and_upload(
            "Przeciągnij i wrzuć 'Wypisy rejestru gruntów'",
            "Wgraj wypisy rejestru gruntów",
            self.upload_wypisy,
        )
        self.wypisy_listbox = self._create_listbox()

    def _create_label_and_upload(self, label_text, button_text, command):
        label = tk.Label(self, text=label_text)
        label.pack(pady=10)
        self.label_wypisy = label
        upload_button = tk.Button(self, text=button_text, command=command)
        upload_button.pack(pady=10)

    def _create_listbox(self):
        listbox = tk.Listbox(self, selectmode=tk.SINGLE, height=8, width=50)
        listbox.pack(pady=10)
        return listbox

    def _create_investor_button(self):
        self.add_investor_btn = tk.Button(self, text="Dodaj inwestora", command=self.add_investor)
        self.add_investor_btn.pack(pady=10)

    def _create_project_name_section(self):
        self._create_labeled_entry("Nazwa projektu:", "project_name_entry")

    def _create_kind_of_work_section(self):
        self._create_labeled_entry("Rodzaj prac:", "type_of_work_entry")

    def _create_labeled_entry(self, label_text, entry_attr_name):
        label = tk.Label(self, text=label_text)
        label.pack(pady=5)
        entry = tk.Entry(self, width=40, justify="center")
        entry.pack(pady=5)
        setattr(self, entry_attr_name, entry)

    def _create_process_button(self):
        self.process_btn = tk.Button(self, text="Generuj oświadczenia", command=self.process_wypisy)
        self.process_btn.pack(pady=10)

    def _configure_drag_and_drop(self):
        self.label_wypisy.drop_target_register(DND_FILES)
        self.label_wypisy.dnd_bind('<<Drop>>', self._handle_drop)

    def upload_wypisy(self):
        self._upload_file()

    def _upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self._add_pdf_to_list(file_path)

    def _handle_drop(self, event):
        file_path = event.data.strip('{}')
        self._add_pdf_to_list(file_path)

    def _add_pdf_to_list(self, file_path):
        if file_path not in self.pdf_list_wypisy:
            self.pdf_list_wypisy.append(file_path)
            file_name = file_path.split('/')[-1]
            self.wypisy_listbox.insert(tk.END, file_name)
        else:
            messagebox.showinfo("Duplicate File", f"{file_path} is already in the list.")

    def process_wypisy(self):
        if not self._validate_inputs():
            return

        directory = filedialog.askdirectory(title="Select a folder to save all documents")
        if not directory:
            messagebox.showerror("Error", "No directory selected.")
            return

        project_name = self.project_name_entry.get()
        type_of_work = self.type_of_work_entry.get()

        for selected_pdf in self.pdf_list_wypisy:
            result = self.controller.process_pdf(selected_pdf, project_name, type_of_work, directory)
            self._handle_process_result(selected_pdf, result, project_name, type_of_work)

    def add_investor(self):
        print("Dodaj inwestora button clicked!")  # Debug

    def _validate_inputs(self):
        if not self.pdf_list_wypisy:
            messagebox.showerror("Error", "No 'Wypisy rejestru gruntów' PDFs available for processing.")
            return False

        if not self.project_name_entry.get() or not self.type_of_work_entry.get():
            messagebox.showerror("Error", "Please fill in both the project name and type of work.")
            return False

        return True

    def _handle_process_result(self, pdf, result, project_name, type_of_work):
        if result:
            messagebox.showinfo(
                "Success",
                f"{pdf} processed successfully with Project: {project_name}, Work Type: {type_of_work}.",
            )
        else:
            messagebox.showerror("Error", f"Failed to process {pdf}.")
