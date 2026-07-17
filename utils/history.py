import sqlite3
import tkinter as tk
from tkinter import ttk


class HistoryWindow:

    def __init__(self):

        self.conn = sqlite3.connect("detections.db")

    def open(self):

        root = tk.Tk()

        root.title("Detection History")

        root.geometry("850x500")

        tree = ttk.Treeview(

            root,

            columns=("Object", "Confidence", "Time", "Image"),

            show="headings"

        )

        tree.heading("Object", text="Object")

        tree.heading("Confidence", text="Confidence")

        tree.heading("Time", text="Time")

        tree.heading("Image", text="Screenshot")

        tree.column("Object", width=120)

        tree.column("Confidence", width=100)

        tree.column("Time", width=220)

        tree.column("Image", width=350)

        tree.pack(fill="both", expand=True)

        cursor = self.conn.cursor()

        cursor.execute("""

        SELECT

        object_name,

        confidence,

        event_time,

        image_path

        FROM detections

        ORDER BY id DESC

        """)

        rows = cursor.fetchall()

        for row in rows:

            tree.insert("", tk.END, values=row)

        root.mainloop()