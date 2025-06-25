import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog

class ReaderView(ttk.Frame):
    def __init__(self, parent, reader_controller) -> None:
        super().__init__(parent)
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_readers()

    def create_widgets(self) -> None:
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        search_button = ttk.Button(search_frame, text="Search", command=self.refresh_readers)
        search_button.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_button = ttk.Button(buttons_frame, text="Add Reader", command=self.add_reader)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        edit_button = ttk.Button(buttons_frame, text="Edit Reader", command=self.edit_reader)
        edit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = ttk.Button(buttons_frame, text="Delete Reader", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT)
        
        # Readers table
        self.tree = ttk.Treeview(self, columns=("id", "name", "email", "phone", "registration_date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("registration_date", text="Registration Date")
        
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("email", width=200)
        self.tree.column("phone", width=120)
        self.tree.column("registration_date", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_readers(self) -> None:
        query = self.search_entry.get()
        readers = self.reader_controller.get_all_readers()
        
        # Filter by query if provided
        if query:
            query = query.lower()
            readers = [
                r for r in readers 
                if query in r.name.lower() 
                or query in r.email.lower() 
                or query in r.phone.lower()
            ]
        
        self.tree.delete(*self.tree.get_children())
        for reader in readers:
            self.tree.insert("", tk.END, values=(
                reader.id,
                reader.name,
                reader.email,
                reader.phone,
                reader.registration_date.strftime("%Y-%m-%d %H:%M:%S")
            ))

    def add_reader(self) -> None:
        dialog = ReaderDialog(self, "Add Reader")
        if dialog.result:
            try:
                self.reader_controller.add_reader(
                    name=dialog.result["name"],
                    email=dialog.result["email"],
                    phone=dialog.result["phone"]
                )
                self.refresh_readers()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def edit_reader(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reader to edit")
            return
            
        reader_id = self.tree.item(selected[0])["values"][0]
        reader = self.reader_controller.get_reader(reader_id)
        if not reader:
            messagebox.showerror("Error", "Reader not found")
            return
            
        dialog = ReaderDialog(
            self, 
            "Edit Reader",
            name=reader.name,
            email=reader.email,
            phone=reader.phone
        )
        
        if dialog.result:
            try:
                self.reader_controller.update_reader(
                    reader_id,
                    name=dialog.result["name"],
                    email=dialog.result["email"],
                    phone=dialog.result["phone"]
                )
                self.refresh_readers()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reader to delete")
            return
            
        reader_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this reader?"):
            try:
                if self.reader_controller.delete_reader(reader_id):
                    self.refresh_readers()
                else:
                    messagebox.showerror("Error", "Failed to delete reader")
            except Exception as e:
                messagebox.showerror("Error", str(e))

class ReaderDialog(Dialog):
    def __init__(self, parent, title, name="", email="", phone=""):
        self.result = None
        self._name = name
        self._email = email
        self._phone = phone
        super().__init__(parent, title)
        
    def body(self, master):
        ttk.Label(master, text="Name:").grid(row=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Email:").grid(row=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(master, text="Phone:").grid(row=2, sticky=tk.W, padx=5, pady=5)
        
        self.name_entry = ttk.Entry(master)
        self.email_entry = ttk.Entry(master)
        self.phone_entry = ttk.Entry(master)
        
        self.name_entry.insert(0, self._name)
        self.email_entry.insert(0, self._email)
        self.phone_entry.insert(0, self._phone)
        
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.email_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        self.phone_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        return self.name_entry  # initial focus
    
    def validate(self):
        try:
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()
            
            if not name or not email or not phone:
                raise ValueError("All fields are required")
                
            self.result = {
                "name": name,
                "email": email,
                "phone": phone
            }
            return True
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def apply(self):
        pass