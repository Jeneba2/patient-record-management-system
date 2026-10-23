import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ============================================================
# MODEL CLASSES (OOP Core)
# ============================================================
class Patient:
    """
    Represents a patient record.
    Privacy-respecting: stores only a name, system-generated patient code,
    and non-sensitive health data (no national ID, address, or contact info).
    """

    _total_patients = 0  # Class-level attribute

    def __init__(self, patient_code: str, name: str, age: int,
                 gender: str, condition: str = "Unknown"):
        self.patient_code = patient_code
        self.name = name
        self.age = age
        self.gender = gender
        self.condition = condition
        self.records = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        Patient._total_patients += 1

    # ---------- Instance methods ----------
    def update_record(self, note: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records.append(f"[{timestamp}] {note}")
        self.updated_at = datetime.now()

    def update_info(self, name: str = None, age: int = None,
                    gender: str = None, condition: str = None) -> None:
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if gender is not None:
            self.gender = gender
        if condition is not None:
            self.condition = condition
        self.updated_at = datetime.now()

    def display_info(self) -> str:
        return (
            f"Patient Code : {self.patient_code}\n"
            f"Name         : {self.name}\n"
            f"Age          : {self.age}\n"
            f"Gender       : {self.gender}\n"
            f"Condition    : {self.condition}\n"
            f"Created      : {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Last Updated : {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Records      : {len(self.records)} visit(s)"
        )

    # ---------- Class method ----------
    @classmethod
    def get_total_patients(cls) -> int:
        return cls._total_patients

    # ---------- Static method ----------
    @staticmethod
    def validate_patient_code(code: str) -> bool:
        if not isinstance(code, str) or len(code) != 6:
            return False
        if not code.startswith("P-"):
            return False
        return code[2:].isdigit()

    def __str__(self) -> str:
        return (f"Patient({self.patient_code}, name='{self.name}', "
                f"age={self.age}, condition='{self.condition}')")


class PatientRegistry:
    """Manages a dictionary of Patient objects keyed by patient_code."""

    def __init__(self):
        self._patients = {}

    def add_patient(self, patient: Patient) -> bool:
        if patient.patient_code in self._patients:
            return False
        self._patients[patient.patient_code] = patient
        return True

    def get_patient(self, code: str):
        return self._patients.get(code)

    def get_all(self):
        return list(self._patients.values())

    def get_count(self) -> int:
        return len(self._patients)

    def remove_patient(self, code: str) -> bool:
        if code in self._patients:
            del self._patients[code]
            return True
        return False


# ============================================================
# GUI APPLICATION
# ============================================================
class PatientApp(tk.Tk):
    """Tkinter GUI for the Patient Record System."""

    def __init__(self):
        super().__init__()
        self.title("Patient Record System - DPG Health Portal")
        self.geometry("1000x720")
        self.minsize(900, 650)
        self.configure(bg="#f4f6f9")

        self.registry = PatientRegistry()

        # Tkinter variables
        self.var_code = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_age = tk.StringVar()
        self.var_gender = tk.StringVar(value="Female")
        self.var_condition = tk.StringVar()
        self.var_note = tk.StringVar()

        self._build_ui()
        self._refresh_patient_list()
        self._update_status()
        self._tick_clock()

    # ---------------- UI Construction ----------------
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1a5276", height=80)
        header.pack(fill="x")

        tk.Label(
            header, text="🏥 Patient Record System",
            font=("Segoe UI", 20, "bold"), fg="white", bg="#1a5276"
        ).pack(side="left", padx=20, pady=15)

        self.lbl_clock = tk.Label(
            header, text="", font=("Consolas", 12, "bold"),
            fg="#aed6f1", bg="#1a5276"
        )
        self.lbl_clock.pack(side="right", padx=20)

        # Main content area
        main = tk.Frame(self, bg="#f4f6f9")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # ---------- LEFT PANEL (scrollable) ----------
        left_container = tk.LabelFrame(
            main, text=" Register / Update Patient ",
            font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a5276",
            relief="solid", bd=1
        )
        left_container.pack(side="left", fill="y", padx=(0, 10))

        # Create Canvas + Scrollbar for the form
        form_canvas = tk.Canvas(
            left_container, bg="#ffffff", highlightthickness=0, width=320
        )
        form_scroll = ttk.Scrollbar(
            left_container, orient="vertical", command=form_canvas.yview
        )
        form_canvas.configure(yscrollcommand=form_scroll.set)

        form_scroll.pack(side="right", fill="y")
        form_canvas.pack(side="left", fill="both", expand=True)

        # Inner frame that holds the actual form widgets
        form_frame = tk.Frame(form_canvas, bg="#ffffff", padx=15, pady=15)
        form_window = form_canvas.create_window(
            (0, 0), window=form_frame, anchor="nw"
        )

        # Keep inner frame width synced with canvas width
        def _on_canvas_resize(event):
            form_canvas.itemconfig(form_window, width=event.width)
        form_canvas.bind("<Configure>", _on_canvas_resize)

        # Update scrollregion whenever form_frame changes size
        def _on_frame_configure(_event):
            form_canvas.configure(scrollregion=form_canvas.bbox("all"))
        form_frame.bind("<Configure>", _on_frame_configure)

        # Enable mouse-wheel scrolling only while hovering over the form
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_mousewheel(_event):
            form_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(_event):
            form_canvas.unbind_all("<MouseWheel>")

        form_canvas.bind("<Enter>", _bind_mousewheel)
        form_canvas.bind("<Leave>", _unbind_mousewheel)

        # Build the form widgets inside the scrollable frame
        self._build_form(form_frame)

        # ---------- RIGHT PANEL ----------
        right = tk.LabelFrame(
            main, text=" Patient Records ",
            font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a5276",
            padx=10, pady=10, relief="solid", bd=1
        )
        right.pack(side="right", fill="both", expand=True)

        self._build_list(right)

        # Status bar
        self.status = tk.Label(
            self, text="", font=("Segoe UI", 10),
            bg="#1a5276", fg="white", anchor="w", padx=10
        )
        self.status.pack(fill="x", side="bottom")

    def _build_form(self, parent):
        label_font = ("Segoe UI", 11)
        entry_font = ("Segoe UI", 11)

        tk.Label(parent, text="Patient Code (e.g. P-0001):",
                 font=label_font, bg="#ffffff", anchor="w").pack(fill="x", pady=(5, 2))
        tk.Entry(parent, textvariable=self.var_code,
                 font=entry_font).pack(fill="x")

        tk.Label(parent, text="Full Name:",
                 font=label_font, bg="#ffffff", anchor="w").pack(fill="x", pady=(10, 2))
        tk.Entry(parent, textvariable=self.var_name,
                 font=entry_font).pack(fill="x")

        tk.Label(parent, text="Age:",
                 font=label_font, bg="#ffffff", anchor="w").pack(fill="x", pady=(10, 2))
        tk.Entry(parent, textvariable=self.var_age,
                 font=entry_font).pack(fill="x")

        tk.Label(parent, text="Gender:",
                 font=label_font, bg="#ffffff", anchor="w").pack(fill="x", pady=(10, 2))
        ttk.Combobox(
            parent, textvariable=self.var_gender,
            values=["Female", "Male", "Other"], state="readonly",
            font=entry_font
        ).pack(fill="x")

        tk.Label(parent, text="Condition:",
                 font=label_font, bg="#ffffff", anchor="w").pack(fill="x", pady=(10, 2))
        tk.Entry(parent, textvariable=self.var_condition,
                 font=entry_font).pack(fill="x")

        tk.Button(
            parent, text="➕ Register Patient", command=self._register_patient,
            font=("Segoe UI", 11, "bold"), bg="#27ae60", fg="white",
            activebackground="#1e8449", relief="flat", pady=6
        ).pack(fill="x", pady=(20, 5))

        tk.Button(
            parent, text="✏ Update Selected Patient", command=self._update_patient,
            font=("Segoe UI", 11, "bold"), bg="#8e44ad", fg="white",
            activebackground="#6c3483", relief="flat", pady=6
        ).pack(fill="x", pady=5)

        tk.Button(
            parent, text="🧹 Clear Form", command=self._clear_form,
            font=("Segoe UI", 11), bg="#95a5a6", fg="white",
            activebackground="#7f8c8d", relief="flat", pady=6
        ).pack(fill="x", pady=5)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=15)

        tk.Label(
            parent, text="Add Visit Note to Selected Patient:",
            font=("Segoe UI", 11, "bold"), bg="#ffffff", anchor="w"
        ).pack(fill="x", pady=(0, 5))

        tk.Entry(parent, textvariable=self.var_note,
                 font=entry_font).pack(fill="x")

        tk.Button(
            parent, text="📝 Add Note", command=self._add_note,
            font=("Segoe UI", 11, "bold"), bg="#2980b9", fg="white",
            activebackground="#1f618d", relief="flat", pady=6
        ).pack(fill="x", pady=(10, 5))

    def _build_list(self, parent):
        cols = ("code", "name", "age", "gender", "condition", "visits", "updated")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings", height=13)
        headings = {
            "code": ("Code", 80),
            "name": ("Name", 140),
            "age": ("Age", 50),
            "gender": ("Gender", 70),
            "condition": ("Condition", 150),
            "visits": ("Visits", 55),
            "updated": ("Last Updated", 140),
        }
        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=(0, 8))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        tk.Label(
            parent, text="Selected Patient Details:",
            font=("Segoe UI", 11, "bold"), bg="#ffffff", anchor="w"
        ).pack(fill="x")

        self.txt_details = tk.Text(
            parent, height=9, font=("Consolas", 10),
            bg="#fbfbfb", relief="solid", bd=1, wrap="word"
        )
        self.txt_details.pack(fill="both", expand=True, pady=(3, 5))

        btn_row = tk.Frame(parent, bg="#ffffff")
        btn_row.pack(fill="x")

        tk.Button(
            btn_row, text="🔄 Refresh", command=self._refresh_patient_list,
            font=("Segoe UI", 10, "bold"), bg="#f39c12", fg="white",
            activebackground="#d68910", relief="flat", padx=10, pady=4
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            btn_row, text="🗑 Delete Selected", command=self._delete_selected,
            font=("Segoe UI", 10), bg="#e74c3c", fg="white",
            activebackground="#c0392b", relief="flat", padx=10, pady=4
        ).pack(side="left")

    # ---------------- Live clock ----------------
    def _tick_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y   %H:%M:%S")
        self.lbl_clock.config(text=f"🕒 {now}")
        self.after(1000, self._tick_clock)

    # ---------------- Event Handlers ----------------
    def _register_patient(self):
        code = self.var_code.get().strip().upper()
        name = self.var_name.get().strip()
        age_str = self.var_age.get().strip()
        gender = self.var_gender.get()
        condition = self.var_condition.get().strip() or "Unknown"

        if not Patient.validate_patient_code(code):
            messagebox.showerror(
                "Invalid Code",
                "Patient code must be in format 'P-' followed by exactly 4 digits (e.g. P-0001)."
            )
            return

        if not name:
            messagebox.showerror("Missing Name", "Please enter the patient's full name.")
            return

        if not age_str.isdigit() or not (0 < int(age_str) < 130):
            messagebox.showerror("Invalid Age", "Please enter a valid age between 1 and 129.")
            return

        patient = Patient(code, name, int(age_str), gender, condition)
        if not self.registry.add_patient(patient):
            messagebox.showwarning("Duplicate", f"Patient code '{code}' already exists.")
            return

        messagebox.showinfo("Success", f"Patient '{name}' ({code}) registered successfully.")
        self._clear_form()
        self._refresh_patient_list()
        self._update_status()

    def _update_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection",
                                   "Please select a patient from the list to update.")
            return

        code = self.tree.item(selected[0], "values")[0]
        patient = self.registry.get_patient(code)
        if not patient:
            return

        new_name = self.var_name.get().strip() or None
        new_age_str = self.var_age.get().strip()
        new_age = int(new_age_str) if new_age_str.isdigit() else None
        new_gender = self.var_gender.get() or None
        new_condition = self.var_condition.get().strip() or None

        if new_age is not None and not (0 < new_age < 130):
            messagebox.showerror("Invalid Age", "Age must be between 1 and 129.")
            return

        patient.update_info(
            name=new_name, age=new_age,
            gender=new_gender, condition=new_condition
        )

        self._refresh_patient_list()
        for iid in self.tree.get_children():
            if self.tree.item(iid, "values")[0] == code:
                self.tree.selection_set(iid)
                break
        self._show_details(patient)
        self._update_status()
        messagebox.showinfo("Updated", f"Patient '{code}' updated successfully.")

    def _clear_form(self):
        self.var_code.set("")
        self.var_name.set("")
        self.var_age.set("")
        self.var_gender.set("Female")
        self.var_condition.set("")
        self.var_note.set("")

    def _add_note(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient from the list first.")
            return
        note = self.var_note.get().strip()
        if not note:
            messagebox.showwarning("Empty Note", "Please enter a note before adding.")
            return
        code = self.tree.item(selected[0], "values")[0]
        patient = self.registry.get_patient(code)
        if patient:
            patient.update_record(note)
            self.var_note.set("")
            self._refresh_patient_list()
            for iid in self.tree.get_children():
                if self.tree.item(iid, "values")[0] == code:
                    self.tree.selection_set(iid)
                    break
            self._show_details(patient)
            messagebox.showinfo("Note Added", f"Visit note added to {code}.")

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to delete.")
            return
        code = self.tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirm Delete", f"Delete patient '{code}' permanently?"):
            return
        self.registry.remove_patient(code)
        self._refresh_patient_list()
        self.txt_details.delete("1.0", "end")
        self._update_status()

    def _on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        code = self.tree.item(selected[0], "values")[0]
        patient = self.registry.get_patient(code)
        if patient:
            self.var_code.set(patient.patient_code)
            self.var_name.set(patient.name)
            self.var_age.set(str(patient.age))
            self.var_gender.set(patient.gender)
            self.var_condition.set(patient.condition)
            self._show_details(patient)

    def _show_details(self, patient: Patient):
        self.txt_details.delete("1.0", "end")
        self.txt_details.insert("end", patient.display_info() + "\n")
        if patient.records:
            self.txt_details.insert("end", "\nVisit History:\n")
            for r in patient.records:
                self.txt_details.insert("end", f"  • {r}\n")
        else:
            self.txt_details.insert("end", "\nNo visit notes yet.")

    def _refresh_patient_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for patient in self.registry.get_all():
            self.tree.insert(
                "", "end",
                values=(
                    patient.patient_code,
                    patient.name,
                    patient.age,
                    patient.gender,
                    patient.condition,
                    len(patient.records),
                    patient.updated_at.strftime("%Y-%m-%d %H:%M"),
                ),
            )

    def _update_status(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status.config(
            text=f"  Total Registered: {self.registry.get_count()}   |   "
                 f"Total Patient Objects Created: {Patient.get_total_patients()}   |   "
                 f"Last action: {now}"
        )


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = PatientApp()
    app.mainloop()