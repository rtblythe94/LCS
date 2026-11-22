"""CSC470 - Ricardo Systems 3 & 4. Nonintrusive CTk popup for book operations.
Requires book_services.py; all writes use the existing team books.csv.
"""
from __future__ import annotations
import csv
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from book_services import BookService, BookError


class BookToolsWindow(ctk.CTkToplevel):
    def __init__(self, master, mode='search', database='books.csv'):
        super().__init__(master)
        self.title('LCS — Book Management / Search')
        self.geometry('950x670')
        self.minsize(760, 530)
        self.service = BookService(Path(database))
        self.mode = mode
        self.transient(master)
        self.after(250, self.lift)
        self._build()
        self.refresh()

    def _build(self):
        ctk.CTkLabel(self, text='System 3 — Book Management' if self.mode == 'manage' else 'System 4 — Search Book',
                     font=('Arial', 23, 'bold')).pack(pady=(14, 7))
        frame = ctk.CTkFrame(self)
        frame.pack(fill='x', padx=15, pady=6)
        self.isbn = self._entry(frame, 'ISBN', 0, 0)
        self.title_entry = self._entry(frame, 'Title', 0, 1)
        self.author = self._entry(frame, 'Author', 0, 2)
        self.genre = self._entry(frame, 'Genre', 1, 0)
        ctk.CTkLabel(frame, text='Status').grid(row=1,column=1,sticky='w',padx=8)
        self.status = ctk.CTkOptionMenu(frame, values=['Available','Borrowed','Checked Out','On Hold','Unavailable'])
        self.status.grid(row=1,column=1,sticky='e',padx=8,pady=8)
        self.status.set('Available')
        for col in range(3): frame.grid_columnconfigure(col, weight=1)
        if self.mode == 'manage':
            actions = ctk.CTkFrame(self)
            actions.pack(fill='x', padx=15, pady=5)
            for title,cmd in [('Add Book',self.add),('Update Status',self.update),('Delete Book',self.delete),('Prepare ISBN / Status columns',self.prepare)]:
                ctk.CTkButton(actions,text=title,command=cmd,width=170).pack(side='left',padx=5,pady=6)
        search = ctk.CTkFrame(self)
        search.pack(fill='x',padx=15,pady=7)
        self.field = ctk.CTkOptionMenu(search,values=['title','author','isbn'])
        self.field.set('title');self.field.pack(side='left',padx=7,pady=8)
        self.query = ctk.CTkEntry(search,placeholder_text='Search text',width=260)
        self.query.pack(side='left',padx=7)
        self.query.bind('<Return>',lambda _e:self.search())
        self.sort = ctk.CTkOptionMenu(search,values=['title','author','isbn','status'])
        self.sort.set('title');self.sort.pack(side='left',padx=7)
        ctk.CTkButton(search,text='Search',width=100,command=self.search).pack(side='left',padx=5)
        ctk.CTkButton(search,text='Show all',width=90,command=self.refresh).pack(side='left',padx=5)
        self.notice = ctk.CTkLabel(self,text='',anchor='w')
        self.notice.pack(fill='x',padx=18,pady=3)
        host = ctk.CTkFrame(self)
        host.pack(fill='both',expand=True,padx=15,pady=(0,13))
        cols = ('ISBN','Title','Author','Genre','Status')
        self.tree=ttk.Treeview(host,columns=cols,show='headings')
        for col,width in [('ISBN',150),('Title',275),('Author',180),('Genre',120),('Status',120)]:
            self.tree.heading(col,text=col);self.tree.column(col,width=width,minwidth=60)
        yscroll=ttk.Scrollbar(host,orient='vertical',command=self.tree.yview)
        xscroll=ttk.Scrollbar(host,orient='horizontal',command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set,xscrollcommand=xscroll.set)
        self.tree.grid(row=0,column=0,sticky='nsew'); yscroll.grid(row=0,column=1,sticky='ns'); xscroll.grid(row=1,column=0,sticky='ew')
        host.grid_columnconfigure(0,weight=1);host.grid_rowconfigure(0,weight=1)
        self.tree.bind('<<TreeviewSelect>>',self._selected)

    def _entry(self,frame,label,row,col):
        sub=ctk.CTkFrame(frame,fg_color='transparent')
        sub.grid(row=row,column=col,sticky='ew',padx=6,pady=5)
        ctk.CTkLabel(sub,text=label).pack(anchor='w')
        item=ctk.CTkEntry(sub,placeholder_text=label)
        item.pack(fill='x')
        return item

    def _read_all(self):
        # The BookService itself validates CSV and supports changing column order.
        _,rows,_ = self.service._read()
        return rows

    def _display(self,rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            normalized={k.strip().casefold():v for k,v in r.items()}
            values=[normalized.get(key.casefold(),'') for key in ('ISBN','Title','Author','Genre','Status')]
            self.tree.insert('',tk.END,values=values)
        self.notice.configure(text=f'{len(rows)} book(s) displayed')

    def _selected(self,_event):
        selection=self.tree.selection()
        if not selection:return
        row=self.tree.item(selection[0])['values']
        for entry,value in [(self.isbn,row[0]),(self.title_entry,row[1]),(self.author,row[2]),(self.genre,row[3])]:
            entry.delete(0,tk.END);entry.insert(0,str(value))
        if row[4] in ['Available','Borrowed','Checked Out','On Hold','Unavailable']:self.status.set(row[4])

    def _perform(self,fn):
        try:
            result=fn()
        except (BookError,FileNotFoundError,OSError) as ex:
            messagebox.showerror('LCS Book Error',str(ex),parent=self)
            return None
        self.refresh()
        return result

    def refresh(self):
        self._perform_read()

    def _perform_read(self):
        try:self._display(self._read_all())
        except (BookError,FileNotFoundError,OSError) as ex: messagebox.showerror('LCS Book Error',str(ex),parent=self)

    def prepare(self):
        if not messagebox.askyesno('Confirm CSV schema upgrade','Create a backup and add ISBN and Status columns to books.csv? Existing ISBN values will remain blank.',parent=self):return
        result=self._perform(self.service.prepare_schema)
        if result is not None:messagebox.showinfo('CSV ready',f'Backup: {result}' if result else 'Columns already exist.',parent=self)

    def add(self):
        data={'isbn':self.isbn.get(),'title':self.title_entry.get(),'author':self.author.get(),
              'Genre':self.genre.get(),'status':self.status.get()}
        result=self._perform(lambda:self.service.add_book(data))
        if result is not None:messagebox.showinfo('Success','Book added.',parent=self)

    def update(self):
        result=self._perform(lambda:self.service.update_book_status(self.isbn.get(),self.status.get()))
        if result is not None:messagebox.showinfo('Success','Book status updated.',parent=self)

    def delete(self):
        isbn=self.isbn.get()
        if not messagebox.askyesno('Confirm delete',f'Delete book ISBN {isbn}?',parent=self):return
        result=self._perform(lambda:self.service.delete_book(isbn))
        if result is not None:messagebox.showinfo('Success','Book deleted.',parent=self)

    def search(self):
        try:
            rows=self.service.search_books(self.field.get(),self.query.get(),sort_by=self.sort.get())
            self._display(rows)
            if not rows:messagebox.showinfo('No results','No result found.',parent=self)
        except (BookError,FileNotFoundError,OSError) as ex:
            messagebox.showerror('Search error',str(ex),parent=self)


def open_book_window(master,mode='search',database='books.csv'):
    return BookToolsWindow(master,mode,database)
