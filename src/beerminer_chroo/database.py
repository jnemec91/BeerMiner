import sqlite3

class Database:
    def __init__(self, db):
        self.name = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS beer (id INTEGER PRIMARY KEY, name TEXT, style TEXT, abv TEXT, epm TEXT, ibu TEXT, brewery TEXT, location TEXT, description TEXT, url TEXT, image_url TEXT, rating TEXT)")
        self.conn.commit()
    
    def __str__(self) -> str:
        return self.name
    
    def __del__(self):
        self.conn.close()

    def fetch(self) -> list:
        self.cur.execute("SELECT * FROM beer")
        rows = self.cur.fetchall()
        return rows

    def find_fuzzy(self, beer) -> list:
        self.cur.execute("SELECT * FROM beer WHERE name LIKE ?", (f'%{beer.name}%',))
        rows = self.cur.fetchall()
        return rows
    
    def find_exact(self, beer) -> list:
        self.cur.execute("SELECT * FROM beer WHERE name=?", (beer.name,))
        rows = self.cur.fetchall()
        return rows

    def insert(self, beer) -> bool:
        self.cur.execute("INSERT INTO beer VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
                         (beer.name, beer.style, beer.abv, beer.epm, beer.ibu, beer.brewery, beer.location, beer.description, beer.url, beer.image_url, beer.rating))
        
        self.conn.commit()
        return True

    def remove(self, id) -> bool:
        self.cur.execute("DELETE FROM beer WHERE id=?", (id,))
        self.conn.commit()
        return True
    
    def update(self, id, beer) -> bool:
        self.cur.execute("UPDATE beer SET name=?, style=?, abv=?, epm=?, ibu=?, brewery=?, location=?, description=?, url=?, image_url=?, rating=? WHERE id=?",
                         (beer.name, beer.style, beer.abv, beer.epm, beer.ibu, beer.brewery, beer.location, beer.description, beer.url, beer.image_url, beer.rating, id))
        
        self.conn.commit()
        return True


