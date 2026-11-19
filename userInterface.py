from PIL import Image
from CTkTable import CTkTable
import customtkinter as ctk


class ManageUserInterface(ctk.CTk):
	def __init__(self):
		### initialize window on app start
		super().__init__()
		self.controller = None
		self.title("LCS")
		self.geometry("540x780")
		self.configure(fg_color="#FFFFFF")
	
	### pass the controller
	def set_controller(self, controller):
		self.controller = controller
		
	def switchUI(self, page):
		#clear old widgets before refreshing window
		self.clear_window()
		
		##create widget container that centers packed widgets 
		widget_container = ctk.CTkFrame(master=self, fg_color="transparent", width=540, height = 780)
		widget_container.place(relx=0.5, rely=0.5, anchor="center")
						
		### button grid for each page handled with match statement
		match page:
			
####################################################################################
############## login page ##########################################################
####################################################################################
			case "login":
				title_label = ctk.CTkLabel(
					master = widget_container,
					text="LCS",
					font=("Times New Roman", 45, "bold"),
					text_color=("#000000")
					)	
				title_label.pack()
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
				
				## username text box
				text= "username"
				username_box = self.login_bar(text, widget_container)
				username_box.pack(pady=5)
				
				## password text box
				text="password"
				password_box = self.login_bar(text, widget_container)
				password_box.pack(pady=5)
											
				##create login button
				##pack buttons to widget container
				self.login = self.custom_button(text = "login", master_container=widget_container, command=lambda: self.controller.navigate("patron_main"))

				self.login.pack(pady=10)
###!!!!! testing command setting only. change later to select usertype based on login credentials		
				
				##pin exit button to bottom-right
				exit_button = self.custom_button(text="exit", master_container=self, command=self.controller.exit_app)
				exit_button.place(
				relx=1.0,
				rely=1.0,
				anchor="se",
				x=-10,
				y=-10
				)
					
		
				reset_pw_button = ctk.CTkButton(
					master=widget_container,
					width=180,
					height=30,
					text="Forgot password?",
					font = ("Times New Roman", 14, "bold"),
					fg_color = "#ffffff",
					hover_color = "#2980b9",
					text_color = "#3f48cc",
					border_width = 3,
					border_color = "#ffffff")
				reset_pw_button.pack()
				
####################################################################################
############## patron main menu ####################################################
####################################################################################											
			case "patron_main":
				##create title widget
##fix title_label to have it's own method
				title_label = ctk.CTkLabel(
					master = widget_container,
					text="LCS",
					font=("Times New Roman", 45, "bold"),
					text_color=("#000000")
					)
				title_label.pack()
##fix header_label to have it's own method
				##create welcome header
				header_label = ctk.CTkLabel(
					master=None,
					#use when fully implemented
					#text="Welcome " + self.userName,
					text = "Welcome, Patron: RBlythe",
					font=("Times New Roman", 20, "bold"),
					text_color=("#000000")
					)
				header_label.place(	
					relx=0,
					rely=0,
					anchor="nw",
					x=10,
					y=8
					)
								
				##create image, then pack on top
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
								
				##create buttons
				##pack buttons to widget container
				self.button2 = self.custom_button(text = "Return Book", master_container=widget_container, command=lambda: self.controller.navigate("return_book"))
				self.button2.pack(pady=10)
				self.button1 = self.custom_button(text = "Book Catalog", master_container=widget_container, command=lambda: self.controller.navigate("book_catalog"))
				self.button1.pack(pady=10)
				self.button3 = self.custom_button(text="Pay Fines", master_container=widget_container, command=lambda: self.controller.navigate("pay_fines"))
				self.button3.pack(pady=10)
				
				##pin logout button to bottom-right
				logout_button = self.custom_button(text="Logout", master_container=self)
				logout_button.place(
				relx=1.0,
				rely=1.0,
				anchor="se",
				x=-10,
				y=-10
				)
				
####################################################################################
############## book catalog page ###################################################
####################################################################################					
			case "book_catalog":
				##create header
				header_label = ctk.CTkLabel(
					master=None,
					#use when fully implemented
					#text="Welcome " + self.userName,
					text = "Book Catalog",
					font=("Times New Roman", 20, "bold"),
					text_color=("#000000")
					)
				header_label.place(
					relx=0,
					rely=0,
					anchor="nw",
					x=10,
					y=8
					)
														
				##pin return button to bottom-right
				logout_button = self.custom_button(text="return", master_container=self)
				logout_button.place(
				relx=1.0,
				rely=1.0,
				anchor="se",
				x=-10,
				y=-10
				)
				
				search_bar = self.search_bar(widget_container)
				search_bar.pack(anchor="center")
				
## make this a table generator
		## create container for book table
				self.table_container = ctk.CTkScrollableFrame(
					master=widget_container,
					width=400,
					height=400,
					scrollbar_button_color="#3f48cc",
					scrollbar_button_hover_color="#2980b9",
					orientation="vertical"
					)
				self.table_container.pack(
					side="top",
					padx=20,
					expand=True,
					pady=(5,10)
				)	
				self.table_container.grid_columnconfigure(0, weight=1)
				## call load_book_database to build book table from 'book.csv'
				book_table = self.load_book_database(self.table_container)
				book_table.pack(side="top", fill="both")
			
				book_table.configure(
					hover_color="#333333"
				)
				
				## create book dropdown
				option_list = ["hold book","borrow book"]
				book_dropdown = self.create_dropdown(option_list, widget_container, text="-- select action --")
	
				## insert button for accepting dropdown selection
				self.dropdown_accept = self.custom_button(text = "accept", master_container=widget_container)
				self.dropdown_accept.pack(pady=10)
				
####################################################################################
############## librarian main page #################################################
####################################################################################	
			case "librarian_main":
					##create title widget
##fix title_label to have it's own method
				title_label = ctk.CTkLabel(
					master = widget_container,
					text="LCS",
					font=("Times New Roman", 45, "bold"),
					text_color=("#000000")
					)
				title_label.pack()
##fix header_label to have it's own method
				##create welcome header
				header_label = ctk.CTkLabel(
					master=None,
					#use when fully implemented
					#text="Welcome " + self.userName,
					text = "Welcome, Librarian: RBlythe",
					font=("Times New Roman", 20, "bold"),
					text_color=("#000000")
					)
				header_label.place(	
					relx=0,
					rely=0,
					anchor="nw",
					x=10,
					y=8
					)
								
				##create image, then pack on top
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
								
				##create buttons
				##pack buttons to widget container
				self.managebooks_button = self.custom_button(text = "manage books", master_container=widget_container)
				self.managebooks_button.pack(pady=10)
				self.managebooks_patrons = self.custom_button(text = "manage patrons", master_container=widget_container, command = lambda: setattr(self, "app_state", "book_catalog"))
				self.managebooks_patrons.pack(pady=10)
				self.createreports_button = self.custom_button(text="create reports", master_container=widget_container)
				self.createreports_button.pack(pady=10)
				self.endDay_button = self.custom_button(text="end day", master_container=widget_container)
				self.endDay_button.pack(pady=10)
								
				##pin logout button to bottom-right
				logout_button = self.custom_button(text="Logout", master_container=self)
				logout_button.place(
				relx=1.0,
				rely=1.0,
				anchor="se",
				x=-10,
				y=-10
				)
				
####################################################################################
############## book management page ################################################
####################################################################################									
			case "book_manage":
					##create title widget
##fix title_label to have it's own method
				title_label = ctk.CTkLabel(
					master = widget_container,
					text="LCS",
					font=("Times New Roman", 45, "bold"),
					text_color=("#000000")
					)
				title_label.pack()
##fix header_label to have it's own method
				##create welcome header
				header_label = ctk.CTkLabel(
					master=None,
					#use when fully implemented
					#text="Welcome " + self.userName,
					text = "Welcome, Librarian: RBlythe",
					font=("Times New Roman", 20, "bold"),
					text_color=("#000000")
					)
				header_label.place(	
					relx=0,
					rely=0,
					anchor="nw",
					x=10,
					y=8
					)
								
				##create image, then pack on top
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
								
				##create buttons
				##pack buttons to widget container
				self.managebooks_button = self.custom_button(text = "add book", master_container=widget_container)
				self.managebooks_button.pack(pady=10)
				self.managebooks_patrons = self.custom_button(text = "move book", master_container=widget_container, command = lambda: setattr(self, "app_state", "book_catalog"))
				self.managebooks_patrons.pack(pady=10)
				self.createreports_button = self.custom_button(text="remove book", master_container=widget_container)
				self.createreports_button.pack(pady=10)

				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self, command=self.contorller.go_back)
				return_button.place(
				relx=1.0,
				rely=1.0,
				anchor="se",
				x=-10,
				y=-10
				)
				
####################################################################################
############## move book page ######################################################
####################################################################################	
			case "move book":
##fix header_label to have it's own method
				##create welcome header
				header_label = ctk.CTkLabel(
					master=None,
					#use when fully implemented
					#text="Welcome " + self.userName,
					text = "Welcome, Librarian: RBlythe",
					font=("Times New Roman", 20, "bold"),
					text_color=("#000000")
					)
				header_label.place(	
					relx=0,
					rely=0,
					anchor="nw",
					x=10,
					y=8
					)
				## pack accordian table
				option_list = ["economics","fiction","history","mathematics", "non-fiction", "philosophy", "science", "hold shelf"]
				
				## create book dropdown

				book_dropdown = self.create_dropdown(option_list, widget_container, text="-- select shelf move destination --")
	
				## insert button for accepting dropdown selection
				self.dropdown_accept = self.custom_button(text = "move book", master_container=widget_container)
				self.dropdown_accept.pack(pady=10)
				
				
				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self, command=self.contorller.go_back)
				return_button.place(
				relx=1.0,
				rely=1.0,
				anchor="se",
				x=-10,
				y=-10
				)

	## text bar generator
	def text_bar(self, master_container=None):
		textBar = ctk.CTkEntry(
			master=master_container,
			placeholder_text="Search",
			#textvariable=text_variable,
			height=20,
			width=260,
			corner_radius=2,
			font=("Times New Roman", 14),
			border_width = 3,
			border_color = "#000000"
		)
		return textBar
	
	## search bar
	def search_bar(self, widget_container):
		search_row = ctk.CTkFrame(master=widget_container, fg_color="transparent")
		self.search_input = self.text_bar(master_container=search_row)
		 
		#create button for search
		self.submit_button = ctk.CTkButton(
			master=search_row,
			text="submit",
			height=20,
			width=80,
			corner_radius=2,
			font=("Times New Roman", 12, "bold"),
			fg_color="#3f48cc",
			hover_color="#2980b9",
			text_color = "#FFFFFF",
			border_width = 2,
			border_color = ("#000000")
		)
		self.search_input.pack(side="left", padx=(0,6))
		self.submit_button.pack(side="left")
		return search_row
	
	def login_bar(self, text, master_container):
		loginBar = ctk.CTkEntry(
			placeholder_text=text,
			master=master_container,
			#textvariable=text_variable,
			height=30,
			width=200,
			corner_radius=2,
			font=("Times New Roman", 14, "bold"),
			border_width = 3,
			text_color = "#000000",
			border_color = "#000000"
		)
		return loginBar
		
	##button generator	
	def custom_button(self, text, master_container=None, command=None):
		button = ctk.CTkButton(
			master=master_container,
			width=180,
			height=30,
			text=text,
			command=command,
			corner_radius = 10,
			font = ("Times New Roman", 18, "bold"),
			fg_color = "#3f48cc",
			hover_color = "#2980b9",
			text_color = "#FFFFFF",
			border_width = 3,
			border_color = "#000000")
		return button	
	
	##dropdown menu generator
	def create_dropdown(self, options, container=None, text=None):
		## create custom border frame for dropdown menus
		border_frame = ctk.CTkFrame(
			master=container,
			fg_color="#000000"
			)
		border_frame.pack(pady=5)
		## create dropdown menu
		dropdown = ctk.CTkOptionMenu(
			master=border_frame,
			width=240,
			values=options,
			anchor="center",
			fg_color="#ffffff",
			text_color="#000000",
			button_color = "#ffffff",
			dropdown_fg_color="#ffffff",
			button_hover_color="#2980b9",
			dropdown_text_color="#000000"
			)
			
		dropdown.set(text)
		dropdown.pack(padx=3, pady=3)
		return dropdown

	##accordian generator

	def decompress_accordian():
		if row_frame.is_expanded:
			table_frame.grid_forget()
			row_frame.is_expanded = False
			row_frame.configure(height=40)
		else:
			detail_frame.grid(row=1, column=0, sticky="ew")
			row_frame.is_expanded = True
			row_frame.configure(height=row_frame.winfo_reqheight() + detail_table.winfo_reqheight())
		accordian_header = ctk.CTKButton(
			row_frame,
			text="Fiction",
			anchor="w",
			font=("Times New Roman", 14, "bold"),
			height=40,
			width=ROW_WIDTH,
			fg_color="#3f48cc",
			hover_color="#2980b9"
				)
		accordian_header.grid(row=0, column=0, sticky="ew")
		row_frame.configure(height=40)
		return row_frame
	
	##call to clear buttons for new page
	def clear_window(self):
		for widget in self.winfo_children():
			widget.destroy()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
