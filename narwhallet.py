from kivy.app import App
from kivy.config import Config
from narwhallet.core.kui.interface.screenmanager import NarwhalletScreens
# Config.set('graphics', 'width', '500')
# Config.set('graphics', 'height', '700')

class NarwhalletApp(App):
    def build(self):
        self.sm = NarwhalletScreens()
        self.sm.setup()
        
        return self.sm

if __name__ == '__main__':
    NarwhalletApp().run()