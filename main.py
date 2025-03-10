class Book:
    def __init__(self, isbn, title, author, price):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
    
    def __str__(self):
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Price: ${self.price}"


class SortedBookStack:
    def __init__(self):
        self.stack = []
    
    def push(self, book):
        if not self.stack or book.isbn > self.stack[-1].isbn:
            self.stack.append(book)
            return
        
        temp_stack = []
        while self.stack and self.stack[-1].isbn > book.isbn:
            temp_stack.append(self.stack.pop())
        
        self.stack.append(book)
        
        while temp_stack:
            self.stack.append(temp_stack.pop())
    
    def pop(self):
        if not self.stack:
            return None
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            return None
        return self.stack[-1]
    
    def find_by_isbn(self, isbn):
        for book in self.stack:
            if book.isbn == isbn:
                return book
        return None
    
    def remove_by_isbn(self, isbn):
        for i, book in enumerate(self.stack):
            if book.isbn == isbn:
                return self.stack.pop(i)
        return None
    
    def display(self):
        if not self.stack:
            print("Inventory is empty")
            return
        
        print("Book Inventory (Sorted by ISBN):")
        for book in self.stack:
            print(book)


class Reservation:
    def __init__(self, customer_name, contact, isbn):
        self.customer_name = customer_name
        self.contact = contact
        self.isbn = isbn
    
    def __str__(self):
        return f"Customer: {self.customer_name}, Contact: {self.contact}, ISBN: {self.isbn}"


class ReservationQueue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, reservation):
        self.queue.append(reservation)
    
    def dequeue(self):
        if not self.queue:
            return None
        return self.queue.pop(0)
    
    def search_by_isbn(self, isbn):
        matching_reservations = []
        for reservation in self.queue:
            if reservation.isbn == isbn:
                matching_reservations.append(reservation)
        return matching_reservations
    
    def remove_reservation(self, customer_name, isbn):
        for i, reservation in enumerate(self.queue):
            if reservation.customer_name == customer_name and reservation.isbn == isbn:
                return self.queue.pop(i)
        return None
    
    def display(self):
        if not self.queue:
            print("No reservations in queue")
            return
        
        print("Reservation Queue:")
        for i, reservation in enumerate(self.queue, 1):
            print(f"{i}. {reservation}")


def display_menu():
    print("\n===== Book Inventory and Reservation System =====")
    print("1. Add a new book to inventory")
    print("2. View all books in inventory")
    print("3. Find a book by ISBN")
    print("4. Sell a book")
    print("5. Add a new reservation")
    print("6. View all reservations")
    print("7. Find reservations by ISBN")
    print("8. Process next reservation")
    print("9. Exit")
    return input("Enter your choice (1-9): ")


def main():
    inventory = SortedBookStack()
    reservations = ReservationQueue()
    
    inventory.push(Book("9780132350884", "Clean Code", "Robert C. Martin", 39.99))
    inventory.push(Book("9780134190440", "The Pragmatic Programmer", "Andrew Hunt", 44.99))
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            print("\n----- Add a New Book -----")
            isbn = input("Enter ISBN: ")
            title = input("Enter title: ")
            author = input("Enter author: ")
            
            while True:
                try:
                    price = float(input("Enter price: $"))
                    break
                except ValueError:
                    print("Invalid price. Please enter a number.")
            
            new_book = Book(isbn, title, author, price)
            inventory.push(new_book)
            print(f"Book added: {new_book}")
        
        elif choice == '2':
            print("\n----- Book Inventory -----")
            inventory.display()
        
        elif choice == '3':
            print("\n----- Find Book by ISBN -----")
            isbn = input("Enter ISBN to search: ")
            book = inventory.find_by_isbn(isbn)
            if book:
                print(f"Book found: {book}")
            else:
                print(f"No book found with ISBN: {isbn}")
        
        elif choice == '4':
            print("\n----- Sell a Book -----")
            isbn = input("Enter ISBN of book to sell: ")
            book = inventory.find_by_isbn(isbn)
            if book:
                print(f"Selling: {book}")
                inventory.remove_by_isbn(isbn)
                
                matching_reservations = reservations.search_by_isbn(isbn)
                if matching_reservations:
                    print(f"There are {len(matching_reservations)} reservations for this book:")
                    for i, res in enumerate(matching_reservations, 1):
                        print(f"{i}. {res}")
                    
                    notify = input("Would you like to notify the first customer? (y/n): ")
                    if notify.lower() == 'y':
                        customer = matching_reservations[0]
                        print(f"Notifying {customer.customer_name} at {customer.contact}")
                        reservations.remove_reservation(customer.customer_name, isbn)
                        print("Reservation processed and removed from queue")
                
                print("Book removed from inventory")
            else:
                print(f"No book found with ISBN: {isbn}")
        
        elif choice == '5':
            print("\n----- Add a Reservation -----")
            customer_name = input("Enter customer name: ")
            contact = input("Enter contact information: ")
            isbn = input("Enter ISBN of book to reserve: ")
            
            book = inventory.find_by_isbn(isbn)
            if book:
                print(f"Book found: {book}")
            else:
                print(f"Warning: No book with ISBN {isbn} in inventory")
                confirm = input("Continue with reservation anyway? (y/n): ")
                if confirm.lower() != 'y':
                    continue
            
            new_reservation = Reservation(customer_name, contact, isbn)
            reservations.enqueue(new_reservation)
            print(f"Reservation added: {new_reservation}")
        
        elif choice == '6':
            print("\n----- Reservation Queue -----")
            reservations.display()
        
        elif choice == '7':
            print("\n----- Find Reservations by ISBN -----")
            isbn = input("Enter ISBN to search: ")
            matching_reservations = reservations.search_by_isbn(isbn)
            
            if matching_reservations:
                print(f"Found {len(matching_reservations)} reservations for ISBN {isbn}:")
                for i, res in enumerate(matching_reservations, 1):
                    print(f"{i}. {res}")
            else:
                print(f"No reservations found for ISBN: {isbn}")
        
        elif choice == '8':
            print("\n----- Process Next Reservation -----")
            next_reservation = reservations.dequeue()
            
            if next_reservation:
                print(f"Processing reservation: {next_reservation}")
                book = inventory.find_by_isbn(next_reservation.isbn)
                
                if book:
                    print(f"Book is available: {book}")
                    sell = input("Sell book to customer? (y/n): ")
                    
                    if sell.lower() == 'y':
                        inventory.remove_by_isbn(next_reservation.isbn)
                        print(f"Book sold to {next_reservation.customer_name}")
                    else:
                        reservations.enqueue(next_reservation)
                        print("Reservation returned to queue")
                else:
                    print(f"Book with ISBN {next_reservation.isbn} not in inventory")
                    reservations.enqueue(next_reservation)
                    print("Reservation returned to queue")
            else:
                print("No reservations in queue")
        
        elif choice == '9':
            print("Thank you for using the Book Inventory and Reservation System!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
