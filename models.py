import json

class Magnitude:

    def __init__(self, id:str, name:str, unit:str, value = None):
        self.id = id
        self.name = name
        self.unit = unit
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit}"
    
class Report:

    def __init__(self, type: str):
        self.type = type

        with open('magnitudes.json', encoding='UTF-8') as j:
            magnitudes = json.load(j)

        self.magnitudes = [Magnitude(x["Id"], x["Name"], x["Unit"]) for x in magnitudes]

    def __str__(self):
        header = f"{self.type}:\n"
        return header + "\n".join(str(x) for x in self.magnitudes if x.value is not None)
    
    def update_magnitude(self, id, value):
        magnitude = [x for x in self.magnitudes if x.id == id]
        if len(magnitude) > 0:
            magnitude[0].value = value