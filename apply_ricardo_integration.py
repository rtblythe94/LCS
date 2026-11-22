"""One-time safe patch for Robert's userInterface.py, only two button handlers.
Run INSIDE A COPY of your LCS project after copying ricardo_ui.py and book_services.py.
"""
from pathlib import Path
import shutil

file=Path('userInterface.py')
if not file.is_file():raise SystemExit('Error: run from the LCS project folder containing userInterface.py')
source=file.read_text(encoding='utf-8')
if 'Ricardo Systems 3 & 4' in source:
    print('Ricardo integration is already installed; no changes.');raise SystemExit(0)
old_manage='self.managebooks_button = self.custom_button(text = "manage books", master_container=widget_container)'
new_manage='self.managebooks_button = self.custom_button(text = "manage books", master_container=widget_container, command=lambda: self._open_ricardo_books("manage"))'
old_search='search_bar.pack(anchor="center")'
new_search=('search_bar.pack(anchor="center")\n'
'\t\t\t\t# Ricardo: launch book search from existing catalog\n'
'\t\t\t\tctk.CTkButton(widget_container,text="Search ISBN / Title / Author",command=lambda: self._open_ricardo_books("search")).pack(pady=5)')
method=('\t# Ricardo Systems 3 & 4 — book management and search popup\n'
'\tdef _open_ricardo_books(self, mode):\n'
'\t\tfrom ricardo_ui import open_book_window\n'
'\t\topen_book_window(self, mode=mode, database="books.csv")\n\n')
needle='\t## text bar generator'
checks={old_manage:1,old_search:1,needle:1}
for text,count in checks.items():
    if source.count(text)!=count:
        raise SystemExit(f'Cannot patch safely: expected {count} occurrence of {text!r}, found {source.count(text)}. No files changed.')
modified=source.replace(old_manage,new_manage).replace(old_search,new_search).replace(needle,method+needle)
import ast
ast.parse(modified)
backup=file.with_name('userInterface.py.before_ricardo.bak')
if backup.exists():raise SystemExit('Backup already exists. No files changed.')
shutil.copy2(file,backup)
file.write_text(modified,encoding='utf-8')
print('Integration applied. Backup at:',backup)
print('Manage Books button opens System 3; Book Catalog gets a Search button for System 4.')
