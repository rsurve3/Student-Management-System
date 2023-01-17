from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
import socket
import bs4

# Connection
from sqlite3 import *
con = None
try:
	con = connect("sms.db")
	#print("connected")
except Exception as e:
	print("issue ", e)
finally:
	if con is not None:
		con.close()
		#print("disconnected")	

# Create Table
con = None
try:
	con = connect("sms.db")	
	#print("connected")
	cursor = con.cursor()
	sql = "create table student(rno int primary key, name text, marks int)"
	cursor.execute(sql)	
	#print("table created ")
except Exception as e:
	print("Table student exists")
finally:
	if con is not None:
		con.close()
		#print("disconected")

# Location
try:
	socket.create_connection( ("www.google.com", 80))
	res = requests.get("https://ipinfo.io/")
	data = res.json()	
	city_name = data['city']
	#print("city name ", city_name)		
except OSError as e:
	print("issue ", e)

# Weather
try:
	socket.create_connection( ("www.google.com", 80))
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address =  a1 + a2  + a3 		
	res = requests.get(api_address)
	data = res.json()
	main = data['main']
	temp1 = main['temp']
	#print("temp = ", temp1)

except OSError as e:
	print("issue ", e)
except KeyError as e1:
	print("check city name ", e1)

# Quote
try:
	socket.create_connection(("www.google.com", 80))

	res = requests.get("https://www.brainyquote.com/quote_of_the_day")

	soup = bs4.BeautifulSoup(res.text, "lxml")
	data = soup.find("img", {"class": "p-qotd"})

	msg = data['alt']
	#print(msg)

except Exception as e:
	print("issue ", e)

def f1():
	adst.deiconify()
	root.withdraw()

def f2():
	root.deiconify()
	adst.withdraw()

def f4(): 
	root.deiconify()
	vist.withdraw()

# View
def f3():
	stdata.delete(1.0,END)
	vist.deiconify()
	root.withdraw()
	con = None
	try:
		con = connect("sms.db")
		#print("connected")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "rno: " + str(d[0]) + " name: " + str(d[1]) + " marks: " + str(d[2]) + "\n"
		stdata.insert(INSERT, info)
	except Exception as e:
		print("select issue ", e)
	finally:
		if con is not None:
			con.close()
			#print("disconnected")

# Chart
def f12():
	con = None
	try:
		con = connect("sms.db")
		#print("connected")
		cursor = con.cursor()
		sql = "select name,marks from student order by marks desc limit 5"
		cursor.execute(sql)
		graph_data = cursor.fetchall()
		#print("graph data")

		data = []
		for d in graph_data:
			d1 = list(d)
			for i in d1:
				data.append(i)

		name = data[::2]
		marks = data[1::2]

		plt.bar(name, marks, color =['r','g','b'], width = 0.25)
		
		plt.xticks(name)
		plt.xlabel("Students")
		plt.ylabel("Marks")
		plt.title("Batch Information")
		
		plt.grid()
		plt.show()

	except Exception as e:
		print(e)

# Add
def f5():
	con = None
	try:
		con = connect("sms.db")
		print("connected")
		cursor = con.cursor()
		rno = int(entrno.get())
		if (rno <= 0):
			showwarning("failure", "Write correct roll no")
			return Exception
		if len(str(rno)) == 0:
			showerror("failure", "Dont leave blank")
			return Exception
		query = "select count(*) from student where rno = '%d'"
		c = (cursor.execute(query % rno).fetchone())
		check = list(c)
		if check[0] == 1:
			showwarning("failure","Rno already exists")
			return Exception
		name = entname.get()
		if len(name) == 1:
			showwarning("failure", "Write Correct name")
			return Exception
		if len(name) == 0:
			showerror("failure", "Dont leave blank")
			return Exception
		marks = int(entmarks.get())
		if (marks < 0) or (marks > 100):
			showwarning("failure", "Write Valid marks") 
			return Exception
		if (len(str(marks))) == '0' :
			showerror("failure", "Dont leave blank") 
			return Exception
		args = (rno, name, marks)
		cursor = con.cursor()
		sql = "insert into student values('%d' , '%s' , '%d')"	
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success", "Record added")
	except ValueError:
		showerror('Error',"Dont leave blank")
	except Exception as e:
		showerror("issue", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")


def f6():
	upst.deiconify()
	root.withdraw()

def f7():
	root.deiconify()
	upst.withdraw()

# Update
def f8():
	con = None
	try:
		con = connect("sms.db")
		print("connected ")
		rno1 = int(enturno.get())
		if (rno1 <= 0):
			showwarning("failure", "Write correct roll no")
			return Exception
		if len(str(rno1)) == 0:
			showerror("failure", "Dont leave blank")
			return Exception
		name1 = entuname.get()
		if (len(name1) == 1):
			showwarning("failure", "Write Correct name")
			return Exception
		if len(name1) == 0:
			showerror("failure", "Dont leave blank")
			return Exception
		marks1 = int(entumarks.get())
		if (marks1 < 0) or (marks1 > 100):
			showwarning("failure", "Write Valid marks") 
			return Exception
		if (len(str(marks1))) == '0' :
			showerror("failure", "Dont leave blank") 
			return Exception
		args = (name1 , marks1, rno1, )
		cursor = con.cursor()
		sql = "update student set name = '%s', marks = '%s' where rno = '%d' "
		cursor.execute(sql % args)
		if cursor.rowcount >= 1:
			con.commit()
			showinfo( "Success","Record updated")
		else:
			showerror("Error" , "Rno does not exist ")
	except ValueError as e:
		showerror('Error',"Dont leave blank")
	except Exception as e:
		showerror("issue ", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected ")


def f9():
	dlst.deiconify()
	root.withdraw()

def f10():
	root.deiconify()
	dlst.withdraw()

# Delete
def f11():
	try:
		con = connect("sms.db")
		print("connected ")
		rno2 = int(entdrno.get())
		if rno2 <= 0:
			showwarning("failure", "Write correct roll no")
			return Exception
		if (len(str(rno2))) == 0: 
			showerror("failure", "Dont leave blank")
			return Exception
		args = (rno2)
		cursor = con.cursor()
		sql = "delete from student where rno = '%d' "
		cursor.execute(sql % args)
		con.commit()
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("Success", "Record deleted")
		else:
			showerror("Error" , "Rno does not exist ")
	except ValueError as e:
		showerror('Error',"Dont leave blank")
	except Exception as e:
		showerror("issue ", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected ")


	

#design of root window --> SMS

root = Tk()
root.title("S. M. S. ")
root.geometry("800x600+400+200")
root.configure(background = "light green")

btnAdd = Button(root, text ="Add", font = ("arial",18,"bold"),width = 10, command = f1)
btnView = Button(root, text ="View", font = ("arial",18,"bold"),width = 10, command = f3)
btnUpdate = Button(root, text ="Update", font = ("arial", 18,"bold"),width = 10, command = f6)
btnDelete = Button(root, text ="Delete", font = ("arial", 18,"bold"),width = 10, command = f9)
btnCharts = Button(root, text ="Charts", font = ("arial", 18,"bold"),width = 10, command = f12)
lblLocation = Label(root, text="Location:" , font = ("arial",18,"bold"),width = 8)
TL = Text(root, height =1 ,width = 10,font = ("arial",18,"bold"))
TL.insert(END, city_name)
lblWeather = Label(root, text="Weather:" ,font = ("arial",18,"bold"),width = 8)
TT = Text(root, height =1 ,width = 10,font = ("arial",18,"bold"))
TT.insert(END, temp1)
lblQuote= Label(root, text="QOTD:" , font = ("arial",18,"bold"),width = 8)		
TQ = Text(root, height =3 ,width = 40,font = ("arial",18,"bold"))
TQ.insert(INSERT, msg)

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnCharts.pack(pady=10)
lblLocation.place(x=20,y=402)
TL.place(x=170,y=400)
lblWeather.place(x=470,y=402)
TT.place(x=620,y=400)
lblQuote.place(x=20,y=502)
TQ.place(x=170,y=500)

# design of adst window --> Add Student 

adst = Toplevel(root)
adst.title("Add Student ")
adst.geometry("500x400+400+200")
adst.configure(background = "light blue")
adst.withdraw()

lblrno = Label(adst, text="Enter Rno", font=("arial",18,"bold"))
entrno = Entry(adst, bd=5, font=("arial",18,"bold"))
lblname = Label(adst, text="Enter Name", font=("arial",18,"bold"))
entname = Entry(adst, bd=5, font=("arial",18,"bold"))
lblmarks = Label(adst, text="Enter Marks", font=("arial",18,"bold"))
entmarks = Entry(adst, bd=5, font=("arial",18,"bold"))
btnsave = Button(adst, text="Save", font=("arial",18,"bold"), command = f5)
btnback = Button(adst, text="Back", font=("arial",18,"bold"), command = f2)

lblrno.pack(pady=5)
entrno.pack(pady=5)
lblname.pack(pady=5)
entname.pack(pady=5)
lblmarks.pack(pady=5)
entmarks.pack(pady=5)
btnsave.pack(pady=5)
btnback.pack(pady=5)


#design of visit window --> View student

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("500x400+400+200")
vist.configure(background = "light yellow")
vist.withdraw()

stdata = ScrolledText(vist, width = 30, height = 20)
btnvback = Button(vist, text="Back", font=("arial",18,"bold"), command=f4)

stdata.pack(pady=10)
btnvback.pack(pady=10)


#design of update window --> update student

upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("500x400+400+200")
upst.configure(background = "sandy brown")
upst.withdraw()

lblurno = Label(upst, text="enter rno: ", font=("arial",18,"bold"))
enturno = Entry(upst, bd=5, font=("arial",18,"bold"))
lbluname = Label(upst, text="enter name: ", font=("arial",18,"bold"))
entuname = Entry(upst, bd=5, font=("arial",18,"bold"))
lblumarks = Label(upst, text="enter marks: ", font=("arial",18,"bold"))
entumarks = Entry(upst, bd=5, font=("arial",18,"bold"))
btnusave = Button(upst, text="Save", font=("arial",18,"bold"),command = f8)
btnuback = Button(upst, text="Back", font=("arial",18,"bold"), command = f7)

lblurno.pack(pady=5)
enturno.pack(pady=5)
lbluname.pack(pady=5)
entuname.pack(pady=5)
lblumarks.pack(pady=5)
entumarks.pack(pady=5)
btnusave.pack(pady=5)
btnuback.pack(pady=5)

#design of delete window --> delete student

dlst = Toplevel(root)
dlst.title("Delete Student ")
dlst.geometry("500x400+400+200")
dlst.configure(background = "light blue")
dlst.withdraw()

lbldrno = Label(dlst, text="enter rno", font=("arial",18,"bold"))
entdrno = Entry(dlst, bd=5, font=("arial",18,"bold"))
btndsave = Button(dlst, text="Delete", font=("arial",18,"bold"), command = f11)
btndback = Button(dlst, text="Back", font=("arial",18,"bold"), command = f10)

lbldrno.pack(pady=5)
entdrno.pack(pady=5)
btndsave.pack(pady=5)
btndback.pack(pady=5)

root.mainloop()