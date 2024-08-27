class Beer():
    def __init__(self, name) -> None:
        self.name = name
        self.style = None
        self.abv = None
        self.epm = None
        self.ibu = None
        self.brewery = None
        self.location = None
        self.description = None
        self.url = None
        self.image_url = None
        self.rating = None


    def __str__(self) -> str:
        return f"{self.name}: ({self.style}), ABV: {self.abv}, IBU: {self.ibu}"
    
    def set(self, key, value) -> object:
        setattr(self, key, value)
        return self
    
    def get(self, key) -> str:
        if hasattr(self, key):
            return str(getattr(self, key)) if getattr(self, key) else "N/A"
        return "N/A"
    