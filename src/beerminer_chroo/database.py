import sqlite3
from .beer import Beer, beer_from_list

class Database:
    def __init__(self, db: str) -> None:
        self.name = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS beer (id INTEGER PRIMARY KEY, name TEXT, style TEXT, abv TEXT, epm TEXT, ibu TEXT, brewery TEXT, location TEXT, description TEXT, url TEXT, image_url TEXT, rating TEXT)")
        self.conn.commit()
    
    def __str__(self) -> str:
        return self.name
    
    def __del__(self) -> None:
        self.conn.close()

    def fetch(self) -> list:
        self.cur.execute("SELECT * FROM beer")
        rows = self.cur.fetchall()
        
        for c,row in enumerate(rows):
            rows[c] = beer_from_list(row)

        return rows

    def find_fuzzy(self, beer: Beer) -> list:
        self.cur.execute("SELECT * FROM beer WHERE name LIKE ?", (f'%{beer.name}%',))
        rows = self.cur.fetchall()

        for c,row in enumerate(rows):
            rows[c] = beer_from_list(row)

        return rows
    
    def find_exact(self, beer: Beer) -> list:
        self.cur.execute("SELECT * FROM beer WHERE name=?", (beer.name,))
        rows = self.cur.fetchall()

        for c,row in enumerate(rows):
            rows[c] = beer_from_list(row)

        return rows

    def insert(self, beer: Beer) -> bool:
        self.cur.execute("INSERT INTO beer VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
                         (beer.name, beer.style, beer.abv, beer.epm, beer.ibu, beer.brewery, beer.location, beer.description, beer.url, beer.image_url, beer.rating))
        
        self.conn.commit()
        return True

    def remove(self, id: int) -> bool:
        self.cur.execute("DELETE FROM beer WHERE id=?", (id,))
        self.conn.commit()
        return True
    
    def update(self, id: int, beer: str) -> bool:
        self.cur.execute("UPDATE beer SET name=?, style=?, abv=?, epm=?, ibu=?, brewery=?, location=?, description=?, url=?, image_url=?, rating=? WHERE id=?",
                         (beer.name, beer.style, beer.abv, beer.epm, beer.ibu, beer.brewery, beer.location, beer.description, beer.url, beer.image_url, beer.rating, id))
        
        self.conn.commit()
        return True


