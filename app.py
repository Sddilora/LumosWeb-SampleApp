from LumosWeb.api import API

from storage import BookStorage
from auth import STATIC_TOKEN, login_required, TokenMiddleware, on_exception


app = API()
book_storage = BookStorage()
book_storage.create(name="7 habits of highly effective people", author="Stephen Covey")
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)

@app.route("/", allowed_methods=["get"])
def index(req, resp):
    books = book_storage.all()
    resp.html = app.template("index.html", context={"books": books})

@app.route("/login", allowed_methods=["post"])
def login(req, resp):
    resp.json = {"token": STATIC_TOKEN}

@app.route("/books", allowed_methods=["post"])
@login_required
def create_book(req, resp):
    book = book_storage.create(**req.POST)

    resp.status_code = 201  # Created
    resp.json = book._asdict()

@app.route("/books/{book_id:d}", allowed_methods=["delete"])
@login_required
def delete_book(req, resp, *, book_id):
    book_storage.delete(book_id)
    resp.status_code = 204  # No content (resource has successfully been deleted.)
