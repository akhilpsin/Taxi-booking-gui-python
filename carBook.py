#--------------------------------------------------------------------
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import ttk, messagebox

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

#Log in Funtions
def loginpage():
    def submitact():
        user = Username.get()
        passw = password.get()
        conn = sqlite3.connect("carbookin.db")
        chek_sql="SELECT * from carbooking_table WHERE uname='"+user+"'AND psw='"+passw+"';"
        #print(chek_sql)

        cur = conn.cursor()
        cur.execute(chek_sql)
        if cur.fetchall():
            conn.close()
            print("login sucess")
            bookingpage(root,user,passw)
        else:
            messagebox.showerror("Error","please Register"+user)	
            conn.close()

    root = tk.Tk()
    root.geometry("300x150")
    root.title("Car bookin Login Page")


    # Defining the first row
    lblfrstrow = tk.Label(root, text ="Username:", )
    lblfrstrow.place(x = 50, y = 20)

    Username = tk.Entry(root, width = 35)
    Username.place(x = 150, y = 20, width = 100)

    lblsecrow = tk.Label(root, text ="Password:")
    lblsecrow.place(x = 50, y = 50)

    password = tk.Entry(root, width = 35,show= '*')
    password.place(x = 150, y = 50, width = 100)

    submitbtn = tk.Button(root, text =" Login ", command = submitact)
    submitbtn.place(x = 150, y = 90, width = 55)

    register_btn = Button(root , text=" Register " , command = lambda: registrationpage(root) )
    register_btn.place(x=50 , y =90)

    root.mainloop()
#--------------------------------------------------------------------------
#Registration Page
def registrationpage(root):
    root.destroy()

    window = Tk()
    window.title("Please register Your self")
    window.geometry('500x350')

    unam_var=tk.StringVar()
    passw_var=tk.StringVar()

    fname_var=tk.StringVar()
    lname_var=tk.StringVar()

    email_var=tk.StringVar()
    pho_var=tk.StringVar()

    #Registration funtions
    def dbAction():
        #all the registration detals are obtain here
        uname_entry=unam_var.get()
        psw_entry=passw_var.get()
        fname_entry=fname_var.get()
        lname_entry=lname_var.get()
        email_entry=email_var.get()
        phone_entry=pho_var.get()
        
        #print(uname_entry,psw_entry,fname_entry,lname_entry,email_entry,phone_entry)
        #Connecting with the DB with sqllit
        conn = sqlite3.connect("carbookin.db")
        print("DB create")
        table_createQurey='''CREATE TABLE IF NOT EXISTS carbooking_table( uname VARCHAR(255),psw VARCHAR(255),First_Name VARCHAR(255),Last_Name VARCHAR(255),phone VARCHAR(255),email VARCHAR(255)); '''
        insert_Query="INSERT INTO carbooking_table(uname,psw,First_Name,Last_Name,phone,email) VALUES ('"+uname_entry+"','"+psw_entry+"','"+fname_entry+"','"+lname_entry+"','"+phone_entry+"','"+email_entry+"')"
        #print(insert_Query)
        
        cur = conn.cursor()
        cur.execute(table_createQurey)
        conn.commit()
        #print("table created")
        cur.execute(insert_Query)
        conn.commit()
        #print("Values Inserted")
            
        cur.execute("SELECT * FROM carbooking_table")
        print(cur.fetchall())
        cur.close()
        window.destroy()
        loginpage()
    
    #empty = Label(window ,text = "     ").grid(row =0,column =3)
    empty = Label(window ,text = "Registartion Page",font = 'Verdana 11 bold').grid(row =1,column =3)
    empty = Label(window ,text = "     ").grid(row =2,column =3)
    
    uname = Label(window ,text = " User name: ").grid(row =3,column =0)
    psw = Label(window ,text = " Password: ").grid(row =3,column =3)
    fname = Label(window ,text = " First Name: ").grid(row =4,column =0)
    lname = Label(window ,text = " Last Name: ").grid(row =4,column =3)
    email = Label(window ,text = " Email ID: ").grid(row =5,column = 0)
    phone = Label(window ,text = " Phone: ").grid(row =5,column = 3)
    
    uname_entry = Entry(window,textvariable = unam_var).grid(row =3,column =1)
    psw_entry = Entry(window,textvariable = passw_var).grid(row =3,column =4)
    fname_entry = Entry(window,textvariable = fname_var).grid(row =4,column =1)
    lname_entry = Entry(window,textvariable = lname_var).grid(row =4,column =4)
    email_entry = Entry(window,textvariable = email_var).grid(row =5,column = 1)
    phone_entry = Entry(window,textvariable = pho_var).grid(row =5,column = 4)
    empty = Label(window ,text = "     ").grid(row =6,column =3)
    
    btn = ttk.Button(window ,text="Submit",command = dbAction).grid(row=7,column=3)
    window.mainloop()
#--------------------------------------------------------------------------

def bookingpage(root,user,passw):
    root.destroy()
    conn = sqlite3.connect("carbookin.db")
    chek_sql="SELECT * from carbooking_table WHERE uname='"+user+"'AND psw='"+passw+"';"

    cur = conn.cursor()
    cur.execute(chek_sql)
    val=str(cur.fetchall())
    userdata=val.replace("[(","").replace("'","").replace(")]","")
    userdata=userdata.split(",")
    fname=userdata[2]
    lname=userdata[3]
    phone=userdata[4]
    email=userdata[5]
    print(userdata)
    #Tikinter screen starts here
    bookingwindow = Tk()
    bookingwindow.title("Book Your Ride !")
    bookingwindow.geometry('400x300')

    clicked = StringVar()
    regFAdd_var = StringVar()
    regTAdd_var = StringVar()
    regdist_var = StringVar()

    caroptions=["1.Micro : 7/km","2.Hatchback: 12/km","3.Sedan : 18/km","4.SUV : 22/km","5.MPV: 28/km","6.Luxury: 35/km","7.Limousine : 50/km","8.Eletric :4/km"]

    #this function is to see the calculated value
    def calculate():
        ditance=regdist_var.get()
        carselected=clicked.get()
        carselected_price=(carselected.replace("/km","")).split(":")[-1].strip()
        #print("Selected car price:",carselected)
        #print("Distance:",ditance)
        amount=int(carselected_price)*int(ditance)
        Label(bookingwindow,text = "Total Cost "+str(amount)+" Rs.").grid(row =10,column =1)
        return amount,carselected,[fname,lname,phone,regFAdd_var.get(),regTAdd_var.get(),regdist_var.get()]

    
    #this function generate booked details
    def booked():
        amount,carselected,datalist=calculate()
        tableData = [
        ["Billing Name & Phone No", "Pick Up Address", "Drop of address", "Toal Distance (KM)", "Type of Car"],
        [datalist[0] +" "+datalist[1]+"\n"+datalist[2],datalist[3],datalist[4],datalist[5],carselected.split(".")[-1]],
        ["Total Cost", "", "", str(amount)+" Rs"],
        ]

        # creating a Document structure with A4 size page
        docu = SimpleDocTemplate(fname+"_invoice_("+str(amount)+"Rs).pdf", pagesize=A4)
        styles = getSampleStyleSheet()


        doc_style = styles["Heading1"]
        doc_style.alignment = 1

        title = Paragraph("BOOKING INVOICE", doc_style)

        style = TableStyle([
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (5, 1), 1, colors.chocolate),
                ("BACKGROUND", (0, 0), (4, 0), colors.skyblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ])
        # creates a table object using the Table() to pass the table data and the style object
        table = Table(tableData, style=style)
        # finally, we have to build the actual pdf merging all objects together
        docu.build([title, table])
        Label(bookingwindow,text = "Cab Booked Invoice Generated! ").grid(row =14,column =1)
        print("Invoice Generated! Thankyou")

    Label(bookingwindow ,text = " Book Your Ride Here! ",font = 'Verdana 10 bold').grid(row =1)
    Label(bookingwindow ,text = "     ").grid(row =2)
    
    Label(bookingwindow ,text = "User ID").grid(row =3,column =0)
    Label(bookingwindow ,text = user).grid(row =3,column =1)

    Label(bookingwindow ,text = "Billing Name" ).grid(row =4,column =0)
    Label(bookingwindow ,text = fname +" "+lname ).grid(row =4,column =1)

    Label(bookingwindow ,text = "Mobile Number").grid(row =5,column =0)
    Label(bookingwindow ,text = phone).grid(row =5,column =1)

    Label(bookingwindow ,text = "Email ID").grid(row =6,column =0)
    Label(bookingwindow ,text = email).grid(row =6,column =1)

    Label(bookingwindow ,text = "Pick Up Address").grid(row =7,column =0),
    Entry(bookingwindow,textvariable = regFAdd_var).grid(row =7,column =1)

    Label(bookingwindow ,text = "Drop off Address:").grid(row =8,column =0)
    Entry(bookingwindow,textvariable = regTAdd_var).grid(row =8,column =1)

    Label(bookingwindow ,text = "Total Distance in KM").grid(row =9,column =0)
    Entry(bookingwindow,textvariable = regdist_var).grid(row =9,column =1)
    clicked.set( " Select your Ride! " )

    OptionMenu( bookingwindow, clicked , *caroptions ).grid(row =10,column =0)

    Label(bookingwindow ,text = "  \n   ").grid(row =11)

    Button( bookingwindow , text = " Calculate " , command = calculate).grid(row =12,column =0)
    Button( bookingwindow , text = " Continue " , command =booked).grid(row =12,column =1)

    

    bookingwindow.mainloop()


#Main funtion
loginpage()
