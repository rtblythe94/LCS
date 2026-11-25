"""Ricardo's LCS Systems 3/4 embedded into Robert's existing CustomTkinter pages.
No new root window, no popup UI, no changes to controller navigation.
"""
from pathlib import Path
from tkinter import ttk, messagebox
import customtkinter as ctk
from book_services import BookService, BookError

BLUE = '#3f48cc'
WHITE = '#FFFFFF'
COLUMNS = ('ISBN', 'Title', 'Author', 'Genre', 'Status')


def _service():
    return BookService(Path(__file__).resolve().with_name('books.csv'))


def _button(parent, text, command, width=115):
    return ctk.CTkButton(parent, text=text, command=command, fg_color=BLUE,
                         hover_color='#2930a2', text_color=WHITE, width=width,
                         font=('Times New Roman', 13, 'bold'))


def _tree(parent, height=9):
    wrap = ctk.CTkFrame(parent, fg_color=WHITE)
    wrap.pack(fill='both', expand=True, padx=8, pady=(4, 6))
    style = ttk.Style()
    style.configure('LCS.Treeview', rowheight=25, font=('Times New Roman', 12),
                    background=WHITE, foreground='#111111', fieldbackground=WHITE)
    style.configure('LCS.Treeview.Heading', font=('Times New Roman', 12, 'bold'),
                    background=BLUE, foreground='#111111')
    tree = ttk.Treeview(wrap, columns=COLUMNS, show='headings', height=height, style='LCS.Treeview')
    for col in COLUMNS:
        tree.heading(col, text=col)
        tree.column(col, width={'ISBN':135,'Title':225,'Author':160,'Genre':120,'Status':105}[col], minwidth=95, stretch=False)
    vertical = ttk.Scrollbar(wrap, orient='vertical', command=tree.yview)
    horizontal = ttk.Scrollbar(wrap, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    tree.grid(row=0, column=0, sticky='nsew')
    vertical.grid(row=0,column=1,sticky='ns')
    horizontal.grid(row=1,column=0,sticky='ew')
    wrap.grid_rowconfigure(0, weight=1)
    wrap.grid_columnconfigure(0,weight=1)
    return tree


def _load_all(service):
    headers, rows, mapping = service._read()
    def val(row, field):
        col = mapping.get(field) if field != 'genre' else next((h for h in headers if h.strip().lower()=='genre'), None)
        return (row.get(col, '') if col else '') or ''
    return [tuple(val(r, key) for key in ('isbn','title','author','genre','status')) for r in rows]


def _fill(tree, rows, count_label):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)
    count_label.configure(text=f'{len(rows)} book(s) displayed')


def render_search_catalog(view, container):
    """Render System 4 INSIDE existing book_catalog page. Return/dropdown remain Robert's."""
    service = _service()
    panel = ctk.CTkFrame(container, fg_color=WHITE)
    panel.pack(fill='both', expand=True, padx=7, pady=(7, 3))
    ctk.CTkLabel(panel, text='Search Books', font=('Times New Roman', 18, 'bold'), text_color=BLUE).pack(pady=(3,6))
    first = ctk.CTkFrame(panel, fg_color=WHITE)
    first.pack(fill='x', padx=5, pady=(0,4))
    field = ctk.CTkOptionMenu(first, values=['title','author','isbn'], width=90,
                              fg_color=BLUE, button_color=BLUE, dropdown_fg_color=WHITE)
    field.pack(side='left', padx=(0,4))
    query = ctk.CTkEntry(first, placeholder_text='ISBN, title, or author', width=180)
    query.pack(side='left', padx=(0,4), expand=True, fill='x')
    sort_row = ctk.CTkFrame(panel, fg_color=WHITE)
    sort_row.pack(fill='x', padx=5, pady=(0,5))
    ctk.CTkLabel(sort_row, text='Sort by:', text_color='#111111').pack(side='left', padx=(0,4))
    sort = ctk.CTkOptionMenu(sort_row, values=['title','author','isbn','status'], width=115,
                             fg_color=BLUE, button_color=BLUE, dropdown_fg_color=WHITE)
    sort.pack(side='left', padx=(0,5))
    status = ctk.CTkLabel(panel, text='', text_color='#111111', anchor='w')
    status.pack(fill='x', padx=8)
    tree = _tree(panel, 8)

    def all_rows():
        try:
            rows = _load_all(service)
            idx = {'isbn':0,'title':1,'author':2,'status':4}[sort.get()]
            rows.sort(key=lambda x: str(x[idx]).casefold())
            _fill(tree, rows, status)
        except (BookError, OSError, ValueError) as exc:
            messagebox.showerror('Book Catalog', str(exc), parent=view)

    def search():
        try:
            results = service.search_books(field.get(), query.get(), sort_by=sort.get())
            headers, _, mapping = service._read()
            genre = next((h for h in headers if h.strip().lower() == 'genre'), None)
            rows = [tuple(r.get(mapping.get(k),'') if k != 'genre' and mapping.get(k) else (r.get(genre,'') if genre else '') for k in ('isbn','title','author','genre','status')) for r in results]
            _fill(tree, rows, status)
        except (BookError, OSError, ValueError) as exc:
            messagebox.showerror('Search Books', str(exc), parent=view)

    _button(sort_row, 'Search', search, width=90).pack(side='left', padx=2)
    _button(sort_row, 'Show all', all_rows, width=90).pack(side='left', padx=2)
    query.bind('<Return>', lambda _event: search())
    all_rows()


def render_book_management(view, container):
    """Render System 3 INSIDE existing manage_books page, without creating new windows."""
    service = _service()
    panel = ctk.CTkFrame(container, fg_color=WHITE)
    panel.pack(fill='both', expand=True, padx=7, pady=(2, 3))
    entries = {}
    for label, hint in [('ISBN','ISBN'), ('Title','Title'), ('Author','Author'), ('Genre','Genre')]:
        row = ctk.CTkFrame(panel, fg_color=WHITE)
        row.pack(fill='x', padx=8, pady=2)
        ctk.CTkLabel(row, text=label, width=75, anchor='w', text_color='#111111', font=('Times New Roman',12)).pack(side='left')
        input_box = ctk.CTkEntry(row, placeholder_text=hint)
        input_box.pack(side='left', fill='x', expand=True)
        entries[label.lower()] = input_box
    status_row = ctk.CTkFrame(panel, fg_color=WHITE)
    status_row.pack(fill='x', padx=8, pady=3)
    ctk.CTkLabel(status_row, text='Status', width=75, anchor='w', text_color='#111111').pack(side='left')
    status_menu = ctk.CTkOptionMenu(status_row, values=['Available','Borrowed','Checked Out','On Hold','Unavailable'],
                                    fg_color=BLUE, button_color=BLUE)
    status_menu.pack(side='left', fill='x', expand=True)
    button_row = ctk.CTkFrame(panel, fg_color=WHITE)
    button_row.pack(fill='x', padx=5, pady=4)
    count = ctk.CTkLabel(panel, text='', text_color='#111111', anchor='w')
    count.pack(fill='x', padx=8)
    tree = _tree(panel, 7)

    def refresh():
        try:
            _fill(tree, _load_all(service), count)
        except (BookError, OSError, ValueError) as exc:
            messagebox.showerror('Book Management', str(exc), parent=view)

    def action(kind):
        try:
            isbn = entries['isbn'].get().strip()
            if kind == 'add':
                service.add_book({**{k:w.get().strip() for k,w in entries.items()}, 'status':status_menu.get()})
                msg = 'Book added successfully.'
            elif kind == 'update':
                service.update_book_status(isbn, status_menu.get())
                msg = 'Book status updated.'
            else:
                if not messagebox.askyesno('Delete Book', f'Delete book with ISBN {isbn}?', parent=view):
                    return
                service.delete_book(isbn)
                msg = 'Book deleted successfully.'
            refresh()
            messagebox.showinfo('Book Management', msg, parent=view)
        except (BookError, OSError, ValueError) as exc:
            messagebox.showerror('Book Management', str(exc), parent=view)

    for name, callback in [('Add Book',lambda:action('add')),
                            ('Update Status',lambda:action('update')),
                            ('Delete Book',lambda:action('delete'))]:
        _button(button_row, name, callback, width=130).pack(side='left', padx=2, expand=True)

    def prepare():
        if not messagebox.askyesno('Prepare Database', 'Add ISBN and Status columns if missing? A backup is created. Only run on a test copy.', parent=view):
            return
        try:
            backup = service.prepare_schema()
            refresh()
            messagebox.showinfo('Database', 'Columns ready.' + (f' Backup: {backup}' if backup else ' Already prepared.'), parent=view)
        except (BookError,OSError,ValueError) as exc:
            messagebox.showerror('Prepare Database', str(exc), parent=view)

    _button(panel,'Prepare ISBN / Status columns (test copy only)',prepare, width=360).pack(pady=(0,4))
    refresh()
