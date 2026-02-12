
from tkinter import*
import customtkinter

root = customtkinter.CTk()
root.title('Astronomy simulation')
root.geometry('600x350')



#set the color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")\

def submit():
    my_label.configure()
    pass

#the method for clearing the button so we can put next thing 

def clear():
    my_entry.delete(0,END)

#the entry box for the users input

my_entry = customtkinter.CTkEntry(root, placeholder_text="Enter the date and location",  height=100, width=250 )

my_entry.place(relx=0.5,rely=0.6,anchor="center")

#the submition button which needs to be connceted to the pre-definied function submit
my_button = customtkinter.CTkButton(root,text="Start simulation",command=submit)
my_button.place(relx=0.5,rely=0.85,anchor="center")




root.mainloop()

"""""
class App(Tk):

	def __init__(self):
		super().__init__()

		# Title, icon, size
		self.title("Tkinter.com - Object Oriented Programming!")
		self.iconbitmap('images/codemy.ico')
		self.geometry('700x450')

		# Create Status Variable
		self.status = True

		# Create some widgets
		self.my_label = Label(self, text="Hello World!", font=("Helvetica", 42))
		self.my_label.pack(pady=20)

		self.my_button = Button(self, text="Change Text", command=self.change)
		self.my_button.pack(pady=20)

		# Create a frame outside this function
		My_frame(self)

	def change(self):
		if self.status == True:
			self.my_label.config(text="Goodbye World!")
			self.status = False
		else:
			self.my_label.config(text="Hello World!")
			self.status = True

class My_frame(Frame):
	def __init__(self, parent):
		super().__init__(parent)

		# Put this sucker on the screen
		self.pack(pady=20)
		# Create a few buttons
		self.my_button1 = Button(self, text="Change", command=parent.change)
		self.my_button2 = Button(self, text="Change", command=parent.change)
		self.my_button3 = Button(self, text="Change", command=parent.change)

		self.my_button1.grid(row=0, column=0, padx=10)
		self.my_button2.grid(row=0, column=1, padx=10)
		self.my_button3.grid(row=0, column=2, padx=10)




# Define and instantiate our app
app = App()
app.mainloop()

print("Hello world")
"""