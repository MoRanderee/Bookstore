'''
Function definitions:
'''

def id_exists(id, cursor):

    cursor.execute('''SELECT id FROM books WHERE id = ?''', (id,))

    keys = cursor.fetchall()

    if len(keys) == 0:

        return False
    
    else:
        return True

'''
Alternate method:
'''
# def id_exists(id, cursor):

#     cursor.execute('''SELECT id FROM books''')

#     key_list = []

#     for key in keys:
#         key = str(key)
#         key = key[1:-2]

#         if id == key:
#             return True
        
#     return False

from tabulate import tabulate

# Creating and connecting to the DB
import sqlite3
db = sqlite3.connect('ebookstore_db.db')
cursor = db.cursor()  # Get a cursor object

# Create the table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY, 
        Title TEXT,
        Author TEXT,
        Qty INTEGER)
''')

# commit to create table
db.commit()

# Insert new data into table
book_info = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

cursor.executemany('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''',
                   book_info)

# commit used to insert new records
db.commit()

menu = ''

while menu != '0':
    '''
    Try/Except block used to repeatedly display the options and to present the user with error messages if necesssary.
    '''
    try:

        menu = input('''
Please select option below:
1. Enter  book
2. Update book
3. Delete book
4. Search books
0. Exit
''')

        if menu == '0':
            '''
            This option allows the user to exit the program

            Must drop the table each time since im inserting IDs that already exist when i run the program.
            This should not be a problem if i allow the table to insert its own default ID values (starting at 1)
            '''

            cursor.execute('''DROP TABLE books''')
            db.close()
            print("Program has been closed.")
            
            break
            
        elif menu == '1':
            '''
            This option allows the user to enter add a new book to the table in the DB
            '''

            # Request info of new books
            name = input("Enter title of book:\n")
            author = input("Enter author of book:\n")
            qty = int(input("Enter the stock quantity:\n"))

            # If i dont specify an ID value to insert, it will automatically increase the value of the ID for the next record
            cursor.execute('''INSERT INTO books(Title, Author, Qty) VALUES(?,?,?)''',
                   (name, author, qty))
            
            # commit to add new data
            db.commit()
            print("New book has been added.")

        elif menu == '2':
            '''
            This option allows the user to change the info of a book using its ID. The user will first view all the books and their IDs. 
            The user can then adjust the book's title, author or stock quanitity.
            '''

            # Display all books in table
            cursor.execute('''SELECT * FROM books''')
            book_info = cursor.fetchall()
            book_info.insert(0, ("ID", "Title", "Author", "Quantity"))

            print(tabulate(book_info, headers='firstrow', tablefmt='fancy_grid'))
            
            # Request the user to enter the ID of the book they want to delete
            id = input("Please enter the ID of the book you would like to update:\n")

            # check if ID exists in the table:
            if id_exists(id, cursor) == True:
                pass

            else:
                raise Exception("This book ID does not exist.")

            change = input('''
What would you like to change?

1. Title
2. Author
3. Stock quantity
''')

            if change == '1':
                title = input("Please enter the new title of this book:\n")
                cursor.execute('''IF EXISTS UPDATE books SET Title = ? WHERE id = ? ''', (title, id))
                print('Book data updated!')

            elif change == '2':
                author = input("Please enter the new author of this book:\n")
                cursor.execute('''UPDATE books SET Author = ? WHERE id = ? ''', (author, id))
                print('Book data updated!')

            elif  change == '3':
                stock = int(input("Please enter the new stock quantity of this book:\n"))
                cursor.execute('''UPDATE books SET Qty = ? WHERE id = ? ''', (stock, id))
                print('Book data updated!')

            else: 
                raise Exception("Incorrect option selected!")
        
        elif menu == '3':
            """
            This menu option allows the user to delete any book from the DB using the ID of the book.
            The user is first provided with a list of all the books and their ID's.
            """
            
            # Display all books in table
            cursor.execute('''SELECT * FROM books''')
            book_info = cursor.fetchall()
            book_info.insert(0, ("ID", "Title", "Author", "Quantity"))

            print(tabulate(book_info, headers='firstrow', tablefmt='fancy_grid'))
            
            # Request the user to enter the ID of the book they want to delete
            id = int(input("Please enter the ID of the book you would like to delete:\n"))

            # check if ID is in the table
            if id_exists(id, cursor) == True:
                pass

            else:
                raise Exception("This book ID does not exist.")

            cursor.execute('''DELETE FROM books WHERE id = ? ''', (id,))
            print("Book has been deleted.")

            # commit to delete data
            db.commit()

        elif menu == '4':
            '''
            This option allows the user to search the table for a book using keywords in the title
            '''

            # Request the user to emter a keyword
            keyword = input("Insert a keyword of the book title:\n")

            # Add the % needed for the LIKE operator of SQL
            keyword = "%"+keyword+"%"

            cursor.execute('''SELECT Title, Author, Qty FROM books WHERE Title LIKE ?''',(keyword,))
            book_info = cursor.fetchall()
            book_info.insert(0, ("Title", "Author", "Quantity"))

            print(tabulate(book_info, headers='firstrow', tablefmt='fancy_grid'))

        else:
            raise Exception("Incorrect option selected!")

    except Exception as error:
        print(error)
        print("Please try again.")
