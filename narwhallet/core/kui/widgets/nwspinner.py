from kivy.app import App
from kivy.clock import Clock
from kivy.compat import string_types
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, NumericProperty
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.spbutton import Spbutton
from kivy.uix.dropdown import DropDown


class Nwspinner(Nwbutton):
    option_cls = ObjectProperty(Spbutton)
    _text = StringProperty('')
    values = ListProperty()
    text_autoupdate = BooleanProperty(False)
    # option_cls = ObjectProperty(SpinnerOption)
    dropdown_cls = ObjectProperty(DropDown)
    is_open = BooleanProperty(False)
    sync_height = BooleanProperty(False)
    _sort = StringProperty('')

    def __init__(self, **kwargs):
        self._dropdown = None
        super(Nwspinner, self).__init__(**kwargs)
        fbind = self.fbind
        build_dropdown = self._build_dropdown
        fbind('on_release', self._toggle_dropdown)
        fbind('dropdown_cls', build_dropdown)
        fbind('option_cls', build_dropdown)
        fbind('values', self._update_dropdown)
        fbind('size', self._update_dropdown_size)
        fbind('text_autoupdate', self._update_dropdown)
        build_dropdown()
        Clock.schedule_once(self._bind)
        self.icon_size = (dp(51), dp(25))
        self.icon_padding = dp(0)
        self.halign = 'center'
        self.valign = 'center'

    def _bind(self, dt):
        app = App.get_running_app()
        app.bind(lang=self.translate_text)
        self.translate_text()

    def translate_text(self, *args):
        app = App.get_running_app()
        self.text = app.translate_text(self._text)

    def on__text(self, *args):
        self.translate_text()

    def _build_dropdown(self, *largs):
        if self._dropdown:
            self._dropdown.unbind(on_select=self._on_dropdown_select)
            self._dropdown.unbind(on_dismiss=self._close_dropdown)
            self._dropdown.dismiss()
            self._dropdown = None
        cls = self.dropdown_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        self._dropdown = cls()
        self._dropdown.bind(on_select=self._on_dropdown_select)
        self._dropdown.bind(on_dismiss=self._close_dropdown)
        self._update_dropdown()

    def _update_dropdown_size(self, *largs):
        if not self.sync_height:
            return
        dp = self._dropdown
        if not dp:
            return

        container = dp.container
        if not container:
            return
        h = self.height
        for item in container.children[:]:
            item.height = h

    def _update_dropdown(self, *largs):
        dp = self._dropdown
        cls = self.option_cls
        values = self.values
        text_autoupdate = self.text_autoupdate
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        dp.clear_widgets()
        for _value, _icon in values:
            item = cls(_sort=_value,icon=_icon)
            item.height = self.height if self.sync_height else item.height
            item.bind(on_release=lambda option: dp.select((option._sort, option.icon)))
            dp.add_widget(item)
        if text_autoupdate:
            if values:
                if not self._text or self._text not in values:
                    self._text = values[0]
            else:
                self._text = ''

    def _toggle_dropdown(self, *largs):
        if self.values:
            self.is_open = not self.is_open

    def _close_dropdown(self, *largs):
        self.is_open = False

    def _on_dropdown_select(self, instance, data, *largs):
        self.icon = data[1]
        self._sort = data[0]
        # for _value, _icon in self.values:
        #     if _value == data:
        #         self.icon = _icon
        self.is_open = False

    def on_is_open(self, instance, value):
        if value:
            self._dropdown.open(self)
        else:
            if self._dropdown.attach_to:
                self._dropdown.dismiss()
