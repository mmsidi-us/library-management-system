from datetime import date
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
    pass

# Many-to-Many Association Table between Books and Authors
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
)

# Association Model for Borrowings (Book <-> Member) with extra attributes
class Borrowing(Base):
    __tablename__ = "borrowings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="RESTRICT"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="RESTRICT"))
    checkout_date: Mapped[date] = mapped_column(Date, default=date.today)
    return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships pointing back to parent entities
    book: Mapped["Book"] = relationship(back_populates="borrowings")
    member: Mapped["Member"] = relationship(back_populates="borrowings")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    isbn: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    year_published: Mapped[int] = mapped_column(Integer, nullable=False)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)

    # Bidirectional Relationships
    authors: Mapped[List["Author"]] = relationship(
        secondary=book_author, back_populates="books"
    )
    borrowings: Mapped[List["Borrowing"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Bidirectional Relationship
    books: Mapped[List["Book"]] = relationship(
        secondary=book_author, back_populates="authors"
    )


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    membership_date: Mapped[date] = mapped_column(Date, default=date.today)

    # Bidirectional Relationship
    borrowings: Mapped[List["Borrowing"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )

def init_db():
    """Creates tables if they don't exist yet."""
    Base.metadata.create_all(engine)