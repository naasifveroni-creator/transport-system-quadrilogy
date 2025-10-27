import datetime

class User:
    """Represents a user of the transport booking platform."""
    def __init__(self, username, password, full_name, home_address, work_address):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.home_address = home_address
        self.work_address = work_address
        self.booking_history = []

class Booking:
    """Represents a single transport booking."""
    def __init__(self, user, start_location, end_location, booking_time):
        self.user = user
        self.start_location = start_location
        self.end_location = end_location
        self.booking_time = booking_time
        self.status = "Confirmed"

    def __str__(self):
        return (f"Booking Details:\n"
                f"  User: {self.user.full_name}\n"
                f"  From: {self.start_location}\n"
                f"  To: {self.end_location}\n"
                f"  Time: {self.booking_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"  Status: {self.status}")

class TransportApp:
    """The main application class to handle user interactions and logic."""
    def __init__(self):
        self.users = {}  # In-memory database to store User objects
        self.current_user = None

    def register(self):
        """Allows a new user to register."""
        print("\n--- User Registration ---")
        username = input("Enter a new username: ")
        if username in self.users:
            print("Username already exists. Please try again.")
            return

        password = input("Create a password: ")
        full_name = input("Enter your full name: ")
        home_address = input("Enter your home address: ")
        work_address = input("Enter your work address: ")

        new_user = User(username, password, full_name, home_address, work_address)
        self.users[username] = new_user
        print("Registration successful! You can now log in.")

    def login(self):
        """Allows an existing user to log in."""
        print("\n--- User Login ---")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print(f"Welcome back, {self.current_user.full_name}!")
            self.main_menu()
        else:
            print("Invalid username or password. Please try again.")

    def book_a_ride(self, start_loc=None, end_loc=None):
        """Handles the general booking process."""
        print("\n--- Book a New Ride ---")
        if start_loc is None:
            start_loc = input("Enter your starting location: ")
        if end_loc is None:
            end_loc = input("Enter your destination: ")

        now = datetime.datetime.now()
        new_booking = Booking(self.current_user, start_loc, end_loc, now)
        self.current_user.booking_history.append(new_booking)

        print("\nBooking successful!")
        print(new_booking)

    def book_home_to_work(self):
        """Books a ride from the user's home to work."""
        print("\n--- Book a Ride: Home to Work ---")
        start_loc = self.current_user.home_address
        end_loc = self.current_user.work_address
        self.book_a_ride(start_loc, end_loc)

    def book_work_to_home(self):
        """Books a ride from the user's work to home."""
        print("\n--- Book a Ride: Work to Home ---")
        start_loc = self.current_user.work_address
        end_loc = self.current_user.home_address
        self.book_a_ride(start_loc, end_loc)

    def view_booking_history(self):
        """Displays the user's past bookings."""
        print("\n--- My Booking History ---")
        if not self.current_user.booking_history:
            print("You have no past bookings.")
            return

        for i, booking in enumerate(self.current_user.booking_history, 1):
            print(f"\n--- Booking #{i} ---")
            print(booking)

    def logout(self):
        """Logs the current user out."""
        print(f"Goodbye, {self.current_user.full_name}!")
        self.current_user = None

    def main_menu(self):
        """Displays the main menu for a logged-in user."""
        while self.current_user:
            print("\n--- Main Menu ---")
            print("1. Book a ride from A to B")
            print("2. Book Home to Work")
            print("3. Book Work to Home")
            print("4. View My Booking History")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.book_a_ride()
            elif choice == '2':
                self.book_home_to_work()
            elif choice == '3':
                self.book_work_to_home()
            elif choice == '4':
                self.view_booking_history()
            elif choice == '5':
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        """The main entry point of the application."""
        while True:
            print("\n--- Welcome to the Transport Booking Platform ---")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("Thank you for using our service. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TransportApp()
    app.run()
