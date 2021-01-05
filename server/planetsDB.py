import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class planetsDB:

    #TODO:
    #return a list of ditionaries, rather than a list of tuples
    #   why?

    def __init__(self):
        #initialize the class instance
        self.connection = sqlite3.connect("planets.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    #Insert
    def insertPlanet(self, name, shape, color, rings):
        data = [name, shape, color, rings]
        self.cursor.execute("INSERT INTO planets (name, shape, color, rings) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    #Read
    def getAllPlanets(self):
        #read from database
        self.cursor.execute("SELECT * FROM planets")
        planets = self.cursor.fetchall()
        return planets

    def getOnePlanet(self, memberID):
        data = [memberID]
        self.cursor.execute("SELECT * FROM planets WHERE id = ?", data)
        planet = self.cursor.fetchone()
        return planet

    def deletePlanet(self, memberID):
        data = [memberID]
        self.cursor.execute("DELETE FROM planets WHERE id = ?", data)
        self.connection.commit()
        return

    #DONT FORGET TO COMMIT
    def updatePlanet(self, name, shape, color, rings, memberID):
        data = [name, shape, color, rings, memberID]
        self.cursor.execute("UPDATE planets SET name = ?, shape = ?, color = ?, rings = ? WHERE id = ?", data)
        self.connection.commit()
        return

    
    def insertUser(self, firstName, lastName, email, password):
        data = [firstName, lastName, email, password]
        self.cursor.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    def emailExists(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM users WHERE email = ?", data)
        email = self.cursor.fetchone()
        return email