import qrcode
from kivy.graphics.texture import Texture
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             StringProperty, ObjectProperty)
from kivy.uix.floatlayout import FloatLayout


class QR_Code(FloatLayout):
    show_border = BooleanProperty(True)
    data = StringProperty(None, allow_none=True)
    error_correction = NumericProperty(qrcode.constants.ERROR_CORRECT_L)
    background_color = ListProperty((1, 1, 1, 1))
    qrimage = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(QR_Code, self).__init__(**kwargs)
        self.addr = None
        self.qr: qrcode.QRCode = None
        self._qrtexture = None

    def on_data(self, instance, value):
        self.generate_qr(value)

    def on_error_correction(self, instance, value):
        self.generate_qr(value)

    def generate_qr(self, value):
        self.addr = value
        self.qr = None
        QRCode = qrcode.QRCode

        try:
            _qr = QRCode(
                version=None,
                error_correction=self.error_correction,
                box_size=10,
                border=0,
            )
            _qr.add_data(self.addr)
            _qr.make(fit=True)
            self.qr = _qr
        except Exception as e:
            self.qr = None

        if self.qr is None:
            return
        matrix = self.qr.get_matrix()
        k = len(matrix)

        # create the texture in main UI thread otherwise
        # this will lead to memory corruption
        # Clock.schedule_once(partial(self._create_texture, k), -1)
        self._qrtexture = Texture.create(size=(k, k), colorfmt='rgb')
        # don't interpolate texture
        self._qrtexture.min_filter = 'nearest'
        self._qrtexture.mag_filter = 'nearest'

        cr, cg, cb, ca = self.background_color[:]
        cr, cg, cb = int(cr*255), int(cg*255), int(cb*255)

        buff = bytearray()
        for r in range(k):
            for c in range(k):
                buff.extend([0, 0, 0] if matrix[r][c] else [cr, cg, cb])

        self._qrtexture.blit_buffer(buff, colorfmt='rgb', bufferfmt='ubyte')
        self._qrtexture.flip_vertical()
        self.qrimage.texture = self._qrtexture
