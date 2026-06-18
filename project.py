from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
print(engine)

Base = declarative_base()

class Author(Base):
    __tablename__ = 'Author'
    id = Column(Integer, primary_key=True)
    name = Column(String(75))
    birth_year = Column(Integer)
    books = relationship('Book', back_populates='authors')
class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), unique=True, nullable=False)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey('Author.id'))
    authors = relationship('Author', back_populates='books')


Base.metadata.create_all(engine)


a1 = Author(name = 'Толстой', birth_year = 1899)
a2 = Author(name = 'Достоевский', birth_year = 1999)
a3 = Author(name = 'Лермонтов', birth_year = 1879)

b1 = Book(title = 'Преступление и наказание', year = 1899, author_id = 2)
b2 = Book(title = 'Война и Мир', year = 1999, author_id = 1)
b3 = Book(title = 'Братья Карамазовы', year = 1999, author_id = 2)
b4 = Book(title = 'Капитанская дочка', year = 1899, author_id = 3)
b5 = Book(title = 'Евгений Онегин', year = 1899, author_id = 3)

session.add_all([a1, a2, a3, b1, b2, b3, b4, b5])
session.commit()

authors_name = session.query(Author.name).all()
print(authors_name)

a3.name = 'Пушкин'
session.commit()
print(a3.name)

session.delete(b5)
session.commit()

books = session.query(Book.year).order_by(Book.year.desc()) # (от новых к старым)
print(books.all())

books_1 = session.query(Book.year).filter(Book.year > 1950)
print(books_1.all())

dostoyevskiy = session.query(Author).filter(Author.name == 'Достоевский').first()
print(dostoyevskiy.name)

books_first_three = session.query(Book).order_by(Book.title).limit(3)

# Для удобного вывода
for book in books_first_three.all():
    print(book.title)

count_books = session.query(func.count(Book.id)).scalar()
print(count_books)

session.close()
