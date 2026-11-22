LCS Ricardo Systems 3 & 4 — UI integration guide (Python 3.13)

IMPORTANT: Work in a COPY of the LCS project; do not modify or push to your teammates' live branch.

1. Download/clone the team's full LCS project (it must contain main.py, controller.py, userInterface.py, books.csv and loginOpenBook.jpg).
2. Make a folder-copy of the project named LCS-test.
3. Put these 3 files IN LCS-test alongside main.py:
      book_services.py
      ricardo_ui.py
      apply_ricardo_integration.py
4. Open Terminal in LCS-test and run:
      python3 -m pip install customtkinter pillow CTkTable
      python3 apply_ricardo_integration.py
      python3 main.py
5. On the librarian main menu, click 'manage books' to open System 3.
   On the patron Book Catalog, click 'Search ISBN / Title / Author' to open System 4.
   Note: the current login screen in Robert's version is only a prototype and routes directly to Patron. To test the librarian screen, Robert must enable librarian login/navigation; do not mistake the prototype login for real authentication.
   If the prototype login prevents reaching Librarian, instead run:
      python3 test_ui_ricardo.py
   This opens a dedicated TEST LAUNCHER with buttons for both modules.
6. For the first librarian test, use 'Prepare ISBN / Status columns' ON THE TEST COPY only.
   This backs up books.csv and adds blank ISBN fields and Available status.
   No ISBNs are invented. Use test book ISBN '978-1260423310', title 'Algorithms', author 'Brown'.
7. Test: Add book; Search ISBN / Title / Author; Sort results; Test no results; update status; delete book (set status Available first).
8. Capture screenshots (macOS Command+Shift+4) and fill each rubric row with results and Y/N.
9. Share the tested files / patch with Robert to integrate into his final code. The script creates a backup of userInterface.py.

LIMITATIONS:
- The popup is an integration adapter, not a replacement for the complete UI.
- Existing CSV book records lack real ISBNs; ISBN searches match only records you populate.
- Authentication/role protection is NOT implemented by this adapter; real role enforcement must be added by Robert before deployment.
- This should not be called a completed end-to-end integration until tested on the team's local app.
