from kivy.properties import DictProperty, StringProperty, ObjectProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDIconButton
import requests
from kivymd.uix.label import MDLabel
from kivy.core.window import Window


class Main(Screen):
    pass


class MyApp(MDApp):
    data = DictProperty()
    text = ObjectProperty("Select a category")
    generated_text = StringProperty()

    def build(self):
        Window.size = (486, 860)
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.kv = Builder.load_file("my.kv")
        self.manager = ScreenManager()
        self.manager.add_widget(Main(name="Main"))
        self.data = {
            'Advices': [
                'bullseye',
                "on_press", lambda x: self.change_text_and_card_widgets("Advices")
            ],
            'Jokes': [
                'emoticon-outline',
                "on_press", lambda x: self.change_text_and_card_widgets("Jokes")
            ],
        }
        return self.manager

    def change_text_and_card_widgets(self, new):
        self.text = new
        widget = self.manager.get_screen("Main").ids.card
        if len(widget.children) < 2:
            self.generated_label = MDLabel(text=self.generated_text, font_style="H5", halign="center", valign="center",
                                           theme_text_color="Custom", text_color="white", padding=("10dp", "20dp"))
            button = MDIconButton(icon="refresh", icon_size="64sp", pos_hint={"center_x": .5, "center_y": .5},
                                  id="refresh", theme_icon_color="Custom", icon_color="white",
                                  on_press=lambda x: self.generate())
            widget.add_widget(self.generated_label)
            widget.add_widget(button)

    def change_theme(self):
        self.theme_cls.primary_palette = (
            "Blue" if self.theme_cls.primary_palette == "Indigo" else "Indigo"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

    def generate(self):
        state = self.text
        if state == "Advices":
            print("Advices")
        elif state == "Jokes":
            self.response = requests.get("https://v2.jokeapi.dev/joke/Any").json()
            if self.response["type"] == "single":
                print("single")
            else:
                self.generated_label.text = self.response["setup"] + "\n" + self.response["delivery"]


if __name__ == "__main__":
    MyApp().run()
