from kivy.app import App

from interface.screens.welcome import WelcomePage

class SAHyATAApp(App):
    def build(self):
        return WelcomePage()


if __name__ == "__main__":
    SAHyATAApp().run()