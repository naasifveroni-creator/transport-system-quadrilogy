import datetime
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# ----------------------------------------------------------------------
# Core Logic Classes (with JSON serialization)
# ----------------------------------------------------------------------
class User:
    def __init__(self, username, password, full_name, home_address, work_address):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.home_address = home_address
        self.work_address = work_address
        self.booking_history = []

    def to_dict(self):
        """Converts the User object to a dictionary for JSON serialization."""
        return {
            'username': self.username,
            'password': self.password,
            'full_name': self.full_name,
            'home_address': self.home_address,
            'work_address': self.work_address,
            'booking_history': [b.to_dict() for b in self.booking_history]
        }
    
    @staticmethod
    def from_dict(data):
        """Creates a User object from a dictionary."""
        user = User(data['username'], data['password'], data['full_name'], data['home_address'], data['work_address'])
        user.booking_history = [Booking.from_dict(b) for b in data['booking_history']]
        return user

class Booking:
    def __init__(self, user, start_location, end_location, booking_time):
        self.user = user
        self.start_location = start_location
        self.end_location = end_location
        self.booking_time = booking_time
        self.status = "Confirmed"

    def to_dict(self):
        """Converts the Booking object to a dictionary for JSON serialization."""
        return {
            'start_location': self.start_location,
            'end_location': self.end_location,
            'booking_time': self.booking_time.isoformat(),
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data):
        """Creates a Booking object from a dictionary."""
        booking = Booking(None, data['start_location'], data['end_location'], datetime.datetime.fromisoformat(data['booking_time']))
        booking.status = data['status']
        return booking

# ----------------------------------------------------------------------
# Application Logic Controller (with file I/O)
# ----------------------------------------------------------------------
class TransportLogicController:
    def __init__(self, data_file='user_data.json'):
        self.data_file = data_file
        self.users = {}
        self.current_user = None
        self.load_data()

    def load_data(self):
        """Loads user data from a JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.users = {username: User.from_dict(user_data) for username, user_data in data.items()}
                print("Data loaded successfully.")
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            print("No data file found. Starting with a new database.")
            self.users['testuser'] = User('testuser', 'password', 'Test User', '123 Test St', '456 Work Ave')
            self.save_data() # Save the default user to the new file

    def save_data(self):
        """Saves all user data to a JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                data = {username: user.to_dict() for username, user in self.users.items()}
                json.dump(data, f, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def register(self, username, password, full_name, home_address, work_address):
        if username in self.users:
            return False, "Username already exists."
        
        new_user = User(username, password, full_name, home_address, work_address)
        self.users[username] = new_user
        self.save_data()
        return True, "Registration successful!"

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            return True, f"Welcome, {self.current_user.full_name}!"
        else:
            return False, "Invalid username or password."

    def book_a_ride(self, start_loc, end_loc):
        if not self.current_user:
            return False, "User not logged in."
        
        now = datetime.datetime.now()
        new_booking = Booking(self.current_user, start_loc, end_loc, now)
        self.current_user.booking_history.append(new_booking)
        self.save_data()
        return True, "Booking successful!"

    def logout(self):
        self.current_user = None
        return True, "Logged out successfully."

    def get_booking_history(self):
        return self.current_user.booking_history if self.current_user else []

# ----------------------------------------------------------------------
# Kivy GUI Classes (The "frontend")
# ----------------------------------------------------------------------
class BackgroundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos, source='background.png')
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class LoginScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.height = 300

        title_label = Label(text='TP Transport - Login', font_size=24, color=(0.8, 0.8, 0.8, 1))
        self.username = TextInput(hint_text='Username', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        self.password = TextInput(hint_text='Password', password=True, foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        login_btn = Button(text='Login', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        register_btn = Button(text='Register', background_color=(0.15, 0.15, 0.15, 1), color=(0.7, 0.7, 0.7, 1))

        login_btn.bind(on_press=self.do_login)
        register_btn.bind(on_press=self.go_to_register)

        layout.add_widget(title_label)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        self.add_widget(layout)

    def do_login(self, instance):
        success, message = self.logic.login(self.username.text, self.password.text)
        self.show_popup('Login Status', message)
        if success:
            self.manager.current = 'main_menu'

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(0.8, 0.4), background_color=(0.1, 0.1, 0.1, 0.9))
        popup.title_color = (0.9, 0.9, 0.9, 1)
        popup.content.color = (0.8, 0.8, 0.8, 1)
        for button in popup.content.children:
            if isinstance(button, Button):
                button.background_color = (0.3, 0.3, 0.3, 1)
                button.color = (0.9, 0.9, 0.9, 1)
        popup.open()

class RegisterScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.height = 450

        title_label = Label(text='TP Transport - Register', font_size=24, color=(0.8, 0.8, 0.8, 1))
        self.username = TextInput(hint_text='Username', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        self.password = TextInput(hint_text='Password', password=True, foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        self.full_name = TextInput(hint_text='Full Name', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        self.home_address = TextInput(hint_text='Home Address', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        self.work_address = TextInput(hint_text='Work Address', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))

        register_btn = Button(text='Register', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        back_btn = Button(text='Back to Login', background_color=(0.15, 0.15, 0.15, 1), color=(0.7, 0.7, 0.7, 1))

        register_btn.bind(on_press=self.do_register)
        back_btn.bind(on_press=self.go_to_login)

        layout.add_widget(title_label)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.full_name)
        layout.add_widget(self.home_address)
        layout.add_widget(self.work_address)
        layout.add_widget(register_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def do_register(self, instance):
        success, message = self.logic.register(
            self.username.text, self.password.text, self.full_name.text,
            self.home_address.text, self.work_address.text
        )
        self.show_popup('Registration Status', message)
        if success:
            self.manager.current = 'login'

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(0.8, 0.4), background_color=(0.1, 0.1, 0.1, 0.9))
        popup.title_color = (0.9, 0.9, 0.9, 1)
        popup.content.color = (0.8, 0.8, 0.8, 1)
        for button in popup.content.children:
            if isinstance(button, Button):
                button.background_color = (0.3, 0.3, 0.3, 1)
                button.color = (0.9, 0.9, 0.9, 1)
        popup.open()

class MainMenuScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.height = 350

        title_label = Label(text='TP Transport - Main Menu', font_size=24, color=(0.8, 0.8, 0.8, 1))
        book_ride_btn = Button(text='Book a ride from A to B', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        home_work_btn = Button(text='Book Home to Work', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        work_home_btn = Button(text='Book Work to Home', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        history_btn = Button(text='View My Booking History', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        logout_btn = Button(text='Logout', background_color=(0.15, 0.15, 0.15, 1), color=(0.7, 0.7, 0.7, 1))

        book_ride_btn.bind(on_press=self.go_to_book_ride)
        home_work_btn.bind(on_press=self.book_home_work)
        work_home_btn.bind(on_press=self.book_work_home)
        history_btn.bind(on_press=self.view_history)
        logout_btn.bind(on_press=self.do_logout)

        layout.add_widget(title_label)
        layout.add_widget(book_ride_btn)
        layout.add_widget(home_work_btn)
        layout.add_widget(work_home_btn)
        layout.add_widget(history_btn)
        layout.add_widget(logout_btn)

        self.add_widget(layout)

    def go_to_book_ride(self, instance):
        self.manager.current = 'book_ride'

    def book_home_work(self, instance):
        success, message = self.logic.book_a_ride(self.logic.current_user.home_address, self.logic.current_user.work_address)
        self.show_popup('Booking Status', message)

    def book_work_home(self, instance):
        success, message = self.logic.book_a_ride(self.logic.current_user.work_address, self.logic.current_user.home_address)
        self.show_popup('Booking Status', message)

    def view_history(self, instance):
        self.manager.current = 'history'

    def do_logout(self, instance):
        success, message = self.logic.logout()
        self.show_popup('Logout Status', message)
        self.manager.current = 'login'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(0.8, 0.4), background_color=(0.1, 0.1, 0.1, 0.9))
        popup.title_color = (0.9, 0.9, 0.9, 1)
        popup.content.color = (0.8, 0.8, 0.8, 1)
        for button in popup.content.children:
            if isinstance(button, Button):
                button.background_color = (0.3, 0.3, 0.3, 1)
                button.color = (0.9, 0.9, 0.9, 1)
        popup.open()

class BookRideScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.height = 300

        title_label = Label(text='TP Transport - Book Ride', font_size=24, color=(0.8, 0.8, 0.8, 1))
        self.start_loc = TextInput(hint_text='Start Location', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        self.end_loc = TextInput(hint_text='Destination', foreground_color=(0.8, 0.8, 0.8, 1), background_color=(0.2, 0.2, 0.2, 1))
        book_btn = Button(text='Confirm Booking', background_color=(0.3, 0.3, 0.3, 1), color=(0.9, 0.9, 0.9, 1))
        back_btn = Button(text='Back to Main Menu', background_color=(0.15, 0.15, 0.15, 1), color=(0.7, 0.7, 0.7, 1))

        book_btn.bind(on_press=self.do_booking)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(self.start_loc)
        layout.add_widget(self.end_loc)
        layout.add_widget(book_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def do_booking(self, instance):
        success, message = self.logic.book_a_ride(self.start_loc.text, self.end_loc.text)
        self.show_popup('Booking Status', message)

    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(0.8, 0.4), background_color=(0.1, 0.1, 0.1, 0.9))
        popup.title_color = (0.9, 0.9, 0.9, 1)
        popup.content.color = (0.8, 0.8, 0.8, 1)
        for button in popup.content.children:
            if isinstance(button, Button):
                button.background_color = (0.3, 0.3, 0.3, 1)
                button.color = (0.9, 0.9, 0.9, 1)
        popup.open()

class HistoryScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = App.get_running_app().logic

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title_label = Label(text='TP Transport - Booking History', font_size=24, color=(0.8, 0.8, 0.8, 1))
        scroll_view = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll_view.add_widget(self.history_layout)
        back_btn = Button(text='Back to Main Menu', size_hint_y=None, height=40, background_color=(0.15, 0.15, 0.15, 1), color=(0.7, 0.7, 0.7, 1))
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(scroll_view)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def on_enter(self):
        self.update_history_display()

    def update_history_display(self):
        self.history_layout.clear_widgets()
        bookings = self.logic.get_booking_history()
        if bookings:
            for booking in bookings:
                booking_details = (f"From: {booking.start_location}\n"
                                   f"To: {booking.end_location}\n"
                                   f"Time: {booking.booking_time.strftime('%Y-%m-%d %H:%M')}")
                
                label = Label(text=booking_details, size_hint_y=None, height=80, color=(0.8, 0.8, 0.8, 1), halign='left', valign='middle', padding=(10, 0))
                
                with label.canvas.before:
                    Color(0.2, 0.2, 0.2, 1)
                    self.rect = Rectangle(size=label.size, pos=label.pos)
                
                label.bind(size=lambda instance, value: setattr(self.rect, 'size', value),
                           pos=lambda instance, value: setattr(self.rect, 'pos', value))
                
                self.history_layout.add_widget(label)
        else:
            self.history_layout.add_widget(Label(text="No booking history yet.", color=(0.8, 0.8, 0.8, 1)))

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class MainApp(App):
    title = "TP Transport"

    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        self.logic = TransportLogicController()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(BookRideScreen(name='book_ride'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm

if __name__ == '__main__':
    MainApp().run()
