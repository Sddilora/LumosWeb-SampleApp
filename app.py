from LumosWeb.api import API
from LumosWeb.orm import Database

from storage import BookStorage
from auth import STATIC_TOKEN, login_required, TokenMiddleware, on_exception
from models import Book

app = API()
book_storage = BookStorage()
book_storage.create(name="7 habits of highly effective people", author="Stephen Covey")
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)

db = Database("./lumos.db")
db.create(Book)

@app.route("/", allowed_methods=["get"])
def index(req, resp):
    books = db.all(Book)
    resp.html = app.template("index.md", context={"books": books})

@app.route("/login", allowed_methods=["post"])
def login(req, resp):
    resp.json = {"token": STATIC_TOKEN}

@app.route("/books", allowed_methods=["post"])
@login_required
def create_book(req, resp):
    book = Book(**req.POST)  # Creates a Book instance with the given data in the request.
    db.save(book)

    resp.status_code = 201  # Created
    resp.json = {"name": book.name, "author": book.author}

@app.route("/books/{id:d}", allowed_methods=["delete"])
@login_required
def delete_book(req, resp, id):
    db.delete(Book, id=id)
    resp.status_code = 204  # No content (resource has successfully been deleted.)
