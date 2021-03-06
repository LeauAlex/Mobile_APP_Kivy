from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

Builder.load_file("design.kv") # this is how we do the bond between py and .kv

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def login(self, name, pword):
        with open("users.json") as file:
            users = json.load(file)
        if name in users and users[name]['password'] == pword:
            self.manager.current = "login_screen_success"
        elif name == "" or pword == "":
            self.ids.login_wrong.text = "Hai bosule, lasa vrajeala, nimic ai tu in buzunare!"
        else:
            self.ids. \
                login_wrong.text = "Maai baga o fisa bosule, ca la pacanele ;)"



class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


class SignUpScreen(Screen):
    def add_user(self, name, pword):
        with open("users.json") as file:
            users = json.load(file)
        users[name] = {
                       'username': name,
                       'password': pword,
                       'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                       }
        with open ("users.json", "w") as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"
    def to_login(self):
        self.manager.current = "login_screen"

class SignUpScreenSuccess(Screen):
    def to_login(self):
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    def get_quote(self, feel):
        feel = feel.lower()
        availabel_feeling = glob.glob("qutoes/*txt")
        availabel_feeling = [Path(filename).stem for filename in availabel_feeling]
        if feel in availabel_feeling:
            with open(f"qutoes/{feel}.txt", "r", encoding="utf-8") as file:
                qutes = file.readlines()
            self.ids.quote.text = random.choice(qutes)

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

if __name__ == "__main__":
    MainApp().run()