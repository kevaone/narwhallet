from narwhallet.core.kcl.file_utils.io import ConfigLoader
# import locale
# loc = locale.getlocale()
# print('l', locale.getdefaultlocale())

_dat = ConfigLoader('narwhallet/core/kui/translations.json')
_dat.load()

def translate(text):
    _lang = _dat.data['available'][_dat.data['active']]

    try:
        _t = _dat.data['strings'][text][_lang]
    except:
        _t = text
    
    return _t
