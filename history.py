import pathlib
import yaml


class History:
    SIZE = 200

    def __init__(self, path):
        self._path = path
        self._history_file = pathlib.Path(path)
        if not self._history_file.is_file():
            self._history_file.touch()
            self._data = {'readings': []}
        else:
            self._data = yaml.safe_load(open(self._history_file))

    def add_reading(self, value):
        self._data['readings'].insert(0, value)
        self._data['readings'] = self._data['readings'][:self.SIZE]
        with open(self._history_file, "w") as file:
            file.write(yaml.dump(self._data))

    def get_readings(self):
        return self._data['readings']
