import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE CONFIGURATION ----------------
DB_FILE = "students.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------------- FORM FUNCTIONS ----------------
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    name_entry.focus_set()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    for data in cur.fetchall():
        tree.insert("", tk.END, values=data)
    conn.close()

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if not name or not age or not course:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (student_name, age, course) VALUES (?, ?, ?)",
                    (name, age, course))
        conn.commit()
        conn.close()
        refresh_table()
        clear_fields()
        messagebox.showinfo("Success", "Student Added!")
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not add student: {e}")

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to delete")
        return
    
    item = tree.item(selected[0])
    student_id = item['values'][0]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    refresh_table()

def update_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to update")
        return

    item = tree.item(selected[0])
    student_id = item['values'][0]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET student_name=?, age=?, course=? WHERE id=?",
                (name_entry.get(), age_entry.get(), course_entry.get(), student_id))
    conn.commit()
    conn.close()
    refresh_table()
    clear_fields()

def get_selected(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item['values']
        clear_fields()
        name_entry.insert(0, values[1])
        age_entry.insert(0, values[2])
        course_entry.insert(0, values[3])

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Student Information System")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

init_db()

# HEADER
header = tk.Frame(root, bg="#1e3a8a", height=70)
header.pack(fill="x")
tk.Label(header, text="STUDENT INFORMATION SYSTEM", bg="#1e3a8a", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(header, text="Manage student records easily", bg="#1e3a8a", fg="white", font=("Arial", 9)).pack()

# FORM
form_frame = tk.Frame(root, bg="#eef2ff", padx=20, pady=20)
form_frame.pack(fill="x")

tk.Label(form_frame, text="Student Name:", bg="#eef2ff").grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Age:", bg="#eef2ff").grid(row=1, column=0, sticky="w", pady=5)
age_entry = tk.Entry(form_frame, width=30)
age_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Course:", bg="#eef2ff").grid(row=2, column=0, sticky="w", pady=5)
course_entry = tk.Entry(form_frame, width=30)
course_entry.grid(row=2, column=1, pady=5)

# BUTTONS
btn_frame = tk.Frame(form_frame, bg="#eef2ff")
btn_frame.grid(row=0, column=2, rowspan=3, padx=30)

tk.Button(btn_frame, text="Add Student", bg="#2563eb", fg="white", command=add_student, width=12).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Update", bg="#f59e0b", fg="white", command=update_student, width=8).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", bg="#ef4444", fg="white", command=delete_student, width=8).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Clear", bg="#6b7280", fg="white", command=clear_fields, width=8).grid(row=1, column=1, padx=5)
tk.Button(btn_frame, text="Refresh", bg="#2563eb", fg="white", command=refresh_table, width=8).grid(row=0, column=2, padx=5)

# TABLE
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

tree = ttk.Treeview(table_frame, columns=("ID", "STUDENT NAME", "AGE", "COURSE"), show="headings")
tree.heading("ID", text="ID")
tree.heading("STUDENT NAME", text="STUDENT NAME")
tree.heading("AGE", text="AGE")
tree.heading("COURSE", text="COURSE")
tree.column("ID", width=50)

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", get_selected)

refresh_table()
root.mainloop()
