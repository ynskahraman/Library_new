class Library:
    def __init__(self):
        self.logged_in_user = None
        self.user_type = None
        self.library_name = None
        self.books_file = open("books.txt", "a+", encoding="utf-8")
        self.users_file = open("users.txt", "a+", encoding="utf-8")
        self.admins_file = open("admins.txt", "a+", encoding="utf-8")
        self.librarians_file_path = "librarians.txt"
        self.history_file = open("history_file.txt", 'a')
        self.librarians_file = open(self.librarians_file_path, "a+", encoding="utf-8")
        self.transactions_file = open("transactions.txt", "a+", encoding="utf-8")
        self.ratings_file = open("ratings.txt", "a+", encoding="utf-8")
        self.cities_file = open("cities.txt", "r", encoding="utf-8")
        self.libraries_file_path = 'libraries.txt'
        self.librarians = {}

    def __del__(self):
        # Close all opened files
        self.books_file.close()
        self.users_file.close()
        self.admins_file.close()
        self.history_file.close()
        self.librarians_file.close()
        self.transactions_file.close()
        self.ratings_file.close()
        self.cities_file.close()

    # Additional methods (login, create_library, etc.) would follow
    def get_average_ratings(self):
        with open("ratings.txt", "r") as f:
            ratings = f.readlines()

        if not ratings:
            print("There is no rated book yet.")
            return {}

        book_ratings = {}
        for rating in ratings:
            user, title, score = rating.strip().split(',')
            score = int(score)
            if title not in book_ratings:
                book_ratings[title] = [score]
            else:
                book_ratings[title].append(score)

        average_ratings = {}
        for title, scores in book_ratings.items():
            average_rating = sum(scores) / len(scores)
            average_ratings[title] = average_rating

        return average_ratings

    def rate_book(self):
        print("*** BORROWED BOOKS ***")
        # List borrowed books (you might want to call your list_borrowed_books method here)
        borrowed_books = self.get_borrowed_books()  # Assume this method fetches borrowed books
        for book in borrowed_books:
            print(book)  # Display borrowed books

        title = input("Enter the title of the book to rate: ")

        # Loop until a valid rating is provided
        while True:
            try:
                rating = int(input("Enter your rating (1-5): "))
                if 1 <= rating <= 5:
                    # Here you can save the rating to your storage (e.g., file or database)
                    print("Thank you for your rating!")
                    # Logic to save the rating goes here
                    break  # Exit the loop since we have a valid rating
                else:
                    print("Invalid rating. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        # Return to the user menu or perform other actions as necessary

    def search_books(self):
        search_term = input("Enter search term (title or author): ").lower()
        found_books = []

        # Move to the beginning of the books_file
        self.books_file.seek(0)
        for book in self.books_file:
            # Split the book details
            details = book.strip().split(',')
            name, author = details[0], details[1]  # Assuming first two entries are title and author

            # Check if the search term matches title or author
            if search_term in name.lower() or search_term in author.lower():
                found_books.append(book.strip())

        # Print the results
        if not found_books:
            print("No matching books found.")
        else:
            print("*************************************************************************************")
            for i, book in enumerate(found_books, start=1):
                details = book.split(',')
                print(
                    f"{i}) Title: {details[0]}, Author: {details[1]}, Release Date: {details[2]}, Pages: {details[3]}")
            print("*************************************************************************************")

    def sort_books(self):
        while True:
            print("*** SORT BOOKS ***")
            print("1) Sort by Title")
            print("2) Sort by Author")
            print("q) Quit")
            choice = input("Enter your choice (1/2/q): ")
            if choice == "1":
                self.sort_books_by("title")
            elif choice == "2":
                self.sort_books_by("author")
            elif choice.lower() == "q":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def sort_books_by(self, key):
        # Move to the beginning of the books_file
        self.books_file.seek(0)
        books = self.books_file.readlines()

        # Sort the books based on the selected key
        books.sort(key=lambda x: x.split(',')[0] if key == 'title' else x.split(',')[1])

        # Move to the beginning of the file and truncate it
        self.books_file.seek(0)
        self.books_file.truncate()

        # Write sorted books back to the file
        for book in books:
            self.books_file.write(book)

        print("Books sorted successfully.")

        # Display the sorted books
        print("\n*** Sorted Books ***")
        for i, book in enumerate(books, start=1):
            try:
                # Attempt to unpack the book details
                name, author, release_date, pages, username = book.strip().split(',')
                print(
                    f"{i}) Title: {name}, Author: {author}, Release Date: {release_date}, Pages: {pages}, Borrowed by: {username}")
            except ValueError:
                print(f"Error processing book entry: {book.strip()}")

        print("*************************************************************************************")

    def add_book(self):
        # Check if the user is a librarian before allowing book addition
        if self.user_type != "librarian":
            print("Only librarians can add books.")
            return

        name = input("Enter book title: ").strip()

        # Validate author name
        author = ""
        while True:
            author = input("Enter book author: ").strip()
            if author.replace(" ", "").isalpha():
                break
            print("Error: Author name cannot contain numbers. Please enter a valid author name.")

        # Validate release year
        release_year = ""
        while True:
            release_year = input("Enter book release year (YYYY): ").strip()
            if release_year.isdigit() and len(release_year) == 4:
                release_year = int(release_year)  # Convert to integer
                break
            print("Error: Please enter a valid year in the format YYYY.")

        # Validate number of pages
        pages = ""
        while True:
            pages = input("Enter number of pages: ").strip()
            if pages.isdigit() and int(pages) > 0:
                pages = int(pages)
                break
            print("Error: Please enter a valid number of pages greater than zero.")

        # Save the book to the books.txt file with library information
        with open("books.txt", "a") as books_file:
            # Assuming self.library_name and self.city_name are set correctly during login
            books_file.write(f"{name}, {author}, {release_year}, {pages}, {self.library_name}, {self.city_name}\n")

        print(f"Book '{name}' by {author} added to the library '{self.library_name}' in {self.city_name}.")

    def normalize_string(text):
        """
        Normalize Turkish characters in a string.
        Converts Turkish characters to their ASCII equivalents.
        """
        turkish_map = {
            'ı': 'i', 'İ': 'i',
            'ğ': 'g', 'Ğ': 'g',
            'ü': 'u', 'Ü': 'u',
            'ş': 's', 'Ş': 's',
            'ö': 'o', 'Ö': 'o',
            'ç': 'c', 'Ç': 'c',
            'â': 'a', 'Â': 'a'
        }
        return ''.join(turkish_map.get(c, c) for c in text)

    def create_library(self):
        while True:  # Loop until a valid city is provided
            city_name = input("Enter the city name for the new library: ").strip()

            if self.check_city_exists(city_name):
                library_name = input("Enter the name for the new library: ").strip()

                # Validate library name
                if not library_name:
                    print("Library name cannot be empty. Please try again.")
                    continue

                try:
                    # Save library name and city to libraries.txt
                    with open(self.libraries_file_path, 'a') as libraries_file:
                        libraries_file.write(f"{library_name}, {city_name}\n")
                    print(f"Library '{library_name}' created in {city_name}.")
                    break  # Exit the loop after successfully creating the library
                except IOError as e:
                    print(f"An error occurred while saving the library: {e}")
            else:
                print("City name is not valid. Please try again.")

    def prompt_non_empty_input(prompt_message):
        while True:
            user_input = input(prompt_message).strip()
            if user_input:  # If input is not empty
                return user_input
            else:
                print("Input cannot be empty. Please try again.")

    def remove_book(self):
        self.list_books()
        book_number = input("Enter the number of the book to remove: ")
        self.file.seek(0)
        books = self.file.readlines()
        self.file.seek(0)
        self.file.truncate()
        book_removed = False
        for i, book in enumerate(books, start=1):
            if i != int(book_number):
                self.file.write(book)
            else:
                book_info = book.split(',')
                if len(book_info) == 5 and book_info[-1].strip() != "":
                    print("Cannot remove borrowed book.")
                else:
                    book_removed = True
        if book_removed:
            print("Book removed successfully.")
        else:
            print(f"There is no book with number {book_number} in the library.")

    def check_library_exists(self, library_name, city_name):
        # Check if the specified library exists in the libraries.txt file
        with open(self.libraries_file_path, 'r', encoding='utf-8') as libraries_file:
            libraries = [
                line.strip().split(', ')
                for line in libraries_file.readlines()
            ]
            return any(
                lib_name.lower() == library_name.lower() and city.lower() == city_name.lower() for lib_name, city in
                libraries)

    def list_books(self):
        print("*************************************************************************************")
        found_books = False  # Track if any books are found for the library

        try:
            with open("books.txt", "r") as books_file:
                for line in books_file:
                    # Split line and unpack values, ensuring to handle lines correctly
                    parts = line.strip().split(', ')
                    if len(parts) < 6:
                        print("Skipping invalid line:", line.strip())
                        continue  # Skip invalid lines

                    title, author, release_year, pages, library_name, city_name = parts

                    # Check if the book belongs to the librarian's library
                    if library_name.strip().lower() == self.library_name.strip().lower():
                        print(
                            f"Title: {title}, Author: {author}, Release Year: {release_year}, Pages: {pages}, Borrowed by: None")
                        found_books = True  # Mark that we found at least one book

        except FileNotFoundError:
            print("Error: books.txt file not found.")
        except Exception as e:
            print(f"An error occurred while reading the books file: {e}")

        if not found_books:
            print("No books found for your library.")

    def delete_user(self):
        username = input("Enter username of the user to delete: ").strip()

            # Read all users from the file
        users = []
        user_found = False

        try:
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    user_info = line.strip().split(',')
                    if user_info[0] == username:
                        user_found = True
                        continue  # Skip the user to delete
                    users.append(line.strip())  # Collect remaining users

            if user_found:
                    # Write remaining users back to the file
                with open("users.txt", "w", encoding="utf-8") as f:
                    for user in users:
                        f.write(f"{user}\n")
                print(f"User '{username}' deleted successfully.")
            else:
                print(f"User '{username}' not found.")

        except FileNotFoundError:
            print("The user file does not exist.")

        # Example of how to call delete_user from an admin menu
        def admin_menu(self):
            while True:
                print("\n*** ADMIN MENU ***")
                print("1) Delete User")
                print("2) Exit")
                choice = input("Enter your choice: ")

                if choice == '1':
                    self.delete_user()
                elif choice == '2':
                    break
                else:
                    print("Invalid choice. Please try again.")

    def list_users(self):
        self.users_file.seek(0)
        users = self.users_file.readlines()
        print("Users in the library:")
        for user in users:
            # Split the user string into components
            user_details = user.strip().split(',')
            if len(user_details) >= 4:  # Ensure there are enough details
                username = user_details[0]
                library = user_details[2]
                city = user_details[3]
                print(f" username:{username} library:{library}, City: {city}")
            else:
                print("Invalid user entry format.")

    def list_librarians(self):
        """List all librarians without revealing their passwords."""
        print("Librarians in the library:")
        try:
            with open(self.librarians_file_path, "r", encoding="utf-8") as librarians_file:
                for line in librarians_file:
                    if line.strip():  # Make sure to skip empty lines
                        # Split line into components
                        name, _, library, city = line.strip().split(',')
                        # Print only the name and city
                        print(f"{name} from {library} library, from {city}")
        except FileNotFoundError:
            print("No librarians found.")

    def login(self):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        # Check if the user is a librarian
        if self.check_credentials(self.librarians_file_path, username, password):
            self.logged_in_user = username
            self.user_type = "librarian"

            # Get the library name and city from the librarian file
            with open(self.librarians_file_path, 'r') as librarians_file:
                for line in librarians_file:
                    stored_username, stored_password, library_name, city_name = line.strip().split(',')
                    if stored_username == username and stored_password == password:
                        self.library_name = library_name  # Store the library name
                        self.city_name = city_name  # Store the city name
                        print(
                            f"Welcome, {username}! You are logged in to the library: {self.library_name} in {self.city_name}.")
                        return True, "librarian"

        # Check if the user is a regular user
        if self.check_credentials(self.users_file.name, username, password):
            self.logged_in_user = username
            self.user_type = "user"
            return True, "user"

        # Check if the user is an admin
        if self.check_credentials(self.admins_file.name, username, password):
            self.logged_in_user = username
            self.user_type = "admin"
            return True, "admin"

        print("Invalid credentials.")
        return False, None

    def login_user(self):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        with open(self.users_file.name, 'r', encoding='utf-8') as users_file:
            for line in users_file:
                stored_username, stored_password, library_name, _ = line.strip().split(',')
                if stored_username == username and stored_password == password:
                    print(f"Welcome back, {username}!")
                    print(f"You are logged in to the library: {library_name}")  # Display library name
                    self.logged_in_user = username
                    self.user_type = "user"
                    self.library_name = library_name  # Store the library name
                    return

        print("Invalid username or password.")

    def check_credentials(self, file_path, username, password):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                stored_username, stored_password, *rest = line.strip().split(',')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def register_user(self):
        city_name = input("Enter your city name: ").strip()
        libraries = self.get_libraries_in_city(city_name)

        if not libraries:
            print(f"No libraries found in {city_name}. Please try again.")
            return

        print("Available libraries:")
        for index, library in enumerate(libraries, start=1):
            print(f"{index}) {library}")

        library_choice = input("Select a library by number: ").strip()

        try:
            library_index = int(library_choice) - 1
            selected_library = libraries[library_index]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
            return

        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        self.save_user(username, password, selected_library, city_name)
        print(f"User '{username}' registered successfully for the library '{selected_library}' in {city_name}.")

    def get_libraries_in_city(self, city_name):
        libraries = []
        # Read from the libraries.txt file or however you're storing libraries
        with open(self.libraries_file_path, 'r', encoding='utf-8') as libraries_file:
            for line in libraries_file:
                library_name, library_city = line.strip().split(',')
                # Normalize the case for comparison
                if library_city.strip().lower() == city_name.strip().lower():
                    libraries.append(library_name.strip())
        return libraries

    def save_user(self, username, password, library, city):
        with open(self.users_file.name, 'a', encoding='utf-8') as users_file:
            users_file.write(f"{username},{password},{library},{city}\n")
            users_file.flush()  # Ensure data is written to the file

    def create_librarian(self):
        # Create a new librarian by checking if the library exists
        city_name = input("Enter the city name where the library is located: ").strip()
        library_name = input("Enter the name of the library: ").strip()

        if self.check_library_exists(library_name, city_name):
            librarian_name = input("Enter the librarian's name: ").strip()
            librarian_password = input("Enter the librarian's password: ").strip()
            # Save librarian details to librarians.txt
            with open(self.librarians_file_path, 'a', encoding='utf-8') as librarians_file:
                librarians_file.write(f"{librarian_name},{librarian_password},{library_name},{city_name}\n")
            print(f"Librarian '{librarian_name}' created for the library '{library_name}' in {city_name}.")
        else:
            print("Library does not exist. Please check the library name and city.")

    def delete_librarian(self):
        """Delete a librarian based on their city."""
        city_name = input("Enter the city name: ").strip()
        found_librarians = []

        # First, list librarians in the specified city
        with open(self.librarians_file_path, "r", encoding="utf-8") as librarians_file:
            for line in librarians_file:
                if line.strip():  # Ensure the line is not empty
                    name, _, surname, librarian_city = line.strip().split(',')
                    if librarian_city.lower() == city_name.lower():
                        found_librarians.append((name, surname, line.strip()))

        # If no librarians found, inform the user
        if not found_librarians:
            print("No librarians found in that city.")
            return

        # Display the found librarians
        print("Found the following librarians:")
        for idx, (name, surname, full_line) in enumerate(found_librarians):
            print(f"{idx + 1}) {name} {surname}")

        # Ask the user which librarian to delete
        choice = int(input(f"Enter the number of the librarian you want to delete (1-{len(found_librarians)}): "))

        if 1 <= choice <= len(found_librarians):
            librarian_to_delete = found_librarians[choice - 1][2]  # Get the full line to delete
            # Now delete the librarian
            with open(self.librarians_file_path, "r", encoding="utf-8") as librarians_file:
                lines = librarians_file.readlines()

            with open(self.librarians_file_path, "w", encoding="utf-8") as librarians_file:
                for line in lines:
                    if line.strip() != librarian_to_delete.strip():  # Write back all lines except the one to delete
                        librarians_file.write(line)

            print(f"Librarian '{librarian_to_delete}' deleted successfully.")
        else:
            print("Invalid choice. Please try again.")

    def delete_account(self):
        if self.user_type == "librarian":
            self.delete_librarian(self.logged_in_user)
            self.logged_in_user = None
            print("Logging out...")
        else:
            print("Only librarians can delete their accounts.")

    def create_library(self):
        while True:  # Loop until a valid city is provided
            city_name = input("Enter the city name for the new library: ").strip()

            if self.check_city_exists(city_name):
                library_name = input("Enter the name for the new library: ").strip()
                # Save library name and city to libraries.txt
                with open(self.libraries_file_path, 'a') as libraries_file:
                    libraries_file.write(f"{library_name}, {city_name}\n")
                print(f"Library '{library_name}' created in {city_name}.")
                break  # Exit the loop after successfully creating the library
            else:
                print("City name is not valid. Please try again.")

    def run(self):
        while True:
            print("*** WELCOME TO THE LIBRARY SYSTEM ***")
            print("1) Login")
            print("2) Register as User")
            print("3) Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                success, user_type = self.login()
                if success:
                    if user_type == "admin":
                        self.admin_menu()
                    elif user_type == "librarian":
                        self.librarian_menu()
                    else:
                        self.user_menu()
            elif choice == "2":
                self.register_user()
            elif choice == "3":
                print("Exiting the library system.")
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_menu(self):
        while True:
            print("*** ADMIN MENU ***")
            print("1) List Books")
            print("2) Add Book")
            print("3) Remove Book")
            print("4) List Users")
            print("5) List Librarians")
            print("6) Get Libraries")
            print("7) Create Library")
            print("8) Create Librarian")
            print("9) Delete Librarian")
            print("10) Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.list_books()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.remove_book()
            elif choice == "4":
                self.list_users()
            elif choice == "5":
                self.list_librarians()
            elif choice == "6":
                self.get_libraries_in_city()
            elif choice == '7':
                self.create_library()
            elif choice == '8':
                self.create_librarian()
            elif choice == '9':
                self.delete_librarian()
            elif choice == '10':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def librarian_menu(self):
        while True:
            print("*** LIBRARIAN MENU ***")
            print("1) List Books")
            print("2) Add Book")
            print("3) Remove Book")
            print("4) Delete My Account")
            #added new
            print("5) List Users")
            print("6) List Borrowed Books")
            print("7) Search Books")
            print("8) Sort Books")
            print("9) See Average Ratings")
            #end of news
            print("10) Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.list_books()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.remove_book()
            elif choice == "4":
                self.delete_account()
            elif choice == "5":
                self.list_users()
            elif choice == "6":
                self.list_borrowed_books()
            elif choice == "7":
                self.search_books()
            elif choice == "8":
                self.sort_books()
            elif choice == "9":
                average_ratings = self.get_average_ratings()
                for title, rating in average_ratings.items():
                    print(f"Title: {title}, Average Rating: {rating}")
            elif choice == "10":
                print("Logging out...")
                self.logged_in_user = None
                break
            else:
                print("Invalid choice. Please try again.")

    def update_password(self):
        if not self.logged_in_user:
            print("You need to be logged in to update your password.")
            return

        current_password = input("Enter your current password: ").strip()
        new_password = input("Enter your new password: ").strip()
        confirm_password = input("Confirm your new password: ").strip()

        if new_password != confirm_password:
            print("Error: The new passwords do not match.")
            return

        file_path = None
        if self.user_type == "librarian":
            file_path = self.librarians_file_path
        elif self.user_type == "user":
            file_path = self.users_file.name
        elif self.user_type == "admin":
            file_path = self.admins_file.name

        if file_path and self.check_credentials(file_path, self.logged_in_user, current_password):
            self._update_password_in_file(file_path, self.logged_in_user, new_password)
            print("Password updated successfully.")
        else:
            print("Error: Current password is incorrect.")

    def _update_password_in_file(self, file_path, username, new_password):
        with open(file_path, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()

            for line in lines:
                stored_username, stored_password, *rest = line.strip().split(',')
                if stored_username == username:
                    # Replace the old password with the new one
                    file.write(f"{username},{new_password},{','.join(rest)}\n")
                else:
                    file.write(line)

    def user_menu(self):
        while True:
            print("*** USER MENU ***")
            print("1) List Books")
            print("2) Borrow Book")
            print("3) Return Book")
            print("4) Update Password")
            #new
            print("5) List Borrowed Books")
            print("6) Search Books")
            print("7) Sort Books")
            print("8) Rate Book")
            print("9) See Average Ratings")
            #new ends
            print("10) Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.list_books()
            elif choice == "2":
                self.borrow_book()
            elif choice == "3":
                self.return_book()
            elif choice == "4":
                self.update_password()
            elif choice == "5":
                self.list_borrowed_books()
            elif choice == "6":
                self.search_books()
            elif choice == "7":
                self.sort_books()
            elif choice == "8":
                self.rate_book()
            elif choice == "9":
                average_ratings = self.get_average_ratings()
                for title, rating in average_ratings.items():
                    print(f"Title: {title}, Average Rating: {rating}")
            elif choice == "10":
                print("Logging out...")
                self.logged_in_user = None
                break
            else:
                print("Invalid choice. Please try again.")

    def borrow_book(self):
        self.list_books()  # Display available books to the user
        book_title = input("Enter the title of the book to borrow: ").strip()

        book_found = False
        book_borrowed = False

        # Read the books from the file
        self.books_file.seek(0)
        books = self.books_file.readlines()

        # Read the transactions file to check borrowed books
        self.transactions_file.seek(0)
        borrowed_books = {}
        for transaction in self.transactions_file:
            transaction = transaction.strip()
            if transaction:  # Check if line is not empty
                try:
                    borrowed_book_title, borrower = transaction.split(',')
                    borrowed_books[borrowed_book_title.lower()] = borrower.strip()
                except ValueError:
                    continue  # Skip invalid lines

        updated_books = []  # Prepare to write back to the file

        for book in books:
            book_info = book.strip().split(',')
            if len(book_info) < 5:
                continue  # Ensure there are enough fields

            title, author, release_year, pages, library_name, *other = book_info

            if title.strip().lower() == book_title.lower() and library_name.strip() == self.library_name:
                book_found = True

                # Check if the book is already borrowed
                if title.lower() in borrowed_books:
                    if borrowed_books[title.lower()] == self.logged_in_user:
                        print(f"You have already borrowed '{title}'.")
                        return
                    else:
                        print(f"Book '{title}' is already borrowed by {borrowed_books[title.lower()]}.")
                        return

                # Mark the book as borrowed
                print(f"Book '{title}' borrowed successfully.")
                borrowed_books[title.lower()] = self.logged_in_user  # Record that the user borrowed this book
                book_borrowed = True

            updated_books.append(','.join([title, author, release_year, pages, library_name] + other))

        if not book_found:
            print(f"Book '{book_title}' not found in your library.")
            return

        if book_borrowed:
            # Write the updated book data back to the file
            self.books_file.seek(0)
            self.books_file.truncate()
            self.books_file.write('\n'.join(updated_books) + '\n')

            # Record the transaction
            with open(self.transactions_file.name, 'a') as transactions_file:
                transactions_file.write(f"{book_title},{self.logged_in_user}\n")

    def return_book(self):
        print("*** BORROWED BOOKS ***")

        # Read the transactions file to get borrowed books
        self.transactions_file.seek(0)
        user_books = []

        for transaction in self.transactions_file:
            transaction = transaction.strip()
            if transaction:  # Check if line is not empty
                try:
                    book_title, borrower = transaction.split(',')
                    if borrower.strip() == self.logged_in_user:
                        user_books.append(book_title.strip())
                        print(f"- {book_title.strip()}")
                except ValueError:
                    continue  # Skip invalid lines

        if not user_books:
            print("You haven't borrowed any books.")
            return

        book_title = input("Enter the title of the book to return: ").strip()

        if book_title.lower() not in [b.lower() for b in user_books]:
            print(f"Book '{book_title}' is not currently borrowed by you.")
            return

        # Remove this transaction from transactions file
        self.transactions_file.seek(0)
        transactions = self.transactions_file.readlines()
        self.transactions_file.seek(0)
        self.transactions_file.truncate()

        for transaction in transactions:
            transaction = transaction.strip()
            if transaction:  # Check if line is not empty
                try:
                    current_title, current_borrower = transaction.split(',')
                    if not (book_title.lower() == current_title.lower() and
                            self.logged_in_user == current_borrower.strip()):
                        self.transactions_file.write(transaction + '\n')
                except ValueError:
                    self.transactions_file.write(transaction + '\n')  # Keep invalid lines

        print(f"Book '{book_title}' returned successfully.")

    def list_borrowed_books(self):
        try:
            self.transactions_file.seek(0)  # Ensure we're at the beginning of the file
            transactions = self.transactions_file.readlines()

            print("*** BORROWED BOOKS ***")
            for transaction in transactions:
                # Strip the line and skip if it's empty
                transaction = transaction.strip()
                if not transaction:  # Skip empty lines
                    continue

                try:
                    title, user = transaction.split(',')  # Split only if there are two values
                    print(f"{title} - Borrowed by {user}")
                except ValueError as e:
                    print(f"Skipping line due to format issue: {transaction} ({e})")

        except Exception as e:
            print(f"Error reading transactions: {e}")

    def get_borrowed_books(self):
        try:
            with open('borrowed_books.txt', 'r') as file:  # Assuming you are using a text file
                transactions = file.readlines()

            borrowed_books = [transaction.strip().split(',')[0] for transaction in transactions if
                              transaction.strip().split(',')[1] == self.logged_in_user]
            return borrowed_books
        except FileNotFoundError:
            print("No borrowed books found.")
            return []

    def remove_borrowed_book(self, title):
        self.transactions_file.seek(0)
        transactions = self.transactions_file.readlines()
        self.transactions_file.seek(0)
        self.transactions_file.truncate()
        for transaction in transactions:
            if transaction.strip().split(',')[0] != title or transaction.strip().split(',')[1] != self.logged_in_user:
                self.transactions_file.write(transaction)

    def is_book_borrowed(self, title):
        self.transactions_file.seek(0)
        transactions = self.transactions_file.readlines()
        for transaction in transactions:
            if transaction.strip().split(',')[0] == title:
                return True
        return False

    def check_city_exists(self, city_name):
        """Check if the given city name exists in cities.txt (case insensitive)."""
        self.cities_file.seek(0)
        cities = [line.strip().lower() for line in self.cities_file if line.strip()]
        print(f"Checking if '{city_name}' exists...")  # Debug output
        return city_name.lower() in cities

if __name__ == "__main__":
    library = Library()
    try:
        library.run()
    except KeyboardInterrupt:
        print("\nExiting the program...")



