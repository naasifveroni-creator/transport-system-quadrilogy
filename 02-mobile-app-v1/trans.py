import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import json
import os
import datetime

kivy.require('2.3.0')

# NEW FEATURE: Predefined time slots for bookings
TIME_SLOTS = [
    "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
]

# NEW FEATURE: The ShuttleLogicController now handles all data management
# and has an `admin` user with an `is_admin` flag.
class ShuttleLogicController:
    def __init__(self, data_file='tfa_shuttles_data.json'):
        self.data_file = data_file
        self.users = {}
        self.shuttles = {}
        self.bookings = []
        self.logged_in_user = None
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.users = data.get('users', {})
                self.shuttles = data.get('shuttles', {})
                self.bookings = data.get('bookings', [])
            print("Data loaded successfully.")
        else:
            print("Data file not found. Initializing with default data.")
            # NEW FEATURE: Default users for a fresh install
            self.users = {
                "testuser": {"password": "testpass", "is_admin": False},
                "admin": {"password": "adminpass", "is_admin": True}
            }
            self.shuttles = {
                "Shuttle A": {"capacity": 10},
                "Shuttle B": {"capacity": 15},
            }
            self.bookings = []
            self.save_data()

    def save_data(self):
        data = {
            'users': self.users,
            'shuttles': self.shuttles,
            'bookings': self.bookings
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")

    def login(self, username, password):
        user_data = self.users.get(username)
        if user_data and user_data['password'] == password:
            self.logged_in_user = username
            return True
        return False

    def is_admin(self):
        if not self.logged_in_user:
            return False
        user_data = self.users.get(self.logged_in_user)
        return user_data.get('is_admin', False)
    
    def get_all_bookings(self):
        return self.bookings
    
    def get_user_bookings(self, username):
        return [b for b in self.bookings if b['username'] == username]

class TFAShuttlesApp(App):
    def build(self):
        self.logic = ShuttleLogicController()
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(BookingsScreen(name='bookings'))
        self.sm.add_widget(AdminDashboardScreen(name='admin_dashboard'))
        self.sm.add_widget(UserBookingsScreen(name='user_bookings'))
        return self.sm

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = FloatLayout()

        grid = GridLayout(cols=2, size_hint=(0.8, 0.4), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        grid.add_widget(Label(text="Username"))
        self.username = TextInput(multiline=False)
        grid.add_widget(self.username)

        grid.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        grid.add_widget(self.password)

        self.login_button = Button(text="Login", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.login_button.bind(on_press=self.do_login)

        self.register_button = Button(text="Register", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.25})
        self.register_button.bind(on_press=self.do_register)

        layout.add_widget(grid)
        layout.add_widget(self.login_button)
        layout.add_widget(self.register_button)

        self.add_widget(layout)

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_layout.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint=(1, 0.2))
        popup_layout.add_widget(close_button)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.3), auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def do_login(self, instance):
        if App.get_running_app().logic.login(self.username.text, self.password.text):
            self.manager.current = 'main_menu'
        else:
            self.show_popup("Login Status", "Invalid username or password.")
            
    def do_register(self, instance):
        username = self.username.text
        password = self.password.text
        if not username or not password:
            self.show_popup("Registration", "Username and password cannot be empty.")
            return

        if username in App.get_running_app().logic.users:
            self.show_popup("Registration", "Username already exists.")
            return

        App.get_running_app().logic.users[username] = {"password": password, "is_admin": False}
        App.get_running_app().logic.save_data()
        self.show_popup("Registration", "User registered successfully! You can now log in.")

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = GridLayout(cols=1, padding=10, spacing=10)
        self.add_widget(layout)

        self.welcome_label = Label(text="Welcome to TFA Shuttles!")
        self.layout.add_widget(self.welcome_label)

        self.book_button = Button(text="Book a Shuttle")
        self.book_button.bind(on_press=self.go_to_bookings)
        self.layout.add_widget(self.book_button)

        self.view_bookings_button = Button(text="My Bookings")
        self.view_bookings_button.bind(on_press=self.go_to_user_bookings)
        self.layout.add_widget(self.view_bookings_button)
        
        self.admin_button = Button(text="Admin Dashboard")
        self.admin_button.bind(on_press=self.go_to_admin)
        
        self.logout_button = Button(text="Logout")
        self.logout_button.bind(on_press=self.do_logout)
        self.layout.add_widget(self.logout_button)

    def on_enter(self):
        logged_in_user = App.get_running_app().logic.logged_in_user
        self.welcome_label.text = f"Welcome, {logged_in_user}!"
        
        # Check if the user is an admin and add the button if so
        if App.get_running_app().logic.is_admin() and self.admin_button not in self.layout.children:
            self.layout.add_widget(self.admin_button)
        elif not App.get_running_app().logic.is_admin() and self.admin_button in self.layout.children:
            self.layout.remove_widget(self.admin_button)
        
        # Ensure logout is always the last button
        if self.logout_button not in self.layout.children:
            self.layout.add_widget(self.logout_button)
            
    def go_to_bookings(self, instance):
        self.manager.current = 'bookings'

    def go_to_admin(self, instance):
        self.manager.current = 'admin_dashboard'

    def go_to_user_bookings(self, instance):
        self.manager.current = 'user_bookings'

    def do_logout(self, instance):
        App.get_running_app().logic.logged_in_user = None
        self.manager.current = 'login'

class BookingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = GridLayout(cols=1, padding=10, spacing=10)
        self.add_widget(self.layout)
        
        self.layout.add_widget(Label(text="Book a Shuttle", font_size='20sp'))
        
        form_layout = GridLayout(cols=2, padding=10, spacing=10)

        form_layout.add_widget(Label(text="Date"))
        self.date_input = TextInput(multiline=False, hint_text="YYYY-MM-DD")
        form_layout.add_widget(self.date_input)

        form_layout.add_widget(Label(text="Time Slot"))
        self.time_input = TextInput(multiline=False, hint_text="e.g., 6:00 AM")
        form_layout.add_widget(self.time_input)

        form_layout.add_widget(Label(text="From"))
        self.from_input = TextInput(multiline=False)
        form_layout.add_widget(self.from_input)

        form_layout.add_widget(Label(text="To"))
        self.to_input = TextInput(multiline=False)
        form_layout.add_widget(self.to_input)

        form_layout.add_widget(Label(text="Shuttle"))
        self.shuttle_input = TextInput(multiline=False)
        form_layout.add_widget(self.shuttle_input)
        
        self.layout.add_widget(form_layout)
        
        self.book_button = Button(text="Confirm Booking")
        self.book_button.bind(on_press=self.confirm_booking)
        self.layout.add_widget(self.book_button)

        self.back_button = Button(text="Back to Main Menu")
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

    def on_enter(self):
        self.date_input.text = ""
        self.time_input.text = ""
        self.from_input.text = ""
        self.to_input.text = ""
        self.shuttle_input.text = ""
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_layout.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint=(1, 0.2))
        popup_layout.add_widget(close_button)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.3), auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def confirm_booking(self, instance):
        username = App.get_running_app().logic.logged_in_user
        date_str = self.date_input.text
        time_slot = self.time_input.text
        from_loc = self.from_input.text
        to_loc = self.to_input.text
        shuttle_id = self.shuttle_input.text

        # Basic validation
        if not all([date_str, time_slot, from_loc, to_loc, shuttle_id]):
            self.show_popup("Booking Error", "All fields are required.")
            return

        try:
            # Check if date is in the future
            booking_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if booking_date < datetime.date.today():
                self.show_popup("Booking Error", "Cannot book for a past date.")
                return
        except ValueError:
            self.show_popup("Booking Error", "Invalid date format. Use YYYY-MM-DD.")
            return
            
        # Check if time slot is valid
        if time_slot not in TIME_SLOTS:
            self.show_popup("Booking Error", f"Invalid time slot. Please choose from: {', '.join(TIME_SLOTS)}.")
            return

        # Check if shuttle exists
        if shuttle_id not in App.get_running_app().logic.shuttles:
            self.show_popup("Booking Error", f"Shuttle '{shuttle_id}' does not exist.")
            return

        # Create a booking entry
        booking = {
            'username': username,
            'date': date_str,
            'time': time_slot,
            'from': from_loc,
            'to': to_loc,
            'shuttle': shuttle_id,
            'status': 'booked'
        }
        
        # Add to the list and save
        App.get_running_app().logic.bookings.append(booking)
        App.get_running_app().logic.save_data()
        
        self.show_popup("Booking Success", "Your shuttle has been booked!")
        self.manager.current = 'main_menu'

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class AdminDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = GridLayout(cols=1, padding=10, spacing=10)
        self.add_widget(self.layout)
        
        self.layout.add_widget(Label(text="Admin Dashboard", font_size='20sp'))
        
        self.booking_list = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        self.booking_list.bind(minimum_height=self.booking_list.setter('height'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.booking_list)
        self.layout.add_widget(scroll_view)
        
        self.back_button = Button(text="Back to Main Menu", size_hint_y=0.1)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)
    
    def on_enter(self):
        self.update_booking_list()
        
    def update_booking_list(self):
        self.booking_list.clear_widgets()
        self.booking_list.add_widget(Label(text="All Bookings", size_hint_y=None, height=40))
        
        bookings = App.get_running_app().logic.get_all_bookings()
        if not bookings:
            self.booking_list.add_widget(Label(text="No bookings found.", size_hint_y=None, height=40))
            return
            
        for booking in bookings:
            text = (f"User: {booking['username']} | Date: {booking['date']} | "
                    f"Time: {booking['time']} | From: {booking['from']} | "
                    f"To: {booking['to']} | Shuttle: {booking['shuttle']}")
            self.booking_list.add_widget(Label(text=text, size_hint_y=None, height=40))

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class UserBookingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = GridLayout(cols=1, padding=10, spacing=10)
        self.add_widget(self.layout)
        
        self.layout.add_widget(Label(text="My Bookings", font_size='20sp'))
        
        self.booking_list = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        self.booking_list.bind(minimum_height=self.booking_list.setter('height'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.booking_list)
        self.layout.add_widget(scroll_view)
        
        self.back_button = Button(text="Back to Main Menu", size_hint_y=0.1)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)
    
    def on_enter(self):
        self.update_booking_list()
        
    def update_booking_list(self):
        self.booking_list.clear_widgets()
        self.booking_list.add_widget(Label(text="Your Bookings", size_hint_y=None, height=40))
        
        logged_in_user = App.get_running_app().logic.logged_in_user
        bookings = App.get_running_app().logic.get_user_bookings(logged_in_user)
        
        if not bookings:
            self.booking_list.add_widget(Label(text="No bookings found.", size_hint_y=None, height=40))
            return
            
        for booking in bookings:
            text = (f"Date: {booking['date']} | Time: {booking['time']} | "
                    f"From: {booking['from']} | To: {booking['to']} | "
                    f"Shuttle: {booking['shuttle']}")
            self.booking_list.add_widget(Label(text=text, size_hint_y=None, height=40))

    def go_back(self, instance):
        self.manager.current = 'main_menu'

if __name__ == '__main__':
    TFAShuttlesApp().run()
