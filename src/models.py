import json
from .constants import *

class Magnitude:

    def __init__(self, id:str, name:str, unit:str, min = None, max = None, mean = None):
        self.id = id
        self.name = name
        self.unit = unit
        self.max = max
        self.mean = mean
        self.min = min

    def __str__(self):
        base = f"{self.name} ({self.unit}): "
        if self.min is not None:
            base += f"m:{self.min} "
        if self.mean is not None:
            base += f"p:{self.mean} "
        if self.max is not None:
            base += f"M:{self.max}"
        return base
    
    def isemtpy(self):
        return self.mean is None and self.min is None and self.max is None
    
    def update(self, value, type):
        if type == MIN:
            self.min = value
        elif type == MEAN:
            self.mean = value
        else:
            self.max = value
    
class Report:

    def __init__(self, message: str = None):
        self.message = message

        with open('magnitudes.json', encoding='UTF-8') as j:
            magnitudes = json.load(j)

        self.magnitudes = [Magnitude(x["Id"], x["Name"], x["Unit"]) for x in magnitudes]

    def __str__(self):
        data = "\n".join(str(x) for x in self.magnitudes if not x.isemtpy())

        if self.message is not None:
            data = f"{self.message}:\n" + data

        return data
    
    def update_magnitude(self, id, value, type):
        magnitude = [x for x in self.magnitudes if x.id == id]
        if len(magnitude) > 0:
            magnitude[0].update(value, type)

    def isempty(self):
        return not any([not x.isemtpy() for x in self.magnitudes])