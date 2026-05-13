import datetime
import json

DATA_FILE = 'library.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": [], "borrow_history": []}

class Base:
    def __init__(self):
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = datetime.datetime.now().isoformat()

class Book(Base):
    def __init__(self, title, author, year, genre):
        super().__init__()
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isBorrowed = False

class User(Base):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._save_user()

    def _save_user(self):
        data = load_data()
        if not any(u["name"] == self.name for u in data["users"]):
            data["users"].append({
                "name": self.name,
                "created_at": self.created_at
            })
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)

    def borrow_book(self, book):
        data = load_data()
        for entry in data["borrow_history"]:
            if entry.get("book") == book.title and not entry.get("returned"):
                print(f"'{book.title}' is already borrowed.")
                return
        book.isBorrowed = True
        book.updated_at = datetime.datetime.now().isoformat()
        data["borrow_history"].append({
            "user": self.name,
            "book": book.title,
            "borrowed_at": datetime.datetime.now().isoformat()
        })
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"{self.name} borrowed '{book.title}'.")

def show_history():
    data = load_data()
    if not data["borrow_history"]:
        print("No history yet.")
        return
    print("\n--- Borrow History ---")
    for entry in data["borrow_history"]:
        print(f"  {entry['borrowed_at']}  |  {entry['user']} borrowed '{entry['book']}'")
    print("----------------------\n")

# --- Run ---
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Novel")
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960, "Novel")

user1 = User("Alice")
user2 = User("Bob")

user1.borrow_book(book1)
user2.borrow_book(book1)  # already borrowed
user2.borrow_book(book2)

show_history()
