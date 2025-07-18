from flask import Flask, request, jsonify

app = Flask(__name__)

#  Book and Library Classes 
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_lent": self.is_lent
        }

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_lent:
                book.is_lent = True
                return book
        return None

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.is_lent = False
                return book
        return None

    def get_available_books(self):
        return [book for book in self.books if not book.is_lent]

library = Library()

#  API Routes 

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(data['title'], data['author'], data['isbn'])
    library.add_book(book)
    return jsonify({"message": "Book added successfully"}), 201

@app.route('/books/<isbn>', methods=['DELETE'])
def remove_book(isbn):
    library.remove_book(isbn)
    return jsonify({"message": "Book removed successfully"}), 200

@app.route('/lend/<isbn>', methods=['POST'])
def lend_book(isbn):
    book = library.lend_book(isbn)
    if book:
        return jsonify({"message": f"Book '{book.title}' lent successfully"}), 200
    return jsonify({"error": "Book not available or already lent"}), 400

@app.route('/return/<isbn>', methods=['POST'])
def return_book(isbn):
    book = library.return_book(isbn)
    if book:
        return jsonify({"message": f"Book '{book.title}' returned successfully"}), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['GET'])
def list_books():
    books = [book.to_dict() for book in library.get_available_books()]
    return jsonify(books), 200

#  Run the App 
if __name__ == '__main__':
    app.run(debug=True)
