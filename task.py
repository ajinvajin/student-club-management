from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import csv

conn = sqlite3.connect("club_management.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT,password TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS clubs(id INTEGER PRIMARY KEY AUTOINCREMENT,club_name TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS membership(student_id INTEGER,club_id INTEGER,event_id INTEGER)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,club TEXT,date TEXT,status TEXT)""")
conn.commit()

root = Tk()
root.title("College Club Management System")
root.geometry("900x600")
root.configure(bg="light blue")
def clear_screen():
    for i in root.winfo_children():
        i.destroy()

def home_page():
    clear_screen()
    Label(root,text="College Club Management System",font=("Arial", 22),fg="blue",bg="light blue").pack(pady=30)
    Button(root,text="Student Register",width=25,command=register_student,bg="light green").pack(pady=10)
    Button(root,text="Student Login",width=25,command=student_login,bg="light green").pack(pady=10)
    Button(root,text="Club Admin Login",width=25,command=login_admin,bg="light green").pack(pady=10)
    Button(root,text="College Management",width=25,command=management_login,bg="light green").pack(pady=10)

def register_student():
    clear_screen()
    Label(root,text="Student Registration",font=("Arial",18),fg="blue",bg="light blue").pack(pady=20)
    Label(root,text="Name",bg="orange").pack()
    name_entry=Entry(root)
    name_entry.pack()
    Label(root,text="Email",bg="orange").pack()
    email_entry=Entry(root)
    email_entry.pack()
    Label(root,text="Password",bg="orange").pack()
    pass_entry=Entry(root,show="*")
    pass_entry.pack()

    def save_student():
        name=name_entry.get()
        email=email_entry.get()
        password=pass_entry.get()
        cursor.execute("INSERT INTO students(name,email,password) VALUES(?,?,?)",(name, email, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration Successful")
        home_page()
    Button(root,text="Register",command=save_student,bg="light green").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()

def student_login():
    clear_screen()
    Label(root,text="Student Login",font=("Arial", 18),bg="light blue",fg="blue").pack(pady=20)
    Label(root,text="Email",bg="orange").pack()
    email_entry=Entry(root)
    email_entry.pack()
    Label(root,text="Password",bg="orange").pack()
    pass_entry=Entry(root,show="*")
    pass_entry.pack()

    def login():
        email=email_entry.get()
        password=pass_entry.get()
        cursor.execute("SELECT*FROM students WHERE email=? AND password=?",(email, password))
        data=cursor.fetchone()
        if data:
            student_dashboard(data[0])
        else:
            messagebox.showerror("Error","Invalid Login")
    Button(root,text="Login",command=login,bg="yellow").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()

def student_dashboard(student_id):
    clear_screen()
    Label(root,text="Student Dashboard",font=("Arial", 18)).pack(pady=20)
    Button(root,text="Browse Clubs",width=25,command=lambda:browse_clubs(student_id),bg="light green").pack(pady=10)
    Button(root,text="View Events",width=25,command=lambda:view_events(student_id),bg="light green").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()

def browse_clubs(student_id):
    clear_screen()
    Label(root,text="Available Clubs",font=("Arial",16)).pack(pady=10)
    tree=ttk.Treeview(root,columns=("ID","Club"),show="headings")
    tree.heading("ID",text="ID")
    tree.heading("Club",text="Club Name")
    tree.pack(fill=BOTH,expand=True)
    cursor.execute("SELECT*FROM clubs")
    for row in cursor.fetchall():
        tree.insert("",END,values=row)

    def join_club():
        selected=tree.selection()
        if not selected:
            messagebox.showerror("Error","Please select a club")
            return
        club_id=tree.item(selected[0])["values"][0]
        cursor.execute("INSERT INTO membership VALUES(?,?,?)",(student_id,club_id,None))
        conn.commit()
        messagebox.showinfo("Joined","Club Joined Successfully")
    Button(root,text="Join Club",command=join_club,bg="light green").pack(pady=10)
    Button(root,text="Back",command=lambda:student_dashboard(student_id),bg="violet").pack()


def view_events(student_id):
    clear_screen()
    Label(root,text="Events",font=("Arial", 16)).pack(pady=10)
    tree=ttk.Treeview(root,columns=("ID","Title","Club","Date","Status"),show="headings")
    for col in("ID","Title","Club","Date","Status"):
        tree.heading(col,text=col)
    tree.pack(fill=BOTH,expand=True)
    cursor.execute("SELECT*FROM events")
    for row in cursor.fetchall():
        tree.insert("",END,values=row)

    def select_event():
        selected=tree.selection()
        if not selected:
            messagebox.showerror("error","please select an event")
            return
        event_id=tree.item(selected[0])["values"][0]
        cursor.execute("UPDATE membership SET event_id=? WHERE student_id=?",(event_id,student_id))
        conn.commit()
        messagebox.showinfo("Selected","Event Selected")
    Button(root,text="Select event",command=select_event,bg="light green").pack(pady=10)        
    Button(root,text="Back",command=lambda:student_dashboard(student_id),bg="violet").pack(pady=10)

def admin_dashboard():
    clear_screen()
    Label(root,text="Club Admin Dashboard",font=("Arial",18)).pack(pady=20)
    Button(root,text="Create Club",width=25,command=create_club,bg="light green").pack(pady=10)
    Button(root,text="Create Event",width=25,command=create_event,bg="light green").pack(pady=10)
    Button(root,text="Participants",width=25,command=view_participants,bg="light green").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()

def login_admin():
    clear_screen()
    Label(root,text="Admin Login",font=("Arial",18)).pack(pady=20) 
    Label(root,text="username",bg="orange").pack()
    username=Entry(root)
    username.pack()
    Label(root,text="Password",bg="orange").pack()
    password=Entry(root,show="*")
    password.pack()
    
    def admin_login():
        if username.get()=="admin" and password.get()=="1234":
            admin_dashboard()
        else:
            messagebox.showerror("Error","Invalid Login")
    Button(root,text="Login",command=admin_login,bg="yellow").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()        

def create_club():
    clear_screen()
    Label(root,text="Create Club",font=("Arial", 16)).pack(pady=20)
    Label(root,text="Club Name").pack()
    club_entry=Entry(root)
    club_entry.pack()

    def save():
        cursor.execute("INSERT INTO clubs(club_name) VALUES(?)",(club_entry.get(),))
        conn.commit()
        messagebox.showinfo("Success","Club Created")
    Button(root,text="Create",command=save,bg="light green").pack(pady=10)
    Button(root,text="Back",command=admin_dashboard,bg="violet").pack()

def create_event():
    clear_screen()
    Label(root,text="Create Event",font=("Arial", 16)).pack(pady=20)
    Label(root,text="Event Title").pack()
    title_entry=Entry(root)
    title_entry.pack()
    Label(root,text="Club").pack()
    club_entry=Entry(root)
    club_entry.pack()
    Label(root,text="Date").pack()
    date_entry=Entry(root)
    date_entry.pack()

    def save():
        cursor.execute("INSERT INTO events(title,club,date,status)VALUES(?,?,?,?)",(title_entry.get(),club_entry.get(),date_entry.get(),"Pending"))
        conn.commit()
        messagebox.showinfo("Success","Event Submitted")
    Button(root,text="Submit",command=save,bg="light green").pack(pady=10)
    Button(root,text="Back",command=admin_dashboard,bg="violet").pack()

def view_participants():
    clear_screen()
    Label(root,text="Participants",font=("arial",16)).pack(pady=20)
    tree=ttk.Treeview(root,columns=("students.id","students.name","clubs.club_name","events.title",'events.date',"events.status"),show="headings")
    tree.heading("students.id",text="Participant ID")
    tree.heading("students.name",text="Participant Name")
    tree.heading("clubs.club_name",text="Club Name")
    tree.heading("events.title",text="Event Title")
    tree.heading("events.date",text="Event Date")
    tree.heading("events.status",text="Event Status")
    tree.pack(fill=BOTH,expand=True)
    cursor.execute("""SELECT students.id, students.name, clubs.club_name, events.title, events.date, events.status
            FROM membership JOIN students ON membership.student_id = students.id JOIN clubs ON membership.club_id = clubs.id
            LEFT JOIN events ON membership.event_id = events.id""")
    for row in cursor.fetchall():
        tree.insert("",END,values=row)
    Button(root,text="Export to csv",command=lambda:export_csv(tree),bg="light green").pack(pady=10)    
    Button(root,text="Back",command=admin_dashboard,bg="violet").pack(pady=10)
    
    def export_csv(tree):
        rows=[tree.item(i)["values"] for i in tree.get_children()]
        with open("participants.csv","w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(["Participant ID","Participant Name","Club Name","Event Title","Event Date","Event Status"])
            writer.writerows(rows)
        messagebox.showinfo("Exported","Data exported successfully")    

def management_login():
    clear_screen()
    Label(root,text="Management Login",font=("Arial",18)).pack(pady=20)
    Label(root,text="Username",bg="orange").pack()
    username=Entry(root)
    username.pack()
    Label(root,text="Password",bg="orange").pack()
    password=Entry(root,show="*")
    password.pack()

    def login_management():
        if username.get()=="management" and password.get()=="5678":
            management_dashboard()
        else:
            messagebox.showerror("Error","Invalid Login")

    Button(root,text="Login",command=login_management,bg="yellow").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()

def management_dashboard():     
    clear_screen()
    Label(root,text="Event Approval System",font=("Arial", 18)).pack(pady=10)
    tree=ttk.Treeview(root,columns=("ID","Title","Club","Date","Status"),show="headings")
    for col in("ID","Title","Club","Date","Status"):
        tree.heading(col,text=col)
    tree.pack(fill=BOTH,expand=True)
    cursor.execute("SELECT*FROM events")
    for row in cursor.fetchall():
        tree.insert("",END,values=row)

    def approve():
        selected=tree.selection()
        if not selected:
            messagebox.showerror("Error","Select an event")
            return
        event_id=tree.item(selected[0])["values"][0]
        cursor.execute("UPDATE events SET status='Approved' WHERE id=?",(event_id,))
        conn.commit()
        messagebox.showinfo("Approved","Event Approved")
    Button(root,text="Approve Event",command=approve,bg="light green").pack(pady=10)
    Button(root,text="Back",command=home_page,bg="violet").pack()

home_page()
root.mainloop()