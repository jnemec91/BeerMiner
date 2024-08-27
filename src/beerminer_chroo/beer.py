class Beer():
    def __init__(self, name,style=None, abv=None, epm=None,
                 ibu=None, brewery=None, location=None, description=None,
                 url=None, image_url=None, rating=None) -> None:
        self.name = name
        self.style = style
        self.abv = abv
        self.epm = epm
        self.ibu = ibu
        self.brewery = brewery
        self.location = location
        self.description = description
        self.url = url
        self.image_url = image_url
        self.rating = rating
        

    def __str__(self) -> str:
        return f"{self.name}: ({self.style}), ABV: {self.abv}, IBU: {self.ibu}"
    
    def set(self, key, value) -> object:
        setattr(self, key, value)
        return self
    
    def get(self, key) -> str:
        if hasattr(self, key):
            return str(getattr(self, key)) if getattr(self, key) else "N/A"
        return "N/A"


def beer_from_list(data: list) -> Beer:
    return Beer(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11])