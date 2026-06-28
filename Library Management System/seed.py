from datetime import date, timedelta
from sqlalchemy.orm import Session
from models import Book, Author, Member, Borrowing, Base, engine

def seed_data():
    """Drops and re-creates tables, filling them with robust initial sample datasets."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # 1. Seeds Authors
        a1 = Author(name="Ahmed Khaled Towfik", bio="Egyptian sci-fi/horror pioneer.")
        a2 = Author(name="Naguib Mahfouz", bio="Nobel Prize laureate in Literature.")
        a3 = Author(name="Malcolm Gladwell", bio="Journalist and non-fiction author.")
        session.add_all([a1, a2, a3])
        session.flush()

        # 2. Seeds Books (Mapping M2M relationships to Authors)
        b1 = Book(title="Utopia", isbn="97801", year_published=2008, available_copies=3, authors=[a1])
        b2 = Book(title="Palace Walk", isbn="97802", year_published=1956, available_copies=2, authors=[a2])
        b3 = Book(title="Outliers", isbn="97803", year_published=2008, available_copies=1, authors=[a3])
        b4 = Book(title="Paranormal Tales", isbn="97804", year_published=1993, available_copies=4, authors=[a1])
        b5 = Book(title="The Thief and the Dogs", isbn="97805", year_published=1961, available_copies=2, authors=[a2])
        session.add_all([b1, b2, b3, b4, b5])
        session.flush()

        # 3. Seeds Members
        m1 = Member(name="Sidi Abdoulah", email="sidi@example.com", membership_date=date.today() - timedelta(days=50))
        m2 = Member(name="Fatima Ali", email="fatima@example.com", membership_date=date.today() - timedelta(days=30))
        m3 = Member(name="Omar Hassan", email="omar@example.com", membership_date=date.today() - timedelta(days=20))
        m4 = Member(name="Zainab Jiddou", email="zainab@example.com", membership_date=date.today() - timedelta(days=10))
        session.add_all([m1, m2, m3, m4])
        session.flush()

        # 4. Seeds 6 Borrowing Records (4 Returned, 2 Active/Overdue)
        borrows = [
            # Historically completed transactions
            Borrowing(book_id=b1.id, member_id=m1.id, checkout_date=date.today()-timedelta(days=20), return_date=date.today()-timedelta(days=15)),
            Borrowing(book_id=b2.id, member_id=m2.id, checkout_date=date.today()-timedelta(days=15), return_date=date.today()-timedelta(days=10)),
            Borrowing(book_id=b3.id, member_id=m3.id, checkout_date=date.today()-timedelta(days=10), return_date=date.today()-timedelta(days=5)),
            Borrowing(book_id=b5.id, member_id=m4.id, checkout_date=date.today()-timedelta(days=8), return_date=date.today()-timedelta(days=2)),
            # Active items out past 14 days (Overdue)
            Borrowing(book_id=b4.id, member_id=m1.id, checkout_date=date.today()-timedelta(days=25), return_date=None),
            Borrowing(book_id=b1.id, member_id=m2.id, checkout_date=date.today()-timedelta(days=18), return_date=None)
        ]
        
        # Deduct active checkouts from inventory numbers
        b4.available_copies -= 1
        b1.available_copies -= 1

        session.add_all(borrows)
        session.commit()
        print("Database successfully seeded with clean test data!")