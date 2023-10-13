from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView


class Nwgrid(RecycleView):

    def __init__(self, **kwargs):
        super(Nwgrid, self).__init__(**kwargs)

        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if self.layout_manager is None:
            return

        for child in self.layout_manager.children:
            if child.collide_point(*self.to_widget(*args[1])):
                child.mouse_hover = True
            else:
                child.mouse_hover = False