import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller) -> None:
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.loan_controller = loan_controller
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.book_tab = BookView(self.notebook, self.book_controller)
        self.reader_tab = ReaderView(self.notebook, self.reader_controller)
        self.loan_tab = LoanView(self.notebook, self.loan_controller, self.book_controller, self.reader_controller)
        
        # Add tabs to notebook
        self.notebook.add(self.book_tab, text="Books")
        self.notebook.add(self.reader_tab, text="Readers")
        self.notebook.add(self.loan_tab, text="Loans")