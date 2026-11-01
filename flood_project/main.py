#Dashboard | View Reports | Admin Login | Admin Panel

import tkinter as tk
from tkinter import ttk, messagebox

from manager import FloodManager
from models import SEVERITY_LEVELS
from auth import check_login

# Tuple: form er label ar table er column
LABELS = ("Report ID", "District", "Date (YYYY-MM-DD)",
          "Water Level (m)", "Affected People", "Houses Damaged")
COLUMNS = ("ID", "District", "Date", "Water Level",
           "Affected", "Houses", "Severity")


class FloodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flood Report Analysis System")
        self.root.geometry("1100x650")

        self.manager = FloodManager()   # data ar hishab-er kaj eta kore
        self.is_admin = False           # login kora ache kina
        self.entries = []               # form er input box gulo
        self.table = None
        self.search_entry = None
        self.user_entry = None
        self.pass_entry = None

        self.make_sidebar()
        self.content = tk.Frame(self.root)      # page ekhane dekhabe
        self.content.pack(side="right", fill="both", expand=True)
        self.show_dashboard()

    # ---------- Sidebar (baam er button) ----------
    def make_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#0d47a1")
        sidebar.pack(side="left", fill="y")
        tk.Label(sidebar, text="FLOOD REPORT\nSYSTEM", bg="#0d47a1", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=20, padx=10)
        tk.Button(sidebar, text="Dashboard", width=18, command=self.show_dashboard).pack(pady=5, padx=10)
        tk.Button(sidebar, text="View Reports", width=18, command=self.show_reports).pack(pady=5, padx=10)
        tk.Button(sidebar, text="Admin Login", width=18, command=self.open_admin).pack(pady=5, padx=10)
        tk.Button(sidebar, text="Logout", width=18, command=self.logout).pack(pady=5, padx=10)
        tk.Button(sidebar, text="Exit", width=18, command=self.root.destroy).pack(pady=5, padx=10)

    def clear_page(self):
        #Purano page er shob jinish muche felo.
        for widget in self.content.winfo_children():
            widget.destroy()

    #Dashboard
    def show_dashboard(self):
        self.clear_page()
        tk.Label(self.content, text="Flood Report Analysis - Overview",
                 font=("Arial", 20, "bold")).pack(pady=15)

        data = self.manager.analyze()
        if data is None:
            tk.Label(self.content, font=("Arial", 13), fg="gray",
                     text="There is not any available data.").pack(pady=60)
            return

        row = tk.Frame(self.content)
        row.pack(pady=10)

        # Box 1: Summary
        box1 = tk.LabelFrame(row, text="Summary", padx=20, pady=10)
        box1.pack(side="left", padx=15, anchor="n")
        tk.Label(box1, text="Total Reports: " + str(data["total_reports"])).pack(anchor="w")
        tk.Label(box1, text="Average Water Level: " + format(data["avg_level"], ".2f") + " m").pack(anchor="w")
        tk.Label(box1, text="Maximum Water Level: " + format(data["max_level"], ".2f") + " m").pack(anchor="w")
        tk.Label(box1, text="Total Affected People: " + str(data["total_affected"])).pack(anchor="w")
        tk.Label(box1, text="Total Houses Damaged: " + str(data["total_houses"])).pack(anchor="w")
        tk.Label(box1, text="Most Affected District: " + data["worst_district"]).pack(anchor="w")

        # Box 2: Severity count
        box2 = tk.LabelFrame(row, text="Reports by Severity", padx=20, pady=10)
        box2.pack(side="left", padx=15, anchor="n")
        for level in SEVERITY_LEVELS:
            if level in data["severity_count"]:
                count = data["severity_count"][level]
            else:
                count = 0
            tk.Label(box2, text=level + " : " + str(count)).pack(anchor="w")

        # Box 3: District wise affected people
        box3 = tk.LabelFrame(row, text="Affected People by District", padx=20, pady=10)
        box3.pack(side="left", padx=15, anchor="n")
        for district in data["district_totals"]:
            tk.Label(box3, text=district + " : " + str(data["district_totals"][district])).pack(anchor="w")

    #Page 2: View Reports
    def show_reports(self):
        self.clear_page()
        tk.Label(self.content, text="All Flood Reports", font=("Arial", 18, "bold")).pack(pady=10)

        bar = tk.Frame(self.content)
        bar.pack(pady=5)
        tk.Label(bar, text="Search District:").pack(side="left")
        self.search_entry = tk.Entry(bar, width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(bar, text="Search", command=self.search).pack(side="left", padx=3)
        tk.Button(bar, text="Show All", command=self.show_all).pack(side="left", padx=3)

        self.build_table(self.content)
        self.refresh_table(self.manager.reports)

    #Login
    def open_admin(self):
        if self.is_admin:
            self.show_admin_panel()
        else:
            self.show_login()

    def show_login(self):
        self.clear_page()
        box = tk.LabelFrame(self.content, text="Director / Admin Login", padx=30, pady=20)
        box.pack(pady=100)
        tk.Label(box, text="Username").pack(anchor="w")
        self.user_entry = tk.Entry(box, width=30)
        self.user_entry.pack(pady=5)
        tk.Label(box, text="Password").pack(anchor="w")
        self.pass_entry = tk.Entry(box, width=30, show="*")
        self.pass_entry.pack(pady=5)
        tk.Button(box, text="Login", width=15, command=self.login).pack(pady=12)

    def login(self):
        try:
            ok = check_login(self.user_entry.get(), self.pass_entry.get())
        except ValueError as error:
            messagebox.showwarning("Warning", str(error))
            return

        if ok:
            self.is_admin = True
            messagebox.showinfo("Welcome", "Login successful!")
            self.show_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Username and Password wrong.")

    def logout(self):
        if not self.is_admin:
            messagebox.showinfo("Info", "Apni login kora nai.")
            return
        self.is_admin = False
        self.show_dashboard()

    #Page 4: Admin Panel (add / update / delete)
    def show_admin_panel(self):
        if not self.is_admin:      
            self.show_login()
            return

        self.clear_page()
        tk.Label(self.content, text="Admin Panel - Manage Reports",
                 font=("Arial", 18, "bold")).pack(pady=10)

        main_row = tk.Frame(self.content)
        main_row.pack(fill="both", expand=True, padx=10)

        #form
        form = tk.LabelFrame(main_row, text="Flood Report Form", padx=10, pady=10)
        form.pack(side="left", anchor="n")

        self.entries = []
        for label in LABELS:
            tk.Label(form, text=label).pack(anchor="w")
            entry = tk.Entry(form, width=25)
            entry.pack(pady=2)
            self.entries.append(entry)

        tk.Button(form, text="Add", width=15, command=self.add_report).pack(pady=3)
        tk.Button(form, text="Update", width=15, command=self.update_report).pack(pady=3)
        tk.Button(form, text="Delete", width=15, command=self.delete_report).pack(pady=3)
        tk.Button(form, text="Clear Form", width=15, command=self.clear_form).pack(pady=3)

        #table
        table_box = tk.Frame(main_row)
        table_box.pack(side="left", fill="both", expand=True, padx=10)
        self.build_table(table_box)
        self.table.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh_table(self.manager.reports)

    #Table er kaj
    def build_table(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.table = ttk.Treeview(frame, columns=COLUMNS, show="headings")
        for col in COLUMNS:
            self.table.heading(col, text=col)
            self.table.column(col, width=90, anchor="center")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_table(self, reports):
        
        for item in self.table.get_children():
            self.table.delete(item)
        for report in reports:
            self.table.insert("", tk.END, values=report.to_row())

    def on_select(self, event):
        #Table e row click korle form e data cole ashe.
        selected = self.table.selection()
        if not selected:
            return
        values = self.table.item(selected[0])["values"]
        self.clear_form()
        for i in range(len(self.entries)):
            self.entries[i].insert(0, str(values[i]))

    #Form er kaj
    def get_form_values(self):
        values = []
        for entry in self.entries:
            values.append(entry.get())
        return values

    def clear_form(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    #Button er kaj
    def add_report(self):
        v = self.get_form_values()
        try:
            self.manager.add_report(v[0], v[1], v[2], v[3], v[4], v[5])
            self.refresh_table(self.manager.reports)
            self.clear_form()
            messagebox.showinfo("success","Report added Successfully ")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))

    def update_report(self):
        v = self.get_form_values()
        try:
            self.manager.update_report(v[0], v[1], v[2], v[3], v[4], v[5])
            self.refresh_table(self.manager.reports)
            messagebox.showinfo("Success", "Report update hoyeche!")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def delete_report(self):
        report_id = self.entries[0].get().strip()
        if report_id == "":
            messagebox.showwarning("Warning", "Select a row from the table.")
            return
        if not messagebox.askyesno("Confirm", report_id + " want to delete ?"):
            return
        try:
            self.manager.delete_report(report_id)
            self.refresh_table(self.manager.reports)
            self.clear_form()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def search(self):
        text = self.search_entry.get()
        if text.strip() == "":
            messagebox.showwarning("Warning", "Please enter district name.")
            return
        results = self.manager.search_by_district(text)
        self.refresh_table(results)
        if len(results) == 0:
            messagebox.showinfo("There is no report.")

    def show_all(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_table(self.manager.reports)


def main():
    root = tk.Tk()
    FloodApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
