from kivy.properties import DictProperty, StringProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
import requests


class Main(Screen):
    data = DictProperty()
    text = StringProperty("Select a category")
    generated_text = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.data = {
            "": [
                "bullseye",
                "on_press", lambda x: self.change_text_and_card_widgets("Advices")
            ],
            " ": [
                "emoticon-outline",
                "on_press", lambda x: self.change_text_and_card_widgets("Jokes")
            ],
        }

    def change_text_and_card_widgets(self, new):
        self.text = new
        card = self.manager.get_screen("Main").ids['card']
        layout = card.children[0]
        if len(layout.children) < 2:
            self.generated_label = MDLabel(text=self.generated_text, font_style="H6", halign="center",
                                           theme_text_color="Custom", text_color="white", pos=("0dp", "-10dp"),
                                           padding=(10, 0))
            button = MDIconButton(icon="refresh", icon_size="64sp", pos_hint={"center_x": .5, "center_y": 0.08},
                                  id="refresh", theme_icon_color="Custom", icon_color="white",
                                  on_press=lambda x: self.generate())
            layout.add_widget(self.generated_label)
            layout.add_widget(button)
            informative_label = layout.children[2]
            informative_label.selected = True
        self.generated_label.text = ""

    def generate(self):
        category = self.text
        if category == "Advices":
            self.response = requests.get("https://api.adviceslip.com/advice").json()
            self.generated_label.text = self.response["slip"]["advice"]
        elif category == "Jokes":
            self.response = requests.get("https://v2.jokeapi.dev/joke/Any").json()
            if self.response["type"] == "single":
                self.generated_label.text = self.response["joke"]
            else:
                self.generated_label.text = self.response["setup"] + "\n" + self.response["delivery"]


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.kv = Builder.load_file("my.kv")
        self.manager = ScreenManager()
        self.manager.add_widget(Main(name="Main"))
        return self.manager

    def change_theme(self):
        self.theme_cls.primary_palette = (
            "Blue" if self.theme_cls.primary_palette == "Indigo" else "Indigo"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )


if __name__ == "__main__":
    MyApp().run()
