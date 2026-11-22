"""Open both Ricardo UI windows even while the team login UI is unfinished.
Run from the team's LCS project folder: python3 test_ui_ricardo.py
"""
import customtkinter as ctk
from ricardo_ui import open_book_window

root=ctk.CTk()
root.title('LCS — Ricardo Systems 3 & 4 Test Launcher')
root.geometry('470x260')
ctk.CTkLabel(root,text='Library Control System',font=('Arial',23,'bold')).pack(pady=(24,10))
ctk.CTkLabel(root,text='Test launcher — not a substitute for login/role authorization').pack(pady=7)
ctk.CTkButton(root,text='System 3: Book Management (Librarian)',width=340,
              command=lambda:open_book_window(root,mode='manage')).pack(pady=9)
ctk.CTkButton(root,text='System 4: Search Book (Patron / Librarian)',width=340,
              command=lambda:open_book_window(root,mode='search')).pack(pady=9)
root.mainloop()
