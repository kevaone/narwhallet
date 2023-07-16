from typing import Dict, List
from narwhallet.core.kcl.favorites import MFavorite
from narwhallet.core.kcl.file_utils.io import FavoritesLoader


class MFavorites():
    def __init__(self):
        self.root_path: str = ''
        self._favorites: Dict[str, MFavorite] = {}

    @property
    def favorites(self) -> Dict[str, MFavorite]:
        return self._favorites

    @property
    def count(self) -> int:
        return len(self.favorites)

    def get_favorite_by_value(self, value: str) -> MFavorite:
        return self._favorites[value]

    def is_favorite_by_value(self, value: str) -> bool:
        if value in self._favorites:
            return True
        return False

    def remove_favorite(self, value: str) -> bool:
        if value in self.favorites:
            del self._favorites[value]
            _return = True
        else:
            _return = False
        return _return

    def from_json(self, favorite: dict):
        _favorite = MFavorite()

        _favorite.set_coin(favorite['coin'])
        _favorite.set_kind(favorite['kind'])
        _favorite.set_value(favorite['value'])
        _favorite.set_filter(favorite['filter'])
        

        self._favorites[_favorite.value] = _favorite

    def to_list(self) -> list:
        _l = []
        for i in self.favorites:
            _l.append(self.favorites[i].to_list())
        return _l

    def to_dict_list(self) -> List[dict]:
        _l = []
        for i in self.favorites:
            _l.append(self.favorites[i].to_dict())
        return _l

    def save_favorites(self):
        return FavoritesLoader.save(self.root_path, self.to_dict_list())

    def load_favorites(self, path: str):
        self.root_path = path
        _data = FavoritesLoader.load(path)

        for _a in _data:
            self.from_json(_a)
