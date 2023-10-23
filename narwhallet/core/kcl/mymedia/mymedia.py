from typing import Dict, List
from narwhallet.core.kcl.file_utils.io import MyMediaLoader
from narwhallet.core.kcl.mymedia.media import MMedia


class MMyMedia():
    def __init__(self):
        self.root_path: str = ''
        self._mymedia: Dict[str, MMedia] = {}

    @property
    def mymedia(self) -> Dict[str, MMedia]:
        return self._mymedia

    @property
    def count(self) -> int:
        return len(self.mymedia)

    def get_media_by_value(self, name: str) -> MMedia:
        return self._mymedia[name]

    def is_media_by_value(self, name: str) -> bool:
        if name in self._mymedia:
            return True
        return False

    def remove_media(self, name: str) -> bool:
        if name in self.mymedia:
            del self._mymedia[name]
            _return = True
        else:
            _return = False
        return _return

    def from_json(self, media: dict):
        _media = MMedia()

        _media.set_name(media['name'])
        _media.set_cid(media['cid'])
        _media.set_pin_date(media['pin_date'])
        _media.set_pin_status(media['pin_status'])

        self._mymedia[_media.name] = _media

    def to_list(self) -> list:
        _l = []
        for i in self.mymedia:
            _l.append(self.mymedia[i].to_list())
        return _l

    def to_dict_list(self) -> List[dict]:
        _l = []
        for i in self.mymedia:
            _l.append(self.mymedia[i].to_dict())
        return _l

    def save_mymedia(self):
        return MyMediaLoader.save(self.root_path, self.to_dict_list())

    def load_mymedia(self, path: str):
        self.root_path = path
        _data = MyMediaLoader.load(path)

        for _a in _data:
            self.from_json(_a)
