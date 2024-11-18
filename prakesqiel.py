import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

def create_database():
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    con.commit()
 
def fetch_data():
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    con.close()
    return rows

def save_to_database(nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama_siswa, biologi, fisika, inggris, prediksi_fakultas))
    con.commit()
    con.close()

def update_database(id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute("""
        UPDATE nilai_siswa SET
            nama_siswa = ?,
            biologi = ?,
            fisika = ?,
            inggris = ?,
            prediksi_fakultas = ?
        WHERE id = ?
    """, (nama_siswa, biologi, fisika, inggris, prediksi_fakultas, id))
    con.commit()
    con.close()

def delete_database(id):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM nilai_siswa WHERE id = ?", (id,))
    con.commit()
    con.close()


def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"
    
def submit():
    try:
        nama_siswa = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama_siswa:
            raise Exception("Nama siswa tidak boleh kosong.")   

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama_siswa, biologi, fisika, inggris, prediksi) 

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def update():
    try:
        if not selected_id.get():
            raise Exception("Pilih data yang akan diupdate!")
        
        id = int(selected_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():
    try:
        if not selected_id.get():
            raise Exception("Pilih data yang akan dihapus!")
        
        id = int(selected_id.get())
        delete_database(id)

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")

    selected_id.set("")

def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert("", "end", values=row)

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)["values"]

        selected_id.set(selected_row[0])

        nama_var.set(selected_row[1])   
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

create_database()

root = Tk()
root.title("Prediksi Fakultas Siswa")

nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_id = StringVar()


Label(root, text="Nama Siswa:").grid(row=0, column=0, sticky="w")
Entry(root, textvariable=nama_var).grid(row=0, column=1)

Label(root, text="Nilai Biologi:").grid(row=1, column=0, sticky="w")
Entry(root, textvariable=biologi_var).grid(row=1, column=1)

Label(root, text="Nilai Fisika:").grid(row=2, column=0, sticky="w")
Entry(root, textvariable=fisika_var).grid(row=2, column=1)

Label(root, text="Nilai Bahasa Inggris:").grid(row=3, column=0, sticky="w")
Entry(root, textvariable=inggris_var).grid(row=3, column=1)

Button(root, text="Simpan", command=submit).grid(row=4, column=0)
Button(root, text="Update", command=update).grid(row=4, column=1)
Button(root, text="Hapus", command=delete).grid(row=4, column=2)

columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("nama_siswa", text="Nama Siswa")
tree.heading("biologi", text="Nilai Biologi")
tree.heading("fisika", text="Nilai Fisika")
tree.heading("inggris", text="Nilai Bahasa Inggris")
tree.heading("prediksi_fakultas", text="Prediksi Fakultas")
tree.column("id", width=50)
tree.column("nama_siswa", width=200)
tree.column("biologi", width=100)
tree.column("fisika", width=100)
tree.column("inggris", width=100)
tree.column("prediksi_fakultas", width=200)

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor="center")

tree.bind("<ButtonRelease-1>", fill_inputs_from_table)

root.mainloop()