import tkinter as tk
from tkinter import ttk, messagebox
from data import load_data, save_data

root = tk.Tk()
root.title("Internship Management System")
root.geometry("1200x700")
root.configure(bg="#EAF4FF")

# ---------------- Dashboard ----------------

total_var = tk.StringVar(value="0")
ongoing_var = tk.StringVar(value="0")
completed_var = tk.StringVar(value="0")

header = tk.Label(
    root,
    text="INTERNSHIP MANAGEMENT SYSTEM",
    font=("Arial",22,"bold"),
    bg="#0B3D91",
    fg="white",
    pady=15
)
header.pack(fill="x")

dashboard = tk.Frame(root,bg="#EAF4FF")
dashboard.pack(pady=10)

def create_card(parent,title,color,var):
    frame=tk.Frame(parent,bg=color,width=180,height=80)
    frame.pack_propagate(False)
    frame.pack(side="left",padx=10)

    tk.Label(
        frame,
        text=title,
        bg=color,
        fg="white",
        font=("Arial",12,"bold")
    ).pack(pady=(10,0))

    tk.Label(
        frame,
        textvariable=var,
        bg=color,
        fg="white",
        font=("Arial",22,"bold")
    ).pack()

create_card(dashboard,"Total Interns","#007BFF",total_var)
create_card(dashboard,"Ongoing","#28A745",ongoing_var)
create_card(dashboard,"Completed","#DC3545",completed_var)

main_frame=tk.Frame(root,bg="#EAF4FF")
main_frame.pack(fill="both",expand=True,pady=10)

# ---------------- Form ----------------

form=tk.LabelFrame(
    main_frame,
    text="Intern Details",
    bg="white",
    font=("Arial",12,"bold"),
    padx=15,
    pady=15
)
form.grid(row=0,column=0,padx=20,sticky="n")

labels=[
"Intern ID",
"Name",
"College",
"Department",
"Email",
"Phone",
"Domain",
"Mentor",
"Duration"
]

entries={}

for i,text in enumerate(labels):

    tk.Label(
        form,
        text=text,
        bg="white",
        font=("Arial",11)
    ).grid(row=i,column=0,sticky="w",pady=6)

    e=tk.Entry(form,width=30,font=("Arial",11))
    e.grid(row=i,column=1,padx=10,pady=6)

    entries[text]=e

tk.Label(
    form,
    text="Status",
    bg="white",
    font=("Arial",11)
).grid(row=9,column=0,sticky="w")

status=ttk.Combobox(
    form,
    values=["Ongoing","Completed"],
    state="readonly",
    width=28
)
status.current(0)
status.grid(row=9,column=1,pady=6)

# ---------------- Buttons ----------------

button_frame=tk.Frame(form,bg="white")
button_frame.grid(row=10,column=0,columnspan=2,pady=20)

def clear_fields():
    for e in entries.values():
        e.delete(0,tk.END)

    status.current(0)

def update_dashboard():

    data=load_data()

    total_var.set(str(len(data)))

    ongoing=0
    completed=0

    for i in data:
        if i["Status"]=="Ongoing":
            ongoing+=1
        else:
            completed+=1

    ongoing_var.set(str(ongoing))
    completed_var.set(str(completed))

def add_intern():

    intern={
        "Intern ID":entries["Intern ID"].get(),
        "Name":entries["Name"].get(),
        "College":entries["College"].get(),
        "Department":entries["Department"].get(),
        "Email":entries["Email"].get(),
        "Phone":entries["Phone"].get(),
        "Domain":entries["Domain"].get(),
        "Mentor":entries["Mentor"].get(),
        "Duration":entries["Duration"].get(),
        "Status":status.get()
    }

    data=load_data()
    data.append(intern)
    save_data(data)

    table.insert(
        "",
        "end",
        values=(
            intern["Intern ID"],
            intern["Name"],
            intern["Department"],
            intern["Mentor"],
            intern["Status"]
        )
    )

    update_dashboard()

    messagebox.showinfo(
        "Success",
        "Intern added successfully!"
    )

    clear_fields()
    # ---------------- Buttons ----------------

tk.Button(
    button_frame,
    text="Add",
    bg="#28A745",
    fg="white",
    font=("Arial",10,"bold"),
    width=12,
    command=add_intern
).grid(row=0,column=0,padx=5,pady=5)

tk.Button(
    button_frame,
    text="Clear",
    bg="#6C757D",
    fg="white",
    font=("Arial",10,"bold"),
    width=12,
    command=clear_fields
).grid(row=0,column=1,padx=5,pady=5)

tk.Button(
    button_frame,
    text="Exit",
    bg="#DC3545",
    fg="white",
    font=("Arial",10,"bold"),
    width=12,
    command=root.destroy
).grid(row=0,column=2,padx=5,pady=5)

# ---------------- Table ----------------

table_frame = tk.Frame(main_frame, bg="#EAF4FF")
table_frame.grid(row=0, column=1, padx=20)

table = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Department", "Mentor", "Status"),
    show="headings",
    height=18
)

table.heading("ID", text="Intern ID")
table.heading("Name", text="Name")
table.heading("Department", text="Department")
table.heading("Mentor", text="Mentor")
table.heading("Status", text="Status")

table.column("ID", width=100)
table.column("Name", width=180)
table.column("Department", width=150)
table.column("Mentor", width=150)
table.column("Status", width=120)

scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scroll.set)

table.pack(side="left")
scroll.pack(side="right", fill="y")

# ---------------- Load Records ----------------

def load_records():
    for row in table.get_children():
        table.delete(row)

    data = load_data()

    for intern in data:
        table.insert(
            "",
            "end",
            values=(
                intern["Intern ID"],
                intern["Name"],
                intern["Department"],
                intern["Mentor"],
                intern["Status"]
            )
        )

    update_dashboard()

load_records()

root.mainloop()