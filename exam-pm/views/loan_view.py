import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog
from datetime import datetime, timedelta

class LoanView(ttk.Frame):
    def __init__(self, parent, loan_controller, book_controller, reader_controller) -> None:
        super().__init__(parent)
        self.loan_controller = loan_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_loans()

    def create_widgets(self) -> None:
        # Filter frame
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar()
        self.filter_var.set("all")
        
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", command=self.refresh_loans).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(filter_frame, text="Active", variable=self.filter_var, value="active", command=self.refresh_loans).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(filter_frame, text="Overdue", variable=self.filter_var, value="overdue", command=self.refresh_loans).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(filter_frame, text="Returned", variable=self.filter_var, value="returned", command=self.refresh_loans).pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_button = ttk.Button(buttons_frame, text="Create Loan", command=self.create_loan)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        return_button = ttk.Button(buttons_frame, text="Return Book", command=self.return_selected)
        return_button.pack(side=tk.LEFT)
        
        # Loans table
        self.tree = ttk.Treeview(self, columns=("id", "book_id", "reader_id", "loan_date", "return_date", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("book_id", text="Book ID")
        self.tree.heading("reader_id", text="Reader ID")
        self.tree.heading("loan_date", text="Loan Date")
        self.tree.heading("return_date", text="Return Date")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("book_id", width=70)
        self.tree.column("reader_id", width=70)
        self.tree.column("loan_date", width=150)
        self.tree.column("return_date", width=150)
        self.tree.column("status", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_loans(self) -> None:
        filter_type = self.filter_var.get()
        
        if filter_type == "all":
            loans = self.loan_controller.get_all_loans()
        elif filter_type == "active":
            loans = [loan for loan in self.loan_controller.get_all_loans() if not loan.is_returned]
        elif filter_type == "overdue":
            loans = self.loan_controller.get_overdue_loans()
        elif filter_type == "returned":
            loans = [loan for loan in self.loan_controller.get_all_loans() if loan.is_returned]
        
        self.tree.delete(*self.tree.get_children())
        for loan in loans:
            status = "Returned" if loan.is_returned else "Overdue" if loan.is_overdue() else "Active"
            self.tree.insert("", tk.END, values=(
                loan.id,
                loan.book_id,
                loan.reader_id,
                loan.loan_date.strftime("%Y-%m-%d %H:%M:%S"),
                loan.return_date.strftime("%Y-%m-%d %H:%M:%S"),
                status
            ))

    def create_loan(self) -> None:
        dialog = LoanDialog(self, "Create Loan", self.book_controller, self.reader_controller)
        if dialog.result:
            try:
                self.loan_controller.create_loan(
                    book_id=dialog.result["book_id"],
                    reader_id=dialog.result["reader_id"],
                    loan_date=dialog.result["loan_date"],
                    return_date=dialog.result["return_date"]
                )
                # Update book availability
                self.book_controller.borrow_book(dialog.result["book_id"])
                self.refresh_loans()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def return_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a loan to return")
            return
            
        loan_id = self.tree.item(selected[0])["values"][0]
        loan = self.loan_controller.get_loan(loan_id)
        if not loan:
            messagebox.showerror("Error", "Loan not found")
            return
            
        if loan.is_returned:
            messagebox.showinfo("Info", "This book has already been returned")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to mark this book as returned?"):
            try:
                if self.loan_controller.return_book(loan_id):
                    # Update book availability
                    self.book_controller.return_book(loan.book_id)
                    self.refresh_loans()
                else:
                    messagebox.showerror("Error", "Failed to return book")
            except Exception as e:
                messagebox.showerror("Error", str(e))

class LoanDialog(Dialog):
    def __init__(self, parent, title, book_controller, reader_controller):
        self.result = None
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        super().__init__(parent, title)
        
    def body(self, master):
        ttk.Label(master, text="Book:").grid(row=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Reader:").grid(row=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Loan Date:").grid(row=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Return Date:").grid(row=3, sticky=tk.W, padx=5, pady=5)
        
        # Book combobox
        self.book_var = tk.StringVar()
        self.book_combobox = ttk.Combobox(master, textvariable=self.book_var, state="readonly")
        self.book_combobox.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Populate books
        books = self.book_controller.get_all_books()
        available_books = [book for book in books if book.is_available()]
        book_options = [f"{book.id}: {book.title} by {book.author}" for book in available_books]
        self.book_combobox["values"] = book_options
        if book_options:
            self.book_combobox.current(0)
        
        # Reader combobox
        self.reader_var = tk.StringVar()
        self.reader_combobox = ttk.Combobox(master, textvariable=self.reader_var, state="readonly")
        self.reader_combobox.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Populate readers
        readers = self.reader_controller.get_all_readers()
        reader_options = [f"{reader.id}: {reader.name}" for reader in readers]
        self.reader_combobox["values"] = reader_options
        if reader_options:
            self.reader_combobox.current(0)
        
        # Loan date (default today)
        self.loan_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(master, textvariable=self.loan_date_var).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Return date (default 2 weeks from today)
        self.return_date_var = tk.StringVar(value=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        ttk.Entry(master, textvariable=self.return_date_var).grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        return self.book_combobox  # initial focus
    
    def validate(self):
        try:
            # Get book ID
            book_text = self.book_var.get()
            if not book_text:
                raise ValueError("Please select a book")
            book_id = int(book_text.split(":")[0])
            
            # Get reader ID
            reader_text = self.reader_var.get()
            if not reader_text:
                raise ValueError("Please select a reader")
            reader_id = int(reader_text.split(":")[0])
            
            # Parse dates
            loan_date = datetime.strptime(self.loan_date_var.get(), "%Y-%m-%d")
            return_date = datetime.strptime(self.return_date_var.get(), "%Y-%m-%d")
            
            if return_date <= loan_date:
                raise ValueError("Return date must be after loan date")
                
            self.result = {
                "book_id": book_id,
                "reader_id": reader_id,
                "loan_date": loan_date,
                "return_date": return_date
            }
            return True
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def apply(self):
        pass