import os
import shutil
from kivy.utils import platform
from narwhallet.core.kcl.file_utils.io import ConfigLoader
# import locale
# loc = locale.getlocale()
# print('l', locale.getdefaultlocale())


if platform != 'android':
    _user_home = os.path.expanduser('~')
else:
    _user_home = '/data/user/0/one.keva.narwhallet/files/'

_narwhallet_path = os.path.join(_user_home, '.narwhallet')

if os.path.isfile(os.path.join(_narwhallet_path,
                                    'translations.json')) is False:
        print('translations.json created.')
        shutil.copy(os.path.join(os.path.dirname(__file__), '../../../config/translations.json'), _narwhallet_path)
        
_dat = ConfigLoader(os.path.join(_narwhallet_path, 'translations.json'))
_dat.load()

def translate(text):
    _lang = _dat.data['available'][_dat.data['active']][1]

    try:
        _t = _dat.data['strings'][text][_lang]
    except:
        _t = text
    
    return _t
