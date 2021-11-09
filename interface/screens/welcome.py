from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class WelcomePage(GridLayout):
    def __init__(self, **kwargs):
        super(WelcomePage, self).__init__(**kwargs)
        self.cols = 1

        self.add_widget(Label(text="SAHyATA\n Situation-Aware Hyperactivity and Autism aware Teaching Assistant"))
        self.add_widget(Button(text="Get Started", font_size=40))
