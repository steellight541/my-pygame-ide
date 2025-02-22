import typing

class StyleSheet:
    background_color: typing.Optional[str]
    color: typing.Optional[str]
    font_size: typing.Optional[int]
    font_family: typing.Optional[str]
    
    def __init__(self, **kwargs):
        if "background_color" in kwargs: self.background_color = kwargs["background_color"]
        if "color" in kwargs: self.color = kwargs["color"]
        if "font_size" in kwargs: self.font_size = kwargs["font_size"]
        if "font_family" in kwargs: self.font_family = kwargs["font_family"]

    def __str__(self):
        return "".join([f"{key.replace('_', '-')}: {value};" for key, value in self.__dict__.items() if value is not None])
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def dark(cls):
        return cls(background_color="black", color="white", font_size=12, font_family="Courier")

    @classmethod
    def light(cls):
        return cls(background_color="white", color="black", font_size=12, font_family="Courier")

    def set_background_color(self, color: str):
        self.background_color = color

    def set_color(self, color: str):
        self.color = color

    def set_font_size(self, size: int):
        self.font_size = size

    def set_font_family(self, family: str):
        self.font_family = family

class CustomStyleSheet(StyleSheet):
    """for the user to customize"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
# get all variables from the file
def get_variables(file_path: str) -> typing.List[str]:
    with open(file_path, 'r') as file:
        return [line.split(" ")[-1].replace(",", "") for line in file.readlines() if line.strip() and not line.strip().startswith("#")]
