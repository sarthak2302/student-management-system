from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
import os
import smtplib
import random
import time
from email.message import EmailMessage
import hashlib as hl

class student():
    def __init__(self):
        self.root=Tk()
        self.root.configure(background='silver')
        self.root.title('Student Management system')
        self.root.geometry('1600x900')  #W x H
        
        title=Label(self.root,text='STUDENT MANAGEMENT SYSTEM',bd=10,relief='ridge',font=('calibri',40,"bold"),bg="black",fg='silver')
        title.pack(side="top",fill=X) 
        #=====ALL VARIABLES======#
        self.name_var=StringVar()
        self.email_var=StringVar()
        self.gender_var=StringVar()
        self.contact_var=StringVar()
        self.dob_var=StringVar()
        self.address_var=StringVar()
        self.search_by=StringVar()
        self.search=StringVar()
        
        #======manange frame======#
        Manage_frame=Frame(self.root,bd=4,relief=RIDGE,bg='grey')
        Manage_frame.place(x=20,y=120,width=500,height=630)

        mngstd=Label(Manage_frame,text="MANAGE STUDENTS",bg='grey',font=('calibri',30,'bold'),bd=2)
        mngstd.grid(row=1,column=0,columnspan=2,padx=45,pady=10)

        roll=Label(Manage_frame,text="ROLLNO",bg='grey',font=('calibri',15))
        roll.grid(row=2,column=0,sticky='w',padx=10,pady=10)
        
        name=Label(Manage_frame,text="NAME",bg='grey',font=('calibri',15))
        name.grid(row=3,column=0,sticky='w',padx=10,pady=10)
        
        email=Label(Manage_frame,text="EMAIL",bg='grey',font=('calibri',15))
        email.grid(row=4,column=0,sticky='w',padx=10,pady=10)
        
        gender=Label(Manage_frame,text="GENDER",bg='grey',font=('calibri',15))
        gender.grid(row=5,column=0,sticky='w',padx=10,pady=10)
        
        contact=Label(Manage_frame,text="CONTACT NO.",bg='grey',font=('calibri',15))
        contact.grid(row=6,column=0,sticky='w',padx=10)
        
        dob=Label(Manage_frame,text="D.O.B",bg='grey',font=('calibri',15))
        dob.grid(row=7,column=0,sticky='w',padx=10,pady=10)
        
        address=Label(Manage_frame,text="ADDRESS",bg='grey',font=('calibri',15))
        address.grid(row=8,column=0,sticky='w',padx=10,pady=10)
        
        #=====ENTRY======#
        self.roll_e=Entry(Manage_frame,width=40,font=('calibri',10)) #textvariable is used ki us entry field ki value acces krne k lie roll_var use kr paenge hum
        self.roll_e.grid(row=2,column=1,pady=12)

        name_e=Entry(Manage_frame,textvariable=self.name_var,width=40,font=('calibri',10))
        name_e.grid(row=3,column=1,pady=12)

        email_e=Entry(Manage_frame,textvariable=self.email_var,width=40,font=('calibri',10))
        email_e.grid(row=4,column=1,pady=12)

        gender_e=ttk.Combobox(Manage_frame,width=37,textvariable=self.gender_var,font=('calibri',10))
        gender_e['value']=('male','female','other')
        gender_e.grid(row=5,column=1,sticky='w',padx=1,pady=12)

        contact_e=Entry(Manage_frame,width=40,textvariable=self.contact_var,font=('calibri',10))
        contact_e.grid(row=6,column=1,pady=12)

        dob_e=Entry(Manage_frame,textvariable=self.dob_var,width=40,font=('calibri',10))
        dob_e.grid(row=7,column=1,pady=12)

        self.address_e=Text(Manage_frame,width=40,height=2,font=('calibri',10))   #text k lie koi textvaribale nhi hota to self laga k directly acces krenge usko
        self.address_e.grid(row=8,column=1,pady=22)
        
        #====BUTTON=====#
        button_frame=Frame(Manage_frame,bd=4,relief='sunken',bg='white')
        button_frame.place(x=18,y=500,width=410,height=49)

        add=Button(button_frame,height=2,width=13,text="ADD",command=self.add_students)
        add.grid(row=0,column=0)
        
        update=Button(button_frame,height=2,width=13,command=self.update,text="UPDATE")
        update.grid(row=0,column=1)
        
        delete=Button(button_frame,height=2,width=13,text="DELETE",command=self.delete)
        delete.grid(row=0,column=2)
        
        clear=Button(button_frame,width=13,height=2,command=self.clear,text="CLEAR")
        clear.grid(row=0,column=3)

        #====detail frame=====#
        Detail_frame=Frame(self.root,bd=4,relief=RIDGE,bg='grey')
        Detail_frame.place(x=560,y=120,width=930,height=630)

        lblSearch=Label(Detail_frame,text='Search_By',bg='grey',fg='white',font=('Arial',20,'bold'))
        lblSearch.grid(row=0,column=0,pady=10,padx=20,sticky='w')

        self.combo_search=ttk.Combobox(Detail_frame,width=15,font=('calibri',10),textvariable=self.search_by)
        self.combo_search['value']=('Rollno','Name','Contact')
        self.combo_search.grid(row=0,column=1,sticky='w',padx=10)

        txt_search=Entry(Detail_frame,width=20,text='Enter value',font=('calibri',10),textvariable=self.search)
        txt_search.grid(row=0,column=2,pady=10,padx=10)

        search=Button(Detail_frame,height=1,width=13,text="SEARCH",command=self.search_student)
        search.grid(row=0,column=3,padx=10)        

        showall=Button(Detail_frame,height=1,width=13,command=self.fetch_data,text="SHOW ALL")
        showall.grid(row=0,column=4,padx=10)       

        #=====TABLE FRAME======#
        Table_frame=Frame(Detail_frame,bg='black',bd=4)
        Table_frame.place(x=22,y=90,width=870,height=490)

        scroll_x=Scrollbar(Table_frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_frame,orient=VERTICAL)

        self.Student_table=ttk.Treeview(Table_frame,columns=('roll','name','email','gender','contact','dob','address'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)   #fill=X poore x axis mai faila dega 
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        self.Student_table.heading('roll',text='ROLL NO')
        self.Student_table.heading('name',text='Name')
        self.Student_table.heading('email',text='Email')
        self.Student_table.heading('gender',text='Gender')
        self.Student_table.heading('contact',text='Contact')
        self.Student_table.heading('dob',text='D.O.B')
        self.Student_table.heading('address',text='Address')
        self.Student_table['show']='headings'   #shows only the address else a staring column will be by default madde
        self.Student_table.column('roll',width=24)
        self.Student_table.column('name',width=100)
        self.Student_table.column('email',width=200)
        self.Student_table.column('gender',width=100)
        self.Student_table.column('contact',width=100)  
        self.Student_table.column('dob',width=100)
        self.Student_table.column('address',width=200)
        self.Student_table.pack(fill=BOTH,expand=1)  #to apply fill expand is used
        self.Student_table.bind("<ButtonRelease-1>",self.get_cursor)   #this will help to perform the action self.get_cursor when button is released of mouse search it on internet for better..
        self.fetch_data()

    def add_students(self):
        if self.name_var.get()=='' or self.email_var.get()=='' or self.gender_var.get()=='' or self.contact_var.get()=='' or self.dob_var.get()=='' or self.address_e.get('1.0',END)=='':
            messagebox.showerror('Error','!!All fields are required!!')
        else:
            messagebox.showinfo('Success','Data added succesfully')
            conn=pymysql.connect(host='localhost',user='root',password='',database='college')
            c=conn.cursor()
            c.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                        self.roll_e.get(),
                                                                        self.name_var.get(),               
                                                                        self.email_var.get(),
                                                                        self.gender_var.get(),
                                                                        self.contact_var.get(),
                                                                        self.address_e.get('1.0',END)    #(line no till END)
                                                                        )
                                                                        )
            conn.commit()
            self.fetch_data()
            self.clear()
            conn.close()

    def fetch_data(self):
        conn=pymysql.connect(host='localhost',user='root',password='',database='college')
        c=conn.cursor()
        c.execute("select * from student")
        rows=c.fetchall()
        if len(rows)!=0:
            self.Student_table.delete(*self.Student_table.get_children() )   #delete all the table data
            for row in rows:
                self.Student_table.insert('',END,values=row)
                conn.commit()
        self.clear()
        conn.close()
        
    def clear(self):
        self.roll_e.delete(0,END)
        self.name_var.set("")
        self.email_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")
        self.dob_var.set("")
        self.address_e.delete("1.0",END)      #1st line se end tak data delete hojaenge
        self.search_by.set("")
        self.search.set('')
        

    def get_cursor(self,self2):
        global select_row
        cursor_row=self.Student_table.focus()  #cursor_row mai row select hojaegi
        contents=self.Student_table.item(cursor_row)   #data cursor row ka contents mai aajaega
        select_row=contents['values']   #value ko fetch krlenge
        
        conn=pymysql.connect(host='localhost',user='root',password='',database='college')
        c=conn.cursor()
        self.roll_e.delete(0,END)
        self.roll_e.insert("0",select_row[0])
        self.name_var.set(select_row[1])               
        self.email_var.set(select_row[2])
        self.gender_var.set(select_row[3])
        self.contact_var.set(select_row[4])
        self.dob_var.set(select_row[5])
        self.address_e.delete("1.0",END)
        self.address_e.insert(END,select_row[6])
        conn.close()
        
    def update(self):
        if self.roll_e.get()=="" or self.name_var.get()=='' or self.email_var.get()=='' or self.gender_var.get()=='' or self.contact_var.get()=='' or self.dob_var.get()=='' or self.address_e.get('1.0',END)=='':
            messagebox.showerror('Error','!!All fields are required!!')
        else:
            messagebox.showinfo('Succes','Update succesfull')
            conn=pymysql.connect(host="localhost",password='',user='root',database="college")
            c=conn.cursor()
            c.execute("update student set Rollno=%s,Name=%s,Email=%s,Gender=%s,Contact=%s,DOB=%s,Address=%s where Rollno = %s",(
                                                                        self.roll_e.get(),
                                                                        self.name_var.get(),               
                                                                        self.email_var.get(),
                                                                        self.gender_var.get(),
                                                                        self.contact_var.get(),
                                                                        self.dob_var.get(),
                                                                        self.address_e.get('1.0',END),
                                                                        self.roll_e.get()
                                                                        ))
            
            conn.commit()
            self.clear()
            self.fetch_data()
            conn.close()

    def delete(self):
        if select_row=='':
            messagebox.showerror('Error','Select row to delete')
        else:
            messagebox.showinfo('Succes','Data deleted succesfully')
            conn=pymysql.connect(host="localhost",password='',user='root',database="college")
            c=conn.cursor()     
            c.execute("delete from student where Rollno=%s",(self.roll_e.get()))
            conn.commit()
            self.clear()
            self.fetch_data()
            conn.close()


    def search_student(self):
        if self.search_by.get() =='' and self.search.get()=='':
            messagebox.showerror('Error','enteries are not filled')
        else:
            conn=pymysql.connect(host="localhost",password='',user='root',database="college")
            c=conn.cursor()
            c.execute('select * from student where '+self.search_by.get()+'  = %s ',(self.search.get()))
            rows=c.fetchall()
            self.Student_table.delete(*self.Student_table.get_children())

            for row in rows:
                self.Student_table.insert('',END,values=row)
                conn.commit()
            conn.close()


class login():
    def __init__(self):
        global top
        top=Tk()
        top.geometry('410x400')
        top.configure(background='silver')
        
        my_l=Label(top,text='Welcome To Student Management System',fg='black',bg='grey',height=2,font=('Calibri',17,'bold'))
        my_l.place(x=-1,y=0)
        
        my_id=Label(top,text='EMAIL',fg='black',font=('Calibri',15,'bold'),bg='silver')
        my_id.place(x=110,y=150,width=50)

        self.my_ide=Entry(top)
        self.my_ide.place(x=170,y=155,width=170)

        self.my_pswrd=Label(top,text='PASSWORD',fg='black',bg='silver',font=('Calibri',15,'bold'))
        self.my_pswrd.place(x=65,y=190)
        
        self.my_pswrde=Entry(top,width=20)
        self.my_pswrde.place(x=170,y=195,width=170)

        ##Label(top,text='Spaces are counted',bg='silver',font=('calibri',20,'bold'))
        self.login_btn=Button(top,text="Log In",bg='goldenrod',fg='black',font=('calibri',12,'bold'),relief='raised',bd=3,width=10,command=lambda:self.login_button(top)).place(x=170,y=240)

        forgot_button=Button(top,text='forgot password??',fg='black',bd=0,bg='silver',font=('calibri',10,'bold'),command=lambda:self.email_verification(top))
        forgot_button.place(x=160,y=290)

    def login_button(self,top):
        conn=pymysql.connect(host='localhost',user='root',password='',database='college')
        c=conn.cursor()
        c.execute('select Password,Email from teachers where Email=%s',(str(self.my_ide.get())))
        rows=c.fetchall()

        p = hl.md5(self.my_pswrde.get().lower().encode())
        p = p.hexdigest()
        
        try:
            if(p==rows[0][0] and self.my_ide.get().lower()==rows[0][1]):
                top.destroy()
                obj=student()
        except:
            messagebox.showerror('Error','wrong id or password')
            
    otp=0
    def email_verification(self,top):
        for widget in top.winfo_children():
            widget.destroy()
            
        
        my_id=Label(top,text='Enter your Email',fg='black',font=('Calibri',15,'bold'),bg='silver')
        my_id.place(x=30,y=150)

        self.my_ide=Entry(top)
        self.my_ide.place(x=180,y=155,width=190)
        
        self.send_otp_btn=Button(top,text="Send OTP",bg='goldenrod',fg='black',font=('calibri',12,'bold'),relief='raised',bd=3,command=lambda:self.send_email(self.my_ide.get(),top))
        self.send_otp_btn.place(x=170,y=200)    
                
    def send_email(self,x,top):
        self.error_lbl=Label(top,text='',bg='silver',font=('calibri',10,'bold'))
        self.error_lbl.place(x=200,y=120)
        conn=pymysql.connect(user='root',host='localhost',password='',database='college')
        c=conn.cursor()
        c.execute('select * from teachers where Email = %s',(x))
        data=c.fetchall()
        

        if x=='':
            self.error_lbl=Label(top,text='Enter Required',bg='silver',font=('calibri',10,'bold'))
            self.error_lbl.place(x=200,y=120)
        elif data==():
            self.error_lbl.destroy()
            self.error_lbl=Label(top,text='Invalid Email',bg='silver',font=('calibri',10,'bold'))
            self.error_lbl.place(x=200,y=120)
            
        else:
            self.user_email=x
            for widget in top.winfo_children():
                widget.destroy()
                
            self.send_otp(self.user_email)        
            
        conn.commit()
        conn.close()
                
    
    def send_otp(self,mail):
        global otp
                    
        self.otp_txt=Entry(top)
        self.otp_txt.place(x=200,y=155,width=190)
        
        self.otp_lbl=Label(top,text='Enter otp send to your mail',bg='silver',font=('calibri',12,'bold'))
        self.otp_lbl.place(x=5,y=152)

        confirm_button=Button(top,text="CONFIRM",bg='goldenrod',fg='black',font=('calibri',12,'bold'),relief='raised',bd=3,command=self.change_password)
        confirm_button.place(x=120,y=200)

        send_otp_again=Button(top,text="Send OTP Again",bg='goldenrod',fg='black',font=('calibri',12,'bold'),relief='raised',bd=3,command=lambda:self.send_otp(self.user_email))
        send_otp_again.place(x=230,y=200)
        
        for i in range(0,5):    
            n = random.randint(1,9)
            self.otp=(10**i)*n + self.otp


        email_address=os.environ.get('EMAIL_ADDRESS')
        email_pswrd=os.environ.get('EMAIL_PASSWORD')
        msg=EmailMessage()
        msg['From']=email_address
        msg['Subject']='OTP LOGIN'
        msg['To']=str(mail)
        msg.set_content('Your foget otp passwrod is '+str(self.otp) + ' .')
        
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as connection:
            connection.login(email_address,email_pswrd)
            connection.send_message(msg)
            connection.quit()
    def change_password(self):
        if str(self.otp_txt.get()) == str(self.otp):
            for widget in top.winfo_children():
                widget.destroy()
            my_pswrd=Label(top,text='NEW PASSWORD',bg='silver',font=('calibri',15,'bold')).place(x=50,y=170)
            my_confirm_pswrd=Label(top,text='CONFIRM PASSWORD',bg='silver',font=('calibri',15,'bold')).place(x=50,y=200)
            
            my_pswrde=Entry(top)
            my_confirm_pswrde=Entry(top)
            
            my_confirm_pswrde.place(x=250,y=205)
            my_pswrde.place(x=250,y=175)

            my_change_btn=Button(top,text='Change',bg='goldenrod',fg='black',font=('calibri',12,'bold'),relief='raised',bd=3,command=lambda:self.password_changed(my_pswrde.get(),my_confirm_pswrde.get() ) )
            my_change_btn.place(x=170,y=240)
        else:
            messagebox.showerror('ERROR','OTP INVALID')
        
    def password_changed(self,x,y):
        conn=pymysql.connect(host='localhost',user='root',password='',database='college')
        c=conn.cursor()

        if x==y and len(x)>5:
            x = hl.md5(x.encode())
            c.execute('update teachers set Password=%s where Email=%s',(x.hexdigest(),self.user_email))
            messagebox.showinfo('change password','Password updated succesfully')
            top.destroy()
            l=login()
        elif len(x)<5:
            messagebox.showerror('ERROR','password length should be > 5')
        else:
            messagebox.showerror('ERROR','Passwords incorrect')
        conn.commit()
        conn.close()
    
l=login()
