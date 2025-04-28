from tkinter import *
import mysql.connector
from tkinter import ttk


root = Tk()
root.geometry("400x400")
root.title("MySQL Connection")


# Muodosta MySql Yhteys
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "PuupiFantti412!",
    database = "levyt"
)

# Create a cursor object using the connection
my_cursor = mydb.cursor()

search_labels = []
empty_search_label = None

# Create a new database
#my_cursor.execute("CREATE DATABASE levyt")

# Create a table
#my_cursor.execute("CREATE TABLE levyt (id INT AUTO_INCREMENT PRIMARY KEY, levy VARCHAR(255), artisti VARCHAR(255),vuosi INT(10))")

# Drop a table
#my_cursor.execute("DROP TABLE levyt")


# Tyhjennä Lomakkeen Kentät
def clear_fields(levy_box, artisti_box, vuosi_box):
    levy_box.delete(0, END)
    artisti_box.delete(0, END)
    vuosi_box.delete(0, END) 

# Lisää Levy Tietokantaan
def add_levy(levy_box, artisti_box, vuosi_box):
    levy = levy_box.get()
    artisti = artisti_box.get()
    vuosi = vuosi_box.get()

    sql_command = "INSERT INTO levyt (levy,artisti,vuosi) VALUES (%s,%s,%s)"
    values = (levy,artisti,vuosi)
    my_cursor.execute(sql_command,values)

    #Commit The Changes To The Database
    mydb.commit()
    #Clear fields
    clear_fields(levy_box, artisti_box, vuosi_box)

    search_levy()

# Poistaa Levyn Tietokannasta
def delete_levy(id,window):
    sql = f"DELETE FROM levyt WHERE id={id}"
    my_cursor.execute(sql)
    mydb.commit()
    window.destroy()
    search_levy()

# Muokkaa levyä tietokannassa
def edit_levy(record, window):

    edit_window = Toplevel(root)
    edit_window.title("Muokkaa levyä")
    edit_window.geometry("300x300")

    # Luo Nimikkeet Lomakkeen Kentille
    levy_label = Label(edit_window, text="Levy")
    levy_label.grid(row=1, column=0, sticky=W, padx=10)
    artisti_label = Label(edit_window, text="Artisti")
    artisti_label.grid(row=2, column=0, sticky=W, padx=10)
    vuosi_label = Label(edit_window, text="Julkaisuvuosi")
    vuosi_label.grid(row=3, column=0, sticky=W, padx=10)

    # Luo Lomakkeen Kentät
    levy_box = Entry(edit_window)
    levy_box.insert(0,record[1])
    levy_box.grid(row=1,column=1, pady=5)

    artisti_box = Entry(edit_window)
    artisti_box.insert(0,record[2])
    artisti_box.grid(row=2,column=1,pady=5)

    vuosi_box = Entry(edit_window)
    vuosi_box.insert(0,record[3])
    vuosi_box.grid(row=3,column=1,pady=5)

    # Funktio muutosten tallentamiselle
    def save_changes():
        new_levy=levy_box.get()
        new_artisti=artisti_box.get()
        new_vuosi=vuosi_box.get()
        new_entry=[record[0],new_levy,new_artisti,new_vuosi]

        sql="UPDATE levyt SET levy=%s, artisti=%s,vuosi=%s WHERE id=%s"
        values = (new_levy,new_artisti,new_vuosi,record[0])
        my_cursor.execute(sql,values)
        mydb.commit()
        edit_window.destroy()
        window.destroy()
        open_levy_window(new_entry)
        search_levy()
    
    save_button = Button(edit_window, text="Tallenna muutokset", command=save_changes)
    save_button.grid(row=4,column=0)

# Luo Uuden Ikkunan levyn Lisäämiselle
def add_levy_query():
    add_album_query = Toplevel(root)
    add_album_query.geometry("400x400")
    add_album_query.title("Lisää Uusi Levy")

    # Luo Otsikko
    title_lable = Label(add_album_query, text="Anna Uuden Levyn Tiedot", font=("Helvetica",16))
    title_lable.grid(row=0, column=0, columnspan=2, pady=10)

    # Luo Nimikkeet Lomakkeen Kentille
    levy_label = Label(add_album_query, text="Levy")
    levy_label.grid(row=1, column=0, sticky=W, padx=10)
    artisti_label = Label(add_album_query, text="Artisti")
    artisti_label.grid(row=2, column=0, sticky=W, padx=10)
    vuosi_label = Label(add_album_query, text="Julkaisuvuosi")
    vuosi_label.grid(row=3, column=0, sticky=W, padx=10)

    # Luo Lomakkeen Kentät
    levy_box = Entry(add_album_query)
    levy_box.grid(row=1,column=1, pady=5)

    artisti_box = Entry(add_album_query)
    artisti_box.grid(row=2,column=1,pady=5)

    vuosi_box = Entry(add_album_query)
    vuosi_box.grid(row=3,column=1,pady=5)

    # Luo Painikkeet
    add_levy_button = Button(
       add_album_query, 
       text="Lisää Levy Tietokantaan", 
       command=lambda: add_levy(levy_box, artisti_box, vuosi_box)
    )
    add_levy_button.grid(row=4,column=0,padx=10,pady=10)

    clear_fields_button = Button(
       add_album_query,
       text="Tyhjennä Kentät",
       command=lambda: clear_fields(levy_box, artisti_box, vuosi_box))
    clear_fields_button.grid(row=4,column=1)

# Luo Listan Levyistä Tietokannassa
def list_levyt(result):
    global search_labels

    #Luo Otsikot Sarakkeille
    column_labels = ["Levy", "Artisti", "Julkaisuvuosi"]
    for index, label in enumerate(column_labels):
        column_label = Label(root, text=label, font=("Helvetica", 10, "bold"))
        column_label.grid(row=4, column=index, sticky=W)
        

    for label in search_labels:
        label.destroy()
    search_labels = []

    for index, x in enumerate(result):
        num = 0
        for y in x[1:]:
            if(isinstance(y,str)):
                y=y[:30]
            if(num==0):
                item_label=Label(root, text=y,cursor="hand2")
                item_label.grid(row=index + 5, column=num, sticky=W)
                item_label.bind("<Button-1>",lambda event, r=x:open_levy_window(r))
            else:
                item_label = Label(root,text=y)
                item_label.grid(row=index + 5, column=num, sticky=W)
            search_labels.append(item_label)
            num+=1

# Etsi Levy Listauksesta
def search_levy():
    global empty_search_label
    selected=drop.get()
    searched=search_box.get()
    sort_filter=filter.get()



    if selected == "Levy":
        sql = f"SELECT * FROM levyt WHERE levy LIKE %s ORDER BY {sort_filter} ASC"
    if selected == "Artisti":
        sql = f"SELECT * FROM levyt WHERE artisti LIKE %s ORDER BY {sort_filter} ASC"
    if selected == "Vuosi":
        sql = f"SELECT * FROM levyt WHERE vuosi LIKE %s ORDER BY {sort_filter} ASC"

    name = ("%" + searched + "%",)
    my_cursor.execute(sql,name)

    result= my_cursor.fetchall()

    for label in search_labels:
        label.destroy()
    search_labels.clear()

    if empty_search_label:
        empty_search_label.destroy()
        empty_search_label = None

    if not result:
        empty_search_label=Label(root,text="Ei Tuloksia",fg="red",font=("Helvetica", 12,"bold"))
        empty_search_label.grid(row=5, column=0)
    else:
        list_levyt(result)

# Avaa Levy Uudessa Ikkunassa
def open_levy_window(record):
    levy_window = Toplevel(root)
    levy_window.title(f"Levy: {record[1]}")
    levy_window.geometry("300x300")

    title_label = Label(levy_window, text=record[1], font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(10, 20))


    details = [
        f"Artisti: {record[2]}",
        f"Vuosi: {record[3]}"
    ]

    for text in details:
        Label(levy_window, text=text, anchor=W).pack(fill="x", padx=10, pady=3)

    button_frame = Frame(levy_window)
    button_frame.pack(pady=20)

    delete_button = Button(button_frame, text="Poista levy", command=lambda: delete_levy(record[0],levy_window))
    delete_button.pack(side=LEFT, padx=10)

    edit_button = Button(button_frame, text="Muokkaa", command=lambda: edit_levy(record,levy_window))
    edit_button.pack(side=LEFT, padx=10)


# Luo Otsikko
title_lable = Label(root, text="Jeremiaksen Levyt", font=("Helvetica",16))
title_lable.grid(row=0, column=0, columnspan=2, pady=10)

# Haku Frame
search_frame = Frame(root)
search_frame.grid(row=1, column=0, columnspan=2, sticky=W, padx=10, pady=5)

search_label = Label(search_frame, text="Hae Levyä:")
search_label.pack(side=LEFT)

search_box = Entry(search_frame, width=12)
search_box.pack(side=LEFT, padx=5)
search_box.bind("<KeyRelease>", lambda event: search_levy())

drop = ttk.Combobox(search_frame, value=["Levy", "Artisti", "Vuosi"],width=5)
drop.current(0)
drop.pack(side=LEFT, padx=5)

# Suodatus Frame
filter_frame = Frame(root)
filter_frame.grid(row=2, column=0, columnspan=2, sticky=W, padx=10, pady=5)

filter_label = Label(filter_frame, text="Suodata:")
filter_label.pack(side=LEFT)

filter = ttk.Combobox(filter_frame, value=["levy", "artisti", "vuosi"],width=5)
filter.current(0)
filter.pack(side=LEFT, padx=5)
filter.bind("<<ComboboxSelected>>", lambda e: search_levy())

# Lisää Levy -painike
add_levy_button = Button(root, text="Lisää Levy", command=add_levy_query)
add_levy_button.grid(row=3, column=0, pady=5, sticky=W, padx=10)


search_levy()
root.mainloop()