import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog

class BookView(ttk.Frame):
    def __init__(self, parent, book_controller) -> None:
        super().__init__(parent)
        self.book_controller = book_controller
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self) -> None:
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        search_button = ttk.Button(search_frame, text="Search", command=self.refresh_books)
        search_button.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_button = ttk.Button(buttons_frame, text="Add Book", command=self.add_book)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        edit_button = ttk.Button(buttons_frame, text="Edit Book", command=self.edit_book)
        edit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = ttk.Button(buttons_frame, text="Delete Book", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT)
        
        # Books table
        self.tree = ttk.Treeview(self, columns=("id", "title", "author", "year", "isbn", "quantity", "available"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("year", text="Year")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("available", text="Available")
        
        self.tree.column("id", width=50)
        self.tree.column("title", width=150)
        self.tree.column("author", width=150)
        self.tree.column("year", width=70)
        self.tree.column("isbn", width=120)
        self.tree.column("quantity", width=70)
        self.tree.column("available", width=70)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_books(self) -> None:
        query = self.search_entry.get()
        books = self.book_controller.search_books(query) if query else self.book_controller.get_all_books()
        
        self.tree.delete(*self.tree.get_children())
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.id,
                book.title,
                book.author,
                book.year,
                book.isbn,
                book.quantity,
                book.available
            ))

    def add_book(self) -> None:
        dialog = BookDialog(self, "Add Book")
        if dialog.result:
            try:
                self.book_controller.add_book(
                    title=dialog.result["title"],
                    author=dialog.result["author"],
                    isbn=dialog.result["isbn"],
                    year=dialog.result["year"],
                    quantity=dialog.result["quantity"]
                )
                self.refresh_books()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def edit_book(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return
            
        book_id = self.tree.item(selected[0])["values"][0]
        book = self.book_controller.get_book(book_id)
        if not book:
            messagebox.showerror("Error", "Book not found")
            return
            
        dialog = BookDialog(
            self, 
            "Edit Book",
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            year=book.year,
            quantity=book.quantity
        )
        
        if dialog.result:
            try:
                self.book_controller.update_book(
                    book_id,
                    title=dialog.result["title"],
                    author=dialog.result["author"],
                    isbn=dialog.result["isbn"],
                    year=dialog.result["year"],
                    quantity=dialog.result["quantity"]
                )
                self.refresh_books()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
            
        book_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            try:
                if self.book_controller.delete_book(book_id):
                    self.refresh_books()
                else:
                    messagebox.showerror("Error", "Failed to delete book")
            except Exception as e:
                messagebox.showerror("Error", str(e))

class BookDialog(Dialog):
    def __init__(self, parent, dialog_title, title="", author="", isbn="", year=0, quantity=1):
        self.result = None
        self._title = title
        self._author = author
        self._isbn = isbn
        self._year = year
        self._quantity = quantity
        super().__init__(parent, dialog_title)
        
    def body(self, master):
        ttk.Label(master, text="Title:").grid(row=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Author:").grid(row=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="ISBN:").grid(row=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Year:").grid(row=3, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Quantity:").grid(row=4, sticky=tk.W, padx=5, pady=5)
        
        self.title_entry = ttk.Entry(master)
        self.author_entry = ttk.Entry(master)
        self.isbn_entry = ttk.Entry(master)
        self.year_entry = ttk.Entry(master)
        self.quantity_entry = ttk.Entry(master)
        
        self.title_entry.insert(0, self._title)
        self.author_entry.insert(0, self._author)
        self.isbn_entry.insert(0, self._isbn)
        self.year_entry.insert(0, str(self._year))
        self.quantity_entry.insert(0, str(self._quantity))
        
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.author_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        self.isbn_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        self.year_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        self.quantity_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)
        
        return self.title_entry  # initial focus
    
    def validate(self):
        try:
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            isbn = self.isbn_entry.get().strip()
            year = int(self.year_entry.get())
            quantity = int(self.quantity_entry.get())
            
            if not title or not author or not isbn:
                raise ValueError("All fields are required")
            if year <= 0 or quantity <= 0:
                raise ValueError("Year and quantity must be positive numbers")
                
            self.result = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "year": year,
                "quantity": quantity
            }
            return True
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def apply(self):
        pass