"""
===========================================
BOOK RECOMMENDATION SYSTEM
===========================================
"""

import mysql.connector
from datetime import datetime, timedelta

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'library_db'
}

conn = None

# ==================== DATABASE SETUP ====================

def create_database():
    """Create database if not exists"""
    try:
        temp_conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = temp_conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
        cursor.close()
        temp_conn.close()
        print("Database created!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def connect_database():
    """Connect to database"""
    global conn
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Connected successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

def create_tables():
    """Create all required tables"""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(200),
            author VARCHAR(100),
            genre VARCHAR(50),
            publisher VARCHAR(100),
            year INT,
            total_copies INT,
            available_copies INT,
            isbn VARCHAR(20)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(15),
            address TEXT,
            join_date DATE,
            membership_type VARCHAR(20)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issue_records (
            issue_id INT PRIMARY KEY AUTO_INCREMENT,
            member_id INT,
            book_id INT,
            issue_date DATE,
            due_date DATE,
            return_date DATE,
            status VARCHAR(20),
            fine DECIMAL(10,2),
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reading_history (
            history_id INT PRIMARY KEY AUTO_INCREMENT,
            member_id INT,
            book_id INT,
            read_date DATE,
            rating INT,
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_reviews (
            review_id INT PRIMARY KEY AUTO_INCREMENT,
            book_id INT,
            member_id INT,
            review_text TEXT,
            rating INT,
            review_date DATE,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)
    
    conn.commit()
    cursor.close()
    print("Tables created!")

def insert_sample_data():
    """Insert sample data"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] > 0:
        cursor.close()
        return
    
    books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 'Scribner', 1925, 5, 5, '9780743273565'),
        ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'J.B. Lippincott', 1960, 4, 4, '9780061120084'),
        ('1984', 'George Orwell', 'Science Fiction', 'Secker & Warburg', 1949, 6, 6, '9780451524935'),
        ('Pride and Prejudice', 'Jane Austen', 'Romance', 'T. Egerton', 1813, 3, 3, '9780141439518'),
        ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 'Little, Brown', 1951, 4, 4, '9780316769174'),
        ('Harry Potter - Philosophers Stone', 'J.K. Rowling', 'Fantasy', 'Bloomsbury', 1997, 7, 5, '9780747532699'),
        ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'George Allen', 1937, 5, 5, '9780547928227'),
        ('The Da Vinci Code', 'Dan Brown', 'Mystery', 'Doubleday', 2003, 4, 3, '9780385504201'),
        ('The Alchemist', 'Paulo Coelho', 'Fiction', 'HarperCollins', 1988, 6, 6, '9780062315007'),
        ('Animal Farm', 'George Orwell', 'Political Satire', 'Secker & Warburg', 1945, 5, 5, '9780451526342'),
        ('Brave New World', 'Aldous Huxley', 'Science Fiction', 'Chatto & Windus', 1932, 3, 3, '9780060850524'),
        ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'Allen & Unwin', 1954, 4, 4, '9780618640157'),
        ('The Chronicles of Narnia', 'C.S. Lewis', 'Fantasy', 'Geoffrey Bles', 1950, 5, 5, '9780066238500'),
        ('Murder on the Orient Express', 'Agatha Christie', 'Mystery', 'Collins Crime Club', 1934, 3, 3, '9780062693662'),
        ('Sherlock Holmes Complete', 'Arthur Conan Doyle', 'Mystery', 'George Newnes', 1892, 4, 4, '9781435114944')
    ]
    
    cursor.executemany("""
        INSERT INTO books (title, author, genre, publisher, year, total_copies, available_copies, isbn)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, books)
    
    members = [
        ('Rahul Sharma', 'rahul@email.com', '9876543210', '123 MG Road Delhi', '2024-01-15', 'Premium'),
        ('Priya Singh', 'priya@email.com', '9876543211', '456 Park Street Kolkata', '2024-02-20', 'Standard'),
        ('Amit Patel', 'amit@email.com', '9876543212', '789 FC Road Pune', '2024-03-10', 'Premium'),
        ('Sneha Reddy', 'sneha@email.com', '9876543213', '321 Beach Road Chennai', '2024-04-05', 'Standard'),
        ('Vikram Kumar', 'vikram@email.com', '9876543214', '654 Lake View Bangalore', '2024-05-12', 'Premium')
    ]
    
    cursor.executemany("""
        INSERT INTO members (name, email, phone, address, join_date, membership_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, members)
    
    history = [
        (1, 1, '2024-06-01', 5),
        (1, 2, '2024-06-15', 4),
        (1, 3, '2024-07-01', 5),
        (2, 4, '2024-06-20', 3),
        (2, 5, '2024-07-10', 4),
        (3, 6, '2024-06-25', 5),
        (3, 7, '2024-07-15', 5),
        (4, 8, '2024-07-01', 4),
        (5, 9, '2024-07-20', 5)
    ]
    
    cursor.executemany("""
        INSERT INTO reading_history (member_id, book_id, read_date, rating)
        VALUES (%s, %s, %s, %s)
    """, history)
    
    reviews = [
        (1, 1, 'Absolutely brilliant! A timeless classic.', 5, '2024-06-02'),
        (2, 2, 'Powerful and moving story.', 4, '2024-06-16'),
        (3, 1, 'One of the best books I have read.', 5, '2024-07-02'),
        (6, 3, 'Magical and captivating!', 5, '2024-06-26'),
        (9, 5, 'Life-changing book.', 5, '2024-07-21')
    ]
    
    cursor.executemany("""
        INSERT INTO book_reviews (book_id, member_id, review_text, rating, review_date)
        VALUES (%s, %s, %s, %s, %s)
    """, reviews)
    
    conn.commit()
    cursor.close()
    print("Sample data inserted!")

# ==================== BOOK MANAGEMENT ====================

def add_book():
    """Add new book"""
    print("\n=== ADD NEW BOOK ===")
    title = input("Title: ")
    author = input("Author: ")
    genre = input("Genre: ")
    publisher = input("Publisher: ")
    year = int(input("Year: "))
    copies = int(input("Total Copies: "))
    isbn = input("ISBN: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, genre, publisher, year, total_copies, available_copies, isbn)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, author, genre, publisher, year, copies, copies, isbn))
        conn.commit()
        print("Book added successfully!")
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

def view_all_books():
    """Display all books"""
    print("\n=== ALL BOOKS ===")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY book_id")
    books = cursor.fetchall()
    
    if books:
        print(f"{'ID':<6} {'Title':<35} {'Author':<25} {'Genre':<15} {'Available':<10}")
        print("=" * 95)
        for book in books:
            print(f"{book[0]:<6} {book[1]:<35} {book[2]:<25} {book[3]:<15} {book[7]}/{book[6]}")
    else:
        print("No books found.")
    cursor.close()

def search_books():
    """Search books by title or author"""
    print("\n=== SEARCH BOOKS ===")
    search = input("Enter title or author: ")
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM books WHERE title LIKE %s OR author LIKE %s
    """, (f"%{search}%", f"%{search}%"))
    books = cursor.fetchall()
    
    if books:
        print(f"\n{'ID':<6} {'Title':<35} {'Author':<25} {'Genre':<15}")
        print("=" * 85)
        for book in books:
            print(f"{book[0]:<6} {book[1]:<35} {book[2]:<25} {book[3]:<15}")
    else:
        print("No books found.")
    cursor.close()

def search_by_genre():
    """Search books by genre"""
    print("\n=== SEARCH BY GENRE ===")
    genre = input("Enter genre: ")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE genre LIKE %s", (f"%{genre}%",))
    books = cursor.fetchall()
    
    if books:
        print(f"\n{'ID':<6} {'Title':<35} {'Author':<25}")
        print("=" * 70)
        for book in books:
            print(f"{book[0]:<6} {book[1]:<35} {book[2]:<25}")
    else:
        print("No books found in this genre.")
    cursor.close()

def update_book_copies(book_id, change):
    """Update available copies"""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books SET available_copies = available_copies + %s WHERE book_id = %s
    """, (change, book_id))
    conn.commit()
    cursor.close()

def delete_book():
    """Delete a book"""
    print("\n=== DELETE BOOK ===")
    try:
        book_id = int(input("Book ID: "))
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id=%s", (book_id,))
        if not cursor.fetchone():
            print("Book not found!")
            cursor.close()
            return
        
        cursor.execute("""
            SELECT COUNT(*) FROM issue_records WHERE book_id=%s AND status='Issued'
        """, (book_id,))
        
        if cursor.fetchone()[0] > 0:
            print("Cannot delete! Book is currently issued.")
            cursor.close()
            return
        
        confirm = input("Confirm deletion? (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
            conn.commit()
            print("Book deleted!")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

# ==================== MEMBER MANAGEMENT ====================

def add_member():
    """Add new member"""
    print("\n=== ADD MEMBER ===")
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    membership = input("Membership Type (Standard/Premium): ")
    
    try:
        cursor = conn.cursor()
        today = datetime.now().date()
        cursor.execute("""
            INSERT INTO members (name, email, phone, address, join_date, membership_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, phone, address, today, membership))
        conn.commit()
        member_id = cursor.lastrowid
        print(f"Member added! ID: {member_id}")
        cursor.close()
        return member_id
    except Exception as e:
        print(f"Error: {e}")
        return None

def view_all_members():
    """Display all members"""
    print("\n=== ALL MEMBERS ===")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members ORDER BY member_id")
    members = cursor.fetchall()
    
    if members:
        print(f"{'ID':<6} {'Name':<25} {'Phone':<15} {'Email':<30} {'Type':<12}")
        print("=" * 90)
        for m in members:
            print(f"{m[0]:<6} {m[1]:<25} {m[3]:<15} {m[2]:<30} {m[6]:<12}")
    else:
        print("No members found.")
    cursor.close()

def search_member():
    """Search member by phone or name"""
    print("\n=== SEARCH MEMBER ===")
    search = input("Enter name or phone: ")
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM members WHERE name LIKE %s OR phone LIKE %s
    """, (f"%{search}%", f"%{search}%"))
    members = cursor.fetchall()
    
    if members:
        print(f"\n{'ID':<6} {'Name':<25} {'Phone':<15} {'Email':<30}")
        print("=" * 80)
        for m in members:
            print(f"{m[0]:<6} {m[1]:<25} {m[3]:<15} {m[2]:<30}")
        return members
    else:
        print("No members found.")
        cursor.close()
        return None

def view_member_history():
    """View member's reading history"""
    print("\n=== MEMBER HISTORY ===")
    try:
        member_id = int(input("Member ID: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.title, b.author, rh.read_date, rh.rating
            FROM reading_history rh
            JOIN books b ON rh.book_id = b.book_id
            WHERE rh.member_id = %s
            ORDER BY rh.read_date DESC
        """, (member_id,))
        
        history = cursor.fetchall()
        
        if history:
            print(f"\n{'Title':<40} {'Author':<25} {'Date':<12} {'Rating':<8}")
            print("=" * 90)
            for h in history:
                print(f"{h[0]:<40} {h[1]:<25} {str(h[2]):<12} {h[3]}/5")
        else:
            print("No reading history found.")
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

# ==================== ISSUE & RETURN ====================

def issue_book():
    """Issue book to member"""
    print("\n=== ISSUE BOOK ===")
    
    try:
        member_id = int(input("Member ID: "))
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE member_id=%s", (member_id,))
        if not cursor.fetchone():
            print("Member not found!")
            cursor.close()
            return
        
        search_books()
        book_id = int(input("\nBook ID: "))
        
        cursor.execute("""
            SELECT available_copies FROM books WHERE book_id=%s
        """, (book_id,))
        
        result = cursor.fetchone()
        if not result:
            print("Book not found!")
            cursor.close()
            return
        
        if result[0] <= 0:
            print("Book not available!")
            cursor.close()
            return
        
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=14)
        
        cursor.execute("""
            INSERT INTO issue_records (member_id, book_id, issue_date, due_date, status, fine)
            VALUES (%s, %s, %s, %s, 'Issued', 0)
        """, (member_id, book_id, issue_date, due_date))
        
        update_book_copies(book_id, -1)
        conn.commit()
        
        print("\n=== ISSUE SUCCESSFUL ===")
        print(f"Issue Date: {issue_date}")
        print(f"Due Date: {due_date}")
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")

def return_book():
    """Return issued book"""
    print("\n=== RETURN BOOK ===")
    
    try:
        issue_id = int(input("Issue ID: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT issue_id, book_id, due_date FROM issue_records 
            WHERE issue_id=%s AND status='Issued'
        """, (issue_id,))
        
        record = cursor.fetchone()
        
        if not record:
            print("Invalid issue ID or book already returned!")
            cursor.close()
            return
        
        return_date = datetime.now().date()
        due_date = record[2]
        
        fine = 0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * 10
            print(f"\nLate by {days_late} days. Fine: Rs.{fine}")
        
        cursor.execute("""
            UPDATE issue_records SET return_date=%s, status='Returned', fine=%s
            WHERE issue_id=%s
        """, (return_date, fine, issue_id))
        
        update_book_copies(record[1], 1)
        conn.commit()
        
        print("\nBook returned successfully!")
        if fine > 0:
            print(f"Please collect fine: Rs.{fine}")
        
        rating = input("\nRate this book (1-5) or skip: ")
        if rating.isdigit() and 1 <= int(rating) <= 5:
            cursor.execute("""
                SELECT member_id FROM issue_records WHERE issue_id=%s
            """, (issue_id,))
            member_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO reading_history (member_id, book_id, read_date, rating)
                VALUES (%s, %s, %s, %s)
            """, (member_id, record[1], return_date, int(rating)))
            conn.commit()
            print("Rating recorded!")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

def view_issued_books():
    """View all issued books"""
    print("\n=== ISSUED BOOKS ===")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.issue_id, m.name, b.title, i.issue_date, i.due_date
        FROM issue_records i
        JOIN members m ON i.member_id = m.member_id
        JOIN books b ON i.book_id = b.book_id
        WHERE i.status = 'Issued'
        ORDER BY i.due_date
    """)
    
    issued = cursor.fetchall()
    
    if issued:
        print(f"\n{'Issue ID':<10} {'Member':<25} {'Book':<35} {'Issue Date':<12} {'Due Date':<12}")
        print("=" * 100)
        for i in issued:
            print(f"{i[0]:<10} {i[1]:<25} {i[2]:<35} {str(i[3]):<12} {str(i[4]):<12}")
    else:
        print("No books currently issued.")
    cursor.close()

def view_overdue_books():
    """View overdue books"""
    print("\n=== OVERDUE BOOKS ===")
    cursor = conn.cursor()
    today = datetime.now().date()
    
    cursor.execute("""
        SELECT i.issue_id, m.name, m.phone, b.title, i.due_date, DATEDIFF(%s, i.due_date) as days_late
        FROM issue_records i
        JOIN members m ON i.member_id = m.member_id
        JOIN books b ON i.book_id = b.book_id
        WHERE i.status = 'Issued' AND i.due_date < %s
        ORDER BY days_late DESC
    """, (today, today))
    
    overdue = cursor.fetchall()
    
    if overdue:
        print(f"\n{'Issue ID':<10} {'Member':<20} {'Phone':<15} {'Book':<30} {'Days Late':<12} {'Fine':<10}")
        print("=" * 105)
        for o in overdue:
            fine = o[5] * 10
            print(f"{o[0]:<10} {o[1]:<20} {o[2]:<15} {o[3]:<30} {o[5]:<12} Rs.{fine}")
    else:
        print("No overdue books!")
    cursor.close()

# ==================== BOOK RECOMMENDATION ====================

def recommend_by_genre():
    """Recommend books based on member's favorite genre"""
    print("\n=== GENRE-BASED RECOMMENDATIONS ===")
    try:
        member_id = int(input("Member ID: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.genre, COUNT(*) as cnt
            FROM reading_history rh
            JOIN books b ON rh.book_id = b.book_id
            WHERE rh.member_id = %s
            GROUP BY b.genre
            ORDER BY cnt DESC
            LIMIT 1
        """, (member_id,))
        
        result = cursor.fetchone()
        
        if not result:
            print("No reading history found. Showing popular books.")
            recommend_popular_books()
            cursor.close()
            return
        
        favorite_genre = result[0]
        print(f"\nYour favorite genre: {favorite_genre}")
        
        cursor.execute("""
            SELECT b.book_id, b.title, b.author, b.available_copies
            FROM books b
            WHERE b.genre = %s
            AND b.book_id NOT IN (
                SELECT book_id FROM reading_history WHERE member_id = %s
            )
            AND b.available_copies > 0
            ORDER BY b.year DESC
            LIMIT 5
        """, (favorite_genre, member_id))
        
        recommendations = cursor.fetchall()
        
        if recommendations:
            print(f"\n{'ID':<6} {'Title':<40} {'Author':<25}")
            print("=" * 75)
            for r in recommendations:
                print(f"{r[0]:<6} {r[1]:<40} {r[2]:<25}")
        else:
            print("No new recommendations in your favorite genre.")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

def recommend_by_rating():
    """Recommend highly rated books"""
    print("\n=== TOP RATED BOOKS ===")
    try:
        member_id = int(input("Member ID: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.book_id, b.title, b.author, AVG(rh.rating) as avg_rating, COUNT(*) as read_count
            FROM books b
            JOIN reading_history rh ON b.book_id = rh.book_id
            WHERE b.book_id NOT IN (
                SELECT book_id FROM reading_history WHERE member_id = %s
            )
            AND b.available_copies > 0
            GROUP BY b.book_id
            HAVING avg_rating >= 4
            ORDER BY avg_rating DESC, read_count DESC
            LIMIT 5
        """, (member_id,))
        
        recommendations = cursor.fetchall()
        
        if recommendations:
            print(f"\n{'ID':<6} {'Title':<40} {'Author':<25} {'Avg Rating':<12}")
            print("=" * 90)
            for r in recommendations:
                print(f"{r[0]:<6} {r[1]:<40} {r[2]:<25} {r[3]:.1f}/5")
        else:
            print("No recommendations found.")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

def recommend_popular_books():
    """Recommend most popular books"""
    print("\n=== POPULAR BOOKS ===")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.book_id, b.title, b.author, COUNT(*) as issue_count
        FROM books b
        JOIN issue_records i ON b.book_id = i.book_id
        WHERE b.available_copies > 0
        GROUP BY b.book_id
        ORDER BY issue_count DESC
        LIMIT 5
    """)
    
    popular = cursor.fetchall()
    
    if popular:
        print(f"\n{'ID':<6} {'Title':<40} {'Author':<25} {'Times Issued':<15}")
        print("=" * 90)
        for p in popular:
            print(f"{p[0]:<6} {p[1]:<40} {p[2]:<25} {p[3]}")
    else:
        print("No data available.")
    cursor.close()

def recommend_by_author():
    """Recommend books by favorite author"""
    print("\n=== AUTHOR-BASED RECOMMENDATIONS ===")
    try:
        member_id = int(input("Member ID: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.author, COUNT(*) as cnt
            FROM reading_history rh
            JOIN books b ON rh.book_id = b.book_id
            WHERE rh.member_id = %s
            GROUP BY b.author
            ORDER BY cnt DESC
            LIMIT 1
        """, (member_id,))
        
        result = cursor.fetchone()
        
        if not result:
            print("No reading history found.")
            cursor.close()
            return
        
        favorite_author = result[0]
        print(f"\nYour favorite author: {favorite_author}")
        
        cursor.execute("""
            SELECT b.book_id, b.title, b.genre
            FROM books b
            WHERE b.author = %s
            AND b.book_id NOT IN (
                SELECT book_id FROM reading_history WHERE member_id = %s
            )
            AND b.available_copies > 0
        """, (favorite_author, member_id))
        
        recommendations = cursor.fetchall()
        
        if recommendations:
            print(f"\n{'ID':<6} {'Title':<50} {'Genre':<20}")
            print("=" * 80)
            for r in recommendations:
                print(f"{r[0]:<6} {r[1]:<50} {r[2]:<20}")
        else:
            print("No more books by this author.")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

# ==================== REPORTS ====================

def most_issued_books():
    """Report of most issued books"""
    print("\n=== MOST ISSUED BOOKS ===")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, b.author, COUNT(*) as issue_count
        FROM issue_records i
        JOIN books b ON i.book_id = b.book_id
        GROUP BY b.book_id
        ORDER BY issue_count DESC
        LIMIT 10
    """)
    
    books = cursor.fetchall()
    
    if books:
        print(f"\n{'Title':<45} {'Author':<30} {'Times Issued':<15}")
        print("=" * 95)
        for b in books:
            print(f"{b[0]:<45} {b[1]:<30} {b[2]}")
    else:
        print("No data available.")
    cursor.close()

def active_members_report():
    """Report of most active members"""
    print("\n=== MOST ACTIVE MEMBERS ===")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, m.phone, COUNT(*) as books_read
        FROM reading_history rh
        JOIN members m ON rh.member_id = m.member_id
        GROUP BY m.member_id
        ORDER BY books_read DESC
        LIMIT 10
    """)
    
    members = cursor.fetchall()
    
    if members:
        print(f"\n{'Name':<30} {'Phone':<15} {'Books Read':<12}")
        print("=" * 60)
        for m in members:
            print(f"{m[0]:<30} {m[1]:<15} {m[2]}")
    else:
        print("No data available.")
    cursor.close()

def genre_popularity_report():
    """Report of popular genres"""
    print("\n=== GENRE POPULARITY ===")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.genre, COUNT(*) as issue_count
        FROM issue_records i
        JOIN books b ON i.book_id = b.book_id
        GROUP BY b.genre
        ORDER BY issue_count DESC
    """)
    
    genres = cursor.fetchall()
    
    if genres:
        print(f"\n{'Genre':<25} {'Times Issued':<15}")
        print("=" * 45)
        for g in genres:
            print(f"{g[0]:<25} {g[1]}")
    else:
        print("No data available.")
    cursor.close()

def fine_collection_report():
    """Report of fine collection"""
    print("\n=== FINE COLLECTION REPORT ===")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(fine) as total_fine, COUNT(*) as late_returns
        FROM issue_records
        WHERE status='Returned' AND fine > 0
    """)
    
    result = cursor.fetchone()
    
    if result and result[0]:
        print(f"\nTotal Fine Collected: Rs.{result[0]}")
        print(f"Total Late Returns: {result[1]}")
    else:
        print("\nNo fines collected yet.")
    cursor.close()

# ==================== REVIEW FUNCTIONS ====================

def add_review():
    """Add book review"""
    print("\n=== ADD REVIEW ===")
    try:
        member_id = int(input("Member ID: "))
        book_id = int(input("Book ID: "))
        rating = int(input("Rating (1-5): "))
        review_text = input("Review: ")
        
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5!")
            return
        
        cursor = conn.cursor()
        today = datetime.now().date()
        
        cursor.execute("""
            INSERT INTO book_reviews (book_id, member_id, review_text, rating, review_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (book_id, member_id, review_text, rating, today))
        
        conn.commit()
        print("Review added successfully!")
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

def view_book_reviews():
    """View reviews for a book"""
    print("\n=== BOOK REVIEWS ===")
    try:
        book_id = int(input("Book ID: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.title, b.author FROM books WHERE book_id=%s
        """, (book_id,))
        
        book = cursor.fetchone()
        if not book:
            print("Book not found!")
            cursor.close()
            return
        
        print(f"\nBook: {book[0]}")
        print(f"Author: {book[1]}")
        
        cursor.execute("""
            SELECT m.name, br.rating, br.review_text, br.review_date
            FROM book_reviews br
            JOIN members m ON br.member_id = m.member_id
            WHERE br.book_id = %s
            ORDER BY br.review_date DESC
        """, (book_id,))
        
        reviews = cursor.fetchall()
        
        if reviews:
            print("\n" + "=" * 80)
            for r in reviews:
                print(f"\nReviewer: {r[0]}")
                print(f"Rating: {r[1]}/5")
                print(f"Date: {r[3]}")
                print(f"Review: {r[2]}")
                print("-" * 80)
        else:
            print("\nNo reviews yet.")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

# ==================== MENU FUNCTIONS ====================

def book_menu():
    """Book management menu"""
    while True:
        print("\n=== BOOK MANAGEMENT ===")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Books")
        print("4. Search by Genre")
        print("5. Delete Book")
        print("6. Back")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            add_book()
        elif choice == '2':
            view_all_books()
        elif choice == '3':
            search_books()
        elif choice == '4':
            search_by_genre()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            break

def member_menu():
    """Member management menu"""
    while True:
        print("\n=== MEMBER MANAGEMENT ===")
        print("1. Add Member")
        print("2. View All Members")
        print("3. Search Member")
        print("4. View Member History")
        print("5. Back")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            add_member()
        elif choice == '2':
            view_all_members()
        elif choice == '3':
            search_member()
        elif choice == '4':
            view_member_history()
        elif choice == '5':
            break

def issue_return_menu():
    """Issue and return menu"""
    while True:
        print("\n=== ISSUE & RETURN ===")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. View Issued Books")
        print("4. View Overdue Books")
        print("5. Back")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            issue_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            view_issued_books()
        elif choice == '4':
            view_overdue_books()
        elif choice == '5':
            break

def recommendation_menu():
    """Recommendation menu"""
    while True:
        print("\n=== BOOK RECOMMENDATIONS ===")
        print("1. Recommend by Genre")
        print("2. Recommend by Rating")
        print("3. Recommend by Author")
        print("4. Popular Books")
        print("5. Back")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            recommend_by_genre()
        elif choice == '2':
            recommend_by_rating()
        elif choice == '3':
            recommend_by_author()
        elif choice == '4':
            recommend_popular_books()
        elif choice == '5':
            break

def review_menu():
    """Review menu"""
    while True:
        print("\n=== REVIEWS ===")
        print("1. Add Review")
        print("2. View Book Reviews")
        print("3. Back")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            add_review()
        elif choice == '2':
            view_book_reviews()
        elif choice == '3':
            break

def report_menu():
    """Reports menu"""
    while True:
        print("\n=== REPORTS ===")
        print("1. Most Issued Books")
        print("2. Most Active Members")
        print("3. Genre Popularity")
        print("4. Fine Collection")
        print("5. Back")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            most_issued_books()
        elif choice == '2':
            active_members_report()
        elif choice == '3':
            genre_popularity_report()
        elif choice == '4':
            fine_collection_report()
        elif choice == '5':
            break

def main_menu():
    """Main menu"""
    while True:
        print("\n" + "=" * 50)
        print("BOOK RECOMMENDATION SYSTEM")
        print("=" * 50)
        print("1. Book Management")
        print("2. Member Management")
        print("3. Issue & Return")
        print("4. Book Recommendations")
        print("5. Reviews")
        print("6. Reports")
        print("7. Exit")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            book_menu()
        elif choice == '2':
            member_menu()
        elif choice == '3':
            issue_return_menu()
        elif choice == '4':
            recommendation_menu()
        elif choice == '5':
            review_menu()
        elif choice == '6':
            report_menu()
        elif choice == '7':
            print("\nThank you! Goodbye!")
            break

# ==================== MAIN PROGRAM ====================

def initialize():
    """Initialize system"""
    print("\n=== INITIALIZING LIBRARY SYSTEM ===")
    create_database()
    
    global conn
    conn = connect_database()
    
    if conn:
        create_tables()
        insert_sample_data()
        print("\nSystem ready!")
        return True
    return False

def main():
    """Main function"""
    if initialize():
        main_menu()
        if conn:
            conn.close()
            print("Connection closed.")
    else:
        print("Initialization failed!")

if __name__ == "__main__":
    main()
