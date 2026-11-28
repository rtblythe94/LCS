from PIL import Image
from CTkTable import CTkTable
import customtkinter as ctk
import user_services

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
				self.create_title(widget_container)
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
				
				## username text box
				text = "username"
				username_box = self.login_bar(text, widget_container)
				username_box.pack(pady=5)
				
				## password text box
				text = "password"
				password_box = self.login_bar(text, widget_container)
				password_box.pack(pady=5)
											
				##create login button
				##pack buttons to widget container
				self.login = self.custom_button(text = "login", master_container=widget_container, command=lambda: self.controller.login(username_box.get().strip(), password_box.get()))
				self.login.pack(pady=10)
						
				##pin exit button to bottom-right
				exit_button = self.custom_button(text="exit", master_container=self, command=self.controller.exit_app)
				exit_button.place(relx=1.0,rely=1.0,anchor="se",x=-10,y=-10)
					
				## account recovery button on login screen
				reset_pw_button = ctk.CTkButton(
					master=widget_container,
					width=180,
					height=30,
					text="Having trouble signing in?",
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
				self.create_title(widget_container)
				self.create_header("Welcome: " + str(self.controller.patron_manager.get_active_user()))
								
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
				logout_button = self.custom_button(text="Logout", master_container=self, command=self.controller.logout)
				logout_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				
####################################################################################
############## book catalog page ###################################################
####################################################################################					
			case "book_catalog":
				##create header
				self.create_header("Book Catalog")
														
				##pin return button to bottom-right
				logout_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				logout_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				

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
				self.create_title(widget_container)
				self.create_header("Welcome: " + str(self.controller.patron_manager.get_active_user()))
								
				##create image, then pack on top
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
								
				##create buttons
				##pack buttons to widget container
				self.managebooks_button = self.custom_button(text = "Manage Books", master_container=widget_container, command=lambda: self.controller.navigate("manage_books"))
				self.managebooks_button.pack(pady=10)
				self.managebooks_patrons = self.custom_button(text = "Manage Patrons", master_container=widget_container, command=lambda: self.controller.navigate("manage_patrons"))
				self.managebooks_patrons.pack(pady=10)
				self.createreports_button = self.custom_button(text="Create Reports", master_container=widget_container, command=lambda: self.controller.navigate("create_reports"))
				self.createreports_button.pack(pady=10)
				self.endDay_button = self.custom_button(text="End Day", master_container=widget_container, command=lambda: self.controller.navigate("end_day"))
				self.endDay_button.pack(pady=10)
								
				##pin logout button to bottom-right
				logout_button = self.custom_button(text="Logout", master_container=self, command=self.controller.logout)
				logout_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				
####################################################################################
############## book management page ################################################
####################################################################################									
			case "manage_books":
					##create title widget
				self.create_title(widget_container)
				self.create_header("Manage Books")
								
				# Ricardo System 3: in-page book management
				from ricardo_pages import render_book_management
				render_book_management(self, widget_container)

				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				
####################################################################################
############## patron management page ##############################################
####################################################################################	
			case "manage_patrons":
					##create title widget
				self.create_title(widget_container)
				self.create_header("Manage Patrons")
				self.results_frame = ctk.CTkFrame(master=widget_container, fg_color="transparent")
				self.results_frame.pack(pady=10)
				
				##create image, then pack on top
				open_book = ctk.CTkImage(
					Image.open("loginOpenBook.jpg"),
					size=(200,150)
					)
					
				open_book_label = ctk.CTkLabel(master=widget_container, image=open_book, text='')
				open_book_label.pack()
									
				
				## search text box
				text = "Search"
				search_box = self.login_bar(text, widget_container)
				search_box.pack(pady=5)						

				##pack buttons to widget container
				self.search = self.custom_button(text = "Search", master_container=widget_container, command=lambda: self.controller.search_patrons(search_box.get()))
				self.search.pack(pady=10)
				


				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
								
####################################################################################
############## create reports #####################################################
####################################################################################									
			case "create_reports":
					##create title widget
				self.create_title(widget_container)
				self.create_header("Create Reports")
								
				
				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)	
									
####################################################################################
############## end day #############################################################
####################################################################################									
			case "end_day":
					##create title widget
				self.create_title(widget_container)
				self.create_header("End Day")
								

				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)		
						
####################################################################################
############## move book page ######################################################
####################################################################################	
			case "move_book":
				##create header
				self.create_title(widget_container)
				self.create_header("Move Books")
								
				## pack accordian table
				option_list = ["economics","fiction","history","mathematics", "non-fiction", "philosophy", "science", "hold shelf"]
				
				## create book dropdown

				book_dropdown = self.create_dropdown(option_list, widget_container, text="-- select shelf move destination --")
	
				## insert button for accepting dropdown selection
				self.dropdown_accept = self.custom_button(text = "move book", master_container=widget_container)
				self.dropdown_accept.pack(pady=10)
				
				
				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				
####################################################################################
############## book return #########################################################
####################################################################################					
			case "return_book":
				##create header
				self.create_title(widget_container)
				self.create_header("Return Book")
								
														
				##pin return button to bottom-right
				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				
####################################################################################
############## patron & librarian user #############################################
####################################################################################	
			case "dual_usertype":
				##create title widget
				self.create_title(widget_container)
				self.create_header("Welcome: " + str(self.controller.patron_manager.get_active_user()))
								
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

				##create buttons
				##pack buttons to widget container
				self.managebooks_button = self.custom_button(text = "Manage Books", master_container=widget_container, command=lambda: self.controller.navigate("manage_books"))
				self.managebooks_button.pack(pady=10)
				self.managebooks_patrons = self.custom_button(text = "Manage Patrons", master_container=widget_container, command=lambda: self.controller.navigate("manage_patrons"))
				self.managebooks_patrons.pack(pady=10)
				self.createreports_button = self.custom_button(text="Create Reports", master_container=widget_container, command=lambda: self.controller.navigate("create_reports"))
				self.createreports_button.pack(pady=10)
				self.endDay_button = self.custom_button(text="End Day", master_container=widget_container, command=lambda: self.controller.navigate("end_day"))
				self.endDay_button.pack(pady=10)
								
				##pin logout button to bottom-right
				logout_button = self.custom_button(text="Logout", master_container=self, command=self.controller.logout)
				logout_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
					
####################################################################################
############## pay fines ###########################################################
####################################################################################					
			case "pay_fines":
				##create header
				self.create_title(widget_container)
				self.create_header("Pay Fines")
								
														
				##pin return button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)		
				
####################################################################################
############## recover email/password page #########################################
####################################################################################	
			case "recovery":
				##pin logout button to bottom-right
				return_button = self.custom_button(text="return", master_container=self,  command=self.controller.return_page)
				return_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
				
####################################################################################
####################################################################################
############## generators/widgets ##################################################
####################################################################################
####################################################################################	
	def display_patron_results(self, results):
		for widget in self.results_frame.winfo_children():
			widget.destroy()
			
		if not results:
			no_match = ctk.CTkLabel(master=self.results_frame, text= "No match found for ", font=("Times New Roman", 16), text_color="#000000")
			no_match.pack(pady=10)
			return
		table_data = [["ID", "Username", "Role"]] + [list(row) for row in results]

    # 4. Draw the CTkTable
		table = CTkTable(
			master=self.results_frame,
			values=table_data,
			header_color="#3f48cc",
			hover_color="#2980b9"
    )
		table.pack(pady=10, padx=10)
    		
	## text bar generator
	def text_bar(self, master_container=None, placeholder="Search", show=""):
		textBar = ctk.CTkEntry(
			master = master_container,
			placeholder_text = placeholder,
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
	
	## login bar for username and password
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
		
		if text == "password":
			loginBar.configure(show="*")
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
		
	## page title generator
	def create_title(self, master_container, text="LCS"):
		title_label = ctk.CTkLabel( master=master_container, text=text, font=("Times New Roman", 45, "bold"), text_color="#000000")
		title_label.pack()
		return title_label
		
	## page header generator
	def create_header(self, text):
		header_label = ctk.CTkLabel(master=self, text=text, font=("Times New Roman", 20, "bold"), text_color="#000000")		
		header_label.place(relx=0, rely=0, anchor="nw", x=10, y=8)
		return header_label
	
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
	
	
####################################################################################
############## cleanup #############################################################
####################################################################################

	##call to clear buttons for new page
	def clear_window(self):
		for widget in self.winfo_children():
			widget.destroy()

	def build_book_table(self, container):
		data = self.controller.load_book_database()
		table = CTkTable(master=container, row=len(data), column=len(data[0]), anchor="w", values=data)
		return table
		
	## create dialog box which displays passed message parameter
	def error_popup(self, message):
		dialog_box = ctk.CTkToplevel(self)
		dialog_box.title("Error")
		dialog_box.resizable(False, False)

		## dialog box dimensions
		box_width = 300
		box_height = 140
		
		## center dialog box to window
		self.update_idletasks()
		x = self.winfo_x() + (self.winfo_width() //2) - (box_width //2)
		y = self.winfo_y() + (self.winfo_height() //2) - (box_height //2)
		dialog_box.geometry(f"{box_width}x{box_height}+{x}+{y}")
		dialog_box.attributes("-topmost", True)
		dialog_box.grab_set()
				
		ctk.CTkLabel(dialog_box, text=message).pack(pady=(25,15))
		ok_button = self.custom_button(text="accept", master_container=dialog_box, command=dialog_box.destroy)
		ok_button.pack()
	
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
