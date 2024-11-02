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
        try:
            with open("ratings.txt", "r") as f:
                ratings = f.readlines()

            if not ratings:
                print("There is no rated book yet.")
                return {}

            book_ratings = {}
            for rating in ratings:
                # Skip empty lines
                if not rating.strip():
                    continue

                # Split the line and ensure it has exactly three parts
                parts = rating.strip().split(',')
                if len(parts) != 3:
                    print(f"Skipping invalid line in ratings file: '{rating.strip()}'")
                    continue  # Skip lines that don't have exactly 3 items

                user, title, score = parts
                try:
                    score = int(score)  # Convert score to integer
                    if title not in book_ratings:
                        book_ratings[title] = [score]
                    else:
                        book_ratings[title].append(score)
                except ValueError:
                    print(f"Skipping line with invalid score: '{rating.strip()}'")
                    continue  # Skip lines where score is not an integer

            average_ratings = {}
            for title, scores in book_ratings.items():
                average_rating = sum(scores) / len(scores)
                average_ratings[title] = average_rating

            if average_ratings:
                print("*** AVERAGE RATINGS ***")
                for title, avg_rating in average_ratings.items():
                    print(f"{title}: {avg_rating:.2f}")
            else:
                print("No average ratings available.")

            return average_ratings
        except FileNotFoundError:
            print("Error: ratings.txt file not found.")
            return {}

    def rate_book(self):
        print("*** BORROWED BOOKS ***")
        borrowed_books = self.get_borrowed_books()

        if not borrowed_books:
            print("You have no borrowed books to rate.")
            return

        for book in borrowed_books:
            print(f"- {book}")

        title = input("Enter the title of the book to rate: ").strip()

        if title.lower() not in [b.lower() for b in borrowed_books]:
            print(f"You have not borrowed the book titled '{title}'.")
            return

        with open("ratings.txt", "r") as f:
            ratings = f.readlines()

        for rating in ratings:
            user, rated_title, _ = rating.strip().split(',')
            if user == self.logged_in_user and rated_title.lower() == title.lower():
                print("You have already rated this book.")
                return

        while True:
            try:
                rating = int(input("Enter your rating (1-5): "))
                if 1 <= rating <= 5:
                    with open("ratings.txt", "a") as f:
                        f.write(f"{self.logged_in_user},{title},{rating}\n")
                    print("Thank you for your rating!")
                    break
                else:
                    print("Invalid rating. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

    def search_books(self):
        search_term = input("Enter search term (title or author): ")
        results = []

        try:
            with open("books.txt", "r", encoding="utf-8") as books_file:
                for line in books_file:

                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        title = parts[0]
                        author = parts[1]
                        if search_term.lower() in title.lower() or search_term.lower() in author.lower():
                            results.append(line.strip())
        except UnicodeDecodeError:
            print("Checking the shells...")
            with open("books.txt", "r", encoding="windows-1252") as books_file:
                for line in books_file:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        title = parts[0]
                        author = parts[1]
                        if search_term.lower() in title.lower() or search_term.lower() in author.lower():
                            results.append(line.strip())

        if results:
            print("Search Results:")
            for book in results:
                print(book)
        else:
            print("No books found matching your search.")

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

    def sort_books_by(self, criterion):
        books = []

        try:
            with open("books.txt", "r", encoding="utf-8") as books_file:
                books = books_file.readlines()
        except UnicodeDecodeError:
            print("UTF-8 decoding error detected. Trying with a different encoding.")
            with open("books.txt", "r", encoding="windows-1252") as books_file:
                books = books_file.readlines()


        books = [line.strip() for line in books if line.strip()]


        books_with_details = []
        for line in books:
            parts = line.split(',')
            if len(parts) >= 2:
                title = parts[0].strip()
                author = parts[1].strip()
                books_with_details.append((title, author, line))


        if criterion == "title":
            books_with_details.sort(key=lambda x: x[0].lower())
        elif criterion == "author":
            books_with_details.sort(key=lambda x: x[1].lower())


        print("Sorted Books:")
        for title, author, original_line in books_with_details:
            print(original_line)

    def add_book(self):

        if self.user_type != "librarian":
            print("Only librarians can add books.")
            return

        name = input("Enter book title: ").strip()


        author = ""
        while True:
            author = input("Enter book author: ").strip()
            if author.replace(" ", "").isalpha():
                break
            print("Error: Author name cannot contain numbers. Please enter a valid author name.")


        release_year = ""
        while True:
            release_year = input("Enter book release year (YYYY): ").strip()
            if release_year.isdigit() and len(release_year) == 4:
                release_year = int(release_year)  # Convert to integer
                break
            print("Error: Please enter a valid year in the format YYYY.")


        pages = ""
        while True:
            pages = input("Enter number of pages: ").strip()
            if pages.isdigit() and int(pages) > 0:
                pages = int(pages)
                break
            print("Error: Please enter a valid number of pages greater than zero.")


        with open("books.txt", "a") as books_file:

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


                if not library_name:
                    print("Library name cannot be empty. Please try again.")
                    continue

                try:

                    with open(self.libraries_file_path, 'a') as libraries_file:
                        libraries_file.write(f"{library_name}, {city_name}\n")
                    print(f"Library '{library_name}' created in {city_name}.")
                    break
                except IOError as e:
                    print(f"An error occurred while saving the library: {e}")
            else:
                print("City name is not valid. Please try again.")

    def prompt_non_empty_input(prompt_message):
        while True:
            user_input = input(prompt_message).strip()
            if user_input:
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
        found_books = False

        try:
            with open("books.txt", "r") as books_file:
                for line in books_file:
                    parts = line.strip().split(', ')
                    if len(parts) < 5:
                        print("Skipping invalid line:", line.strip())
                        continue

                    title, author, release_year, pages, library_name = parts[:5]

                    if library_name.strip().lower() == self.library_name.strip().lower():
                        print(f"Title: {title}, Author: {author}, Year: {release_year}, Pages: {pages}")
                        found_books = True

        except FileNotFoundError:
            print("Error: books.txt file not found.")
        except Exception as e:
            print(f"An error occurred while reading the books file: {e}")

        if not found_books:
            print("No books found for your library.")



    def list_users(self):
        self.users_file.seek(0)
        users = self.users_file.readlines()
        print("Users in the library:")
        for user in users:

            user_details = user.strip().split(',')
            if len(user_details) >= 4:
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
                    if line.strip():

                        name, _, library, city = line.strip().split(',')

                        print(f"{name} from {library} library, from {city}")
        except FileNotFoundError:
            print("No librarians found.")

    def login(self):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()


        if self.check_credentials(self.librarians_file_path, username, password):
            self.logged_in_user = username
            self.user_type = "librarian"


            with open(self.librarians_file_path, 'r') as librarians_file:
                for line in librarians_file:
                    stored_username, stored_password, library_name, city_name = line.strip().split(',')
                    if stored_username == username and stored_password == password:
                        self.library_name = library_name  # Store the library name
                        self.city_name = city_name  # Store the city name
                        print(
                            f"Welcome, {username}! You are logged in to the library: {self.library_name} in {self.city_name}.")
                        return True, "librarian"


        if self.check_credentials(self.users_file.name, username, password):
            self.logged_in_user = username
            self.user_type = "user"
            with open(self.users_file.name, 'r') as users_file:
                for line in users_file:
                    stored_username, stored_password, library_name, city_name = line.strip().split(',')
                    if stored_username == username and stored_password == password:
                        self.library_name = library_name
                        self.city_name = city_name
                        print(
                            f"Welcome, {username}! You are logged in to the library: {self.library_name} in {self.city_name}.")
                        return True, "User"


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
                    print(f"You are logged in to the library: {library_name}")
                    self.logged_in_user = username
                    self.user_type = "user"
                    self.library_name = library_name
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

        with open(self.libraries_file_path, 'r', encoding='utf-8') as libraries_file:
            for line in libraries_file:
                library_name, library_city = line.strip().split(',')

                if library_city.strip().lower() == city_name.strip().lower():
                    libraries.append(library_name.strip())
        return libraries

    def save_user(self, username, password, library, city):
        with open(self.users_file.name, 'a', encoding='utf-8') as users_file:
            users_file.write(f"{username},{password},{library},{city}\n")
            users_file.flush()

    def create_librarian(self):

        city_name = input("Enter the city name where the library is located: ").strip()
        library_name = input("Enter the name of the library: ").strip()

        if self.check_library_exists(library_name, city_name):
            librarian_name = input("Enter the librarian's name: ").strip()
            librarian_password = input("Enter the librarian's password: ").strip()

            with open(self.librarians_file_path, 'a', encoding='utf-8') as librarians_file:
                librarians_file.write(f"{librarian_name},{librarian_password},{library_name},{city_name}\n")
            print(f"Librarian '{librarian_name}' created for the library '{library_name}' in {city_name}.")
        else:
            print("Library does not exist. Please check the library name and city.")

    def delete_librarian(self):
        """Delete a librarian based on their city."""
        city_name = input("Enter the city name: ").strip()
        found_librarians = []


        with open(self.librarians_file_path, "r", encoding="utf-8") as librarians_file:
            for line in librarians_file:
                if line.strip():
                    name, _, surname, librarian_city = line.strip().split(',')
                    if librarian_city.lower() == city_name.lower():
                        found_librarians.append((name, surname, line.strip()))


        if not found_librarians:
            print("No librarians found in that city.")
            return


        print("Found the following librarians:")
        for idx, (name, library, full_line) in enumerate(found_librarians):
            print(f"{idx + 1}) {name} from {library} library")


        choice = int(input(f"Enter the number of the librarian you want to delete (1-{len(found_librarians)}): "))

        if 1 <= choice <= len(found_librarians):
            librarian_to_delete = found_librarians[choice - 1][2]

            with open(self.librarians_file_path, "r", encoding="utf-8") as librarians_file:
                lines = librarians_file.readlines()

            with open(self.librarians_file_path, "w", encoding="utf-8") as librarians_file:
                for line in lines:
                    if line.strip() != librarian_to_delete.strip():
                        librarians_file.write(line)

            print(f"Librarian '{librarian_to_delete}' deleted successfully.")
        else:
            print("Invalid choice. Please try again.")


    def create_library(self):
        while True:
            city_name = input("Enter the city name for the new library: ").strip()

            if self.check_city_exists(city_name):
                library_name = input("Enter the name for the new library: ").strip()

                with open(self.libraries_file_path, 'a') as libraries_file:
                    libraries_file.write(f"{library_name}, {city_name}\n")
                print(f"Library '{library_name}' created in {city_name}.")
                break
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
            print("1) List Librarians")
            print("2) Get Libraries")
            print("3) Create Library")
            print("4) Create Librarian")
            print("5) Delete Librarian")
            print("6) Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.list_librarians()
            elif choice == "2":
                city_name = input("Enter the city name to get libraries: ")
                libraries = self.get_libraries_in_city(city_name)

                if libraries:
                    print(f"Libraries in {city_name}:")
                    for library in libraries:
                        print(f"- {library}")
                else:
                    print(f"No libraries found in {city_name}.")
            elif choice == '3':
                self.create_library()
            elif choice == '4':
                self.create_librarian()
            elif choice == '5':
                self.delete_librarian()
            elif choice == '6':
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
            #added new
            print("4) List Users")
            print("5) List Borrowed Books")
            print("6) Search Books")
            print("7) Sort Books")
            print("8) See Average Ratings")
            #end of news
            print("9) Logout")
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
                self.list_borrowed_books()
            elif choice == "6":
                self.search_books()
            elif choice == "7":
                self.sort_books()
            elif choice == "8":
                average_ratings = self.get_average_ratings()
                for title, rating in average_ratings.items():
                    print(f"Title: {title}, Average Rating: {rating}")
            elif choice == "9":
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
        self.list_books()
        book_title = input("Enter the title of the book to borrow: ").strip()

        book_found = False
        book_borrowed = False

        try:
            with open("books.txt", "r") as books_file:
                books = books_file.readlines()

            with open("transactions.txt", "r") as transactions_file:
                borrowed_books = {}
                for transaction in transactions_file:
                    transaction = transaction.strip()
                    if transaction:
                        try:
                            borrowed_book_title, borrower = transaction.split(',')
                            borrowed_books[borrowed_book_title.lower()] = borrower.strip()
                        except ValueError:
                            continue

            updated_books = []

            for book in books:
                book_info = book.strip().split(', ')
                if len(book_info) < 5:
                    continue

                title, author, release_year, pages, library_name = book_info[:5]

                if title.strip().lower() == book_title.lower() and library_name.strip().lower() == self.library_name.lower():
                    book_found = True

                    if title.lower() in borrowed_books:
                        if borrowed_books[title.lower()] == self.logged_in_user:
                            print(f"You have already borrowed '{title}'.")
                            return
                        else:
                            print(f"Book '{title}' is already borrowed by {borrowed_books[title.lower()]}.")
                            return

                    print(f"Book '{title}' borrowed successfully.")
                    borrowed_books[title.lower()] = self.logged_in_user
                    book_borrowed = True

                updated_books.append(', '.join([title, author, release_year, pages, library_name]))

            if not book_found:
                print(f"Book '{book_title}' not found in your library.")
                return

            if book_borrowed:
                with open("books.txt", "w") as books_file:
                    books_file.write('\n'.join(updated_books) + '\n')

                with open("transactions.txt", "a") as transactions_file:
                    transactions_file.write(f"{book_title}, {self.logged_in_user}\n")

        except FileNotFoundError:
            print("Error: One of the files (books.txt or transactions.txt) was not found.")
        except Exception as e:
            print(f"An error occurred while borrowing the book: {e}")

    def return_book(self):
        print("*** BORROWED BOOKS ***")

        user_books = []

        try:
            with open("transactions.txt", "r") as transactions_file:
                for transaction in transactions_file:
                    transaction = transaction.strip()
                    if transaction:
                        try:
                            book_title, borrower = transaction.split(',')
                            if borrower.strip() == self.logged_in_user:
                                user_books.append(book_title.strip())
                                print(f"- {book_title.strip()}")
                        except ValueError:
                            continue

            if not user_books:
                print("You haven't borrowed any books.")
                return

            book_title = input("Enter the title of the book to return: ").strip()

            if book_title.lower() not in [b.lower() for b in user_books]:
                print(f"Book '{book_title}' is not currently borrowed by you.")
                return

            with open("transactions.txt", "r") as transactions_file:
                transactions = transactions_file.readlines()

            with open("transactions.txt", "w") as transactions_file:
                for transaction in transactions:
                    transaction = transaction.strip()
                    if transaction:
                        try:
                            current_title, current_borrower = transaction.split(',')
                            if not (book_title.lower() == current_title.lower() and
                                    self.logged_in_user == current_borrower.strip()):
                                transactions_file.write(transaction + '\n')
                        except ValueError:
                            transactions_file.write(transaction + '\n')

            print(f"Book '{book_title}' returned successfully.")

        except FileNotFoundError:
            print("Error: transactions.txt file not found.")
        except Exception as e:
            print(f"An error occurred while returning the book: {e}")

    def list_borrowed_books(self):
        try:
            self.transactions_file.seek(0)
            transactions = self.transactions_file.readlines()

            print("*** BORROWED BOOKS ***")
            for transaction in transactions:

                transaction = transaction.strip()
                if not transaction:
                    continue

                try:
                    title, user = transaction.split(',')
                    print(f"{title} - Borrowed by {user}")
                except ValueError as e:
                    print(f"Skipping line due to format issue: {transaction} ({e})")

        except Exception as e:
            print(f"Error reading transactions: {e}")

    def get_borrowed_books(self):
        borrowed_books = []
        self.transactions_file.seek(0)

        for transaction in self.transactions_file:
            transaction = transaction.strip()
            if transaction:
                try:
                    title, borrower = transaction.split(',')
                    if borrower.strip() == self.logged_in_user:
                        borrowed_books.append(title.strip())
                except ValueError:
                    continue

        return borrowed_books

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
        print(f"Checking if '{city_name}' exists...")
        return city_name.lower() in cities

if __name__ == "__main__":
    library = Library()
    try:
        library.run()
    except KeyboardInterrupt:
        print("\nExiting the program...")



