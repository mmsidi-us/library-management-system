from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Book, Author, Member, Borrowing

# --- CREATE Operations ---

def add_author(session: Session, name: str, bio: str = None) -> Author:
    author = Author(name=name, bio=bio)
    session.add(author)
    session.commit()
    return author

def add_book(session: Session, title: str, isbn: str, year_published: int, available_copies: int, author_ids: list) -> Book:
    # Ensure ISBN uniqueness
    existing = session.scalar(select(Book).where(Book.isbn == isbn))
    if existing:
        raise ValueError(f"ISBN '{isbn}' is already registered.")
    
    authors = session.scalars(select(Author).where(Author.id.in_(author_ids))).all()
    if not authors:
        raise ValueError("At least one valid Author ID is required.")
        
    book = Book(title=title, isbn=isbn, year_published=year_published, available_copies=available_copies)
    book.authors.extend(authors)
    session.add(book)
    session.commit()
    return book

def add_member(session: Session, name: str, email: str) -> Member:
    existing = session.scalar(select(Member).where(Member.email == email))
    if existing:
        raise ValueError(f"Email '{email}' is already in use.")
    member = Member(name=name, email=email, membership_date=date.today())
    session.add(member)
    session.commit()
    return member

def check_out_book(session: Session, book_id: int, member_id: int) -> Borrowing:
    book = session.get(Book, book_id)
    member = session.get(Member, member_id)
    
    if not book:
        raise ValueError("Book not found.")
    if not member:
        raise ValueError("Member not found.")
    if book.available_copies <= 0:
        raise ValueError("No available copies remaining for checkout.")
        
    # Decrement available inventory and record the transaction
    book.available_copies -= 1
    borrowing = Borrowing(book_id=book_id, member_id=member_id, checkout_date=date.today())
    session.add(borrowing)
    session.commit()
    return borrowing

# --- READ Operations ---

def list_all_books(session: Session):
    return session.scalars(select(Book)).all()

def search_books_by_title(session: Session, title_query: str):
    return session.scalars(select(Book).where(Book.title.icontains(title_query))).all()

def find_books_by_author(session: Session, author_name: str):
    return session.scalars(select(Book).join(Book.authors).where(Author.name.icontains(author_name))).all()

def list_member_borrowings(session: Session, member_id: int):
    return session.scalars(select(Borrowing).where(Borrowing.member_id == member_id, Borrowing.return_date == None)).all()

def list_overdue_books(session: Session, days_limit: int = 14):
    """Fetch unreturned books past the library's return window (e.g., 14 days)."""
    limit_date = date.today() - timedelta(days=days_limit)
    return session.scalars(select(Borrowing).where(Borrowing.checkout_date < limit_date, Borrowing.return_date == None)).all()

# --- UPDATE Operations ---

def return_book(session: Session, borrowing_id: int) -> Borrowing:
    borrowing = session.get(Borrowing, borrowing_id)
    if not borrowing or borrowing.return_date is not None:
        raise ValueError("Active borrowing record not found.")
        
    borrowing.return_date = date.today()
    borrowing.book.available_copies += 1  # Restock copy
    session.commit()
    return borrowing

def update_member_email(session: Session, member_id: int, new_email: str) -> Member:
    member = session.get(Member, member_id)
    if not member:
        raise ValueError("Member not found.")
    
    existing = session.scalar(select(Member).where(Member.email == new_email, Member.id != member_id))
    if existing:
        raise ValueError("Email is already used by another account.")
        
    member.email = new_email
    session.commit()
    return member

# --- DELETE Operations ---

def delete_book(session: Session, book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise ValueError("Book not found.")
    
    # Enforce data safety rule: Can't delete if actively checked out
    active_borrows = session.scalar(select(Borrowing).where(Borrowing.book_id == book_id, Borrowing.return_date == None))
    if active_borrows:
        raise ValueError("Cannot delete a book that is currently checked out by a member.")
        
    session.delete(book)
    session.commit()

def delete_member(session: Session, member_id: int):
    member = session.get(Member, member_id)
    if not member:
        raise ValueError("Member not found.")
        
    # Enforce data safety rule: Can't delete a member holding active library property
    active_borrows = session.scalar(select(Borrowing).where(Borrowing.member_id == member_id, Borrowing.return_date == None))
    if active_borrows:
        raise ValueError("Cannot delete a member with active, unreturned borrowings.")
        
    session.delete(member)
    session.commit()