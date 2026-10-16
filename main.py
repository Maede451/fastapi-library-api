from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Library API",
    description="سیستم ساده کتابداری با FastAPI (داده‌ها در حافظه نگهداری می‌شوند)",
    version="1.0.0",
)


# ---------- Schemas ----------
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, examples=["Clean Code"])
    author: str = Field(..., min_length=1, examples=["Robert C. Martin"])
    year: Optional[int] = Field(None, ge=0, examples=[2008])
    isbn: Optional[str] = Field(None, examples=["9780132350884"])
    available: bool = True


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=0)
    isbn: Optional[str] = None
    available: Optional[bool] = None


class Book(BookCreate):
    id: int


# ---------- In-memory "database" ----------
books_db: dict[int, dict] = {
    1: {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "isbn": "9780132350884",
        "available": True,
    },
    2: {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "year": 1999,
        "isbn": "9780201616224",
        "available": True,
    },
}
next_id = 3


def get_book_or_404(book_id: int) -> dict:
    book = books_db.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ---------- Endpoints ----------
@app.get("/books", response_model=list[Book])
def list_books():
    return list(books_db.values())


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate):
    global next_id
    book = {"id": next_id, **payload.model_dump()}
    books_db[next_id] = book
    next_id += 1
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    return get_book_or_404(book_id)


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate):
    book = get_book_or_404(book_id)
    book.update(payload.model_dump(exclude_unset=True))
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    get_book_or_404(book_id)
    del books_db[book_id]
