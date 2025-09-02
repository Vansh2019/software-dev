import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ------------------- DATABASE FUNCTIONS -------------------
def connect_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            roll_no TEXT PRIMARY KEY,
            name TEXT,
            course TEXT,
            marks INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_student(roll_no, name, course, marks):
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO student VALUES (?, ?, ?, ?)",
                    (roll_no, name, course, marks))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student Added Successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll No already exists!")

def update_student(roll_no, name, course, marks):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=?, course=?, marks=? WHERE roll_no=?",
                (name, course, marks, roll_no))
    conn.commit()
    if cur.rowcount == 0:
        messagebox.showerror("Error", "Student not found!")
    else:
        messagebox.showinfo("Success", "Student Updated Successfully!")
    conn.close()

def delete_student(roll_no):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE roll_no=?", (roll_no,))
    conn.commit()
    if cur.rowcount == 0:
        messagebox.showerror("Error", "Student not found!")
    else:
        messagebox.showinfo("Success", "Student Deleted Successfully!")
    conn.close()

def fetch_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_student(roll_no):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE roll_no=?", (roll_no,))
    row = cur.fetchone()
    conn.close()
    return row

# ------------------- GUI APPLICATION -------------------
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("700x500")

        # Labels and Entries
        tk.Label(root, text="Roll No").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Course").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(root, text="Marks").grid(row=3, column=0, padx=10, pady=5)

        self.roll_entry = tk.Entry(root)
        self.name_entry = tk.Entry(root)
        self.course_entry = tk.Entry(root)
        self.marks_entry = tk.Entry(root)

        self.roll_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.course_entry.grid(row=2, column=1, padx=10, pady=5)
        self.marks_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Add Student", command=self.add_student).grid(row=4, column=0, pady=10)
        tk.Button(root, text="Update Student", command=self.update_student).grid(row=4, column=1, pady=10)
        tk.Button(root, text="Delete Student", command=self.delete_student).grid(row=5, column=0, pady=10)
        tk.Button(root, text="Search Student", command=self.search_student).grid(row=5, column=1, pady=10)
        tk.Button(root, text="View All", command=self.view_students).grid(row=6, column=0, columnspan=2, pady=10)

        # Treeview for Display
        self.tree = ttk.Treeview(root, columns=("roll_no", "name", "course", "marks"), show="headings")
        self.tree.heading("roll_no", text="Roll No")
        self.tree.heading("name", text="Name")
        self.tree.heading("course", text="Course")
        self.tree.heading("marks", text="Marks")
        self.tree.grid(row=7, column=0, columnspan=3, padx=10, pady=20)

    def add_student(self):
        insert_student(self.roll_entry.get(), self.name_entry.get(),
                       self.course_entry.get(), self.marks_entry.get())
        self.view_students()

    def update_student(self):
        update_student(self.roll_entry.get(), self.name_entry.get(),
                       self.course_entry.get(), self.marks_entry.get())
        self.view_students()

    def delete_student(self):
        delete_student(self.roll_entry.get())
        self.view_students()

    def search_student(self):
        row = search_student(self.roll_entry.get())
        if row:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=row)
        else:
            messagebox.showerror("Error", "Student not found!")

    def view_students(self):
        rows = fetch_students()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)


# ------------------- MAIN PROGRAM -------------------
if __name__ == "__main__":
    connect_db()
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
