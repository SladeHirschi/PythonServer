from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from planetsDB import planetsDB
from passlib.hash import bcrypt
from http import cookies
import json
from session_store import SessionStore

SESSION_STORE = SessionStore()

db = planetsDB()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def readCookie(self):
        if "Cookie" in self.headers:
            print("the COOKIES are:", self.headers["Cookie"])
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSessionData(self):
        self.readCookie()
        print("STEVEN", self.cookie)
        # if the session ID is found in the cookie
        if "sessionId" in self.cookie:
            #load the session ID value from the cookie objext
            sessionId = self.cookie["sessionId"].value

            # load the session data from the sesson store using the session ID
            sessionData = SESSION_STORE.getSessionData(sessionId)
            print("If this is seen then you should not see the other")
                # if session data exists

            if sessionData == None:
                #create a new session and assign a new cookie with the session ID
                sessionId = SESSION_STORE.createSession()
                print("This should not be seen")
                sessionData = SESSION_STORE.getSessionData(sessionId)
                self.cookie["sessionId"] = sessionId
            #otherwise if session data does not exist


        #otherwise, if no session Id in the cookie
        else:
            sessionId = SESSION_STORE.createSession()
            print("This is the session Id!!!!!!!!!!!!!!!!!!!!!", sessionId)
            sessionData = SESSION_STORE.getSessionData(sessionId)
            self.cookie["sessionId"] = sessionId
            print("This is the cookie Id!!!!!!!!!!!!!!!!", self.cookie)
            

        self.sessionData = sessionData


    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def handleNotFound(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

    def handleNotAuthenticated(self):
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes("Not Authenticated", "utf-8"))
    
    # def handleUnproccessable(self):
    #     self.send_response(422)
    #     self.end_headers()
    #     self.wfile.write(bytes("Not Processable", "utf-8"))
    
    def handleGetPlanets(self):
        if "userId" not in self.sessionData:
            self.handleNotAuthenticated()
            return
        # 1. send a status code
        self.send_response(200)
        # 2. send any headers
        self.send_header("Content-Type", "application/json")
        # 3. finish any headers (whether we have headers ro send or not)
        self.end_headers()
        # 4. send a body to the client:
        self.wfile.write(bytes(json.dumps(db.getAllPlanets()), "utf-8"))


    def handleGetOnePlanet(self, memberID):
        if "userId" not in self.sessionData:
            self.handleNotAuthenticated()
            return
        onePlanet = db.getOnePlanet(memberID)
        if onePlanet != None:
            # 1. send a status code
            self.send_response(200)
            # 2. send any headers
            self.send_header("Content-Type", "application/json")
            # 3. finish any headers (whether we have headers ro send or not)
            self.end_headers()
            # 4. send a body to the client:
            onePlanet = db.getOnePlanet(memberID)
            self.wfile.write(bytes(json.dumps(db.readAllRecords()), "utf-8"))
        else:
            self.handleNotFound()

    def handleDeleteOnePlanet(self, memberID):
        if "userId" not in self.sessionData:
            self.handleNotAuthenticated()
            return
        onePlanet = db.getOnePlanet(memberID)
        if onePlanet != None:
            # 1. send a status code
            self.send_response(200)
            # 2. send any headers
            # 3. finish any headers (whether we have headers ro send or not)
            self.end_headers()
            db.deletePlanet(memberID)
        else:
            self.handleNotFound()


    def handleCreatePlanet(self):
        if "userId" not in self.sessionData:
            self.handleNotAuthenticated()
            return
        print("the HEADERS are:", self.headers)

        #1. read the request body
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the BODY:", body)

        # #2. parse the body into usable data
        parsed_body = parse_qs(body)
        print("parsed BODY:", parsed_body)

        # #3. append the new data to our data
        planet_name = parsed_body['name'][0]
        planet_color = parsed_body['color'][0]
        planet_rings = parsed_body['rings'][0]
        planet_shape = parsed_body['shape'][0]
        db.insertPlanet(planet_name, planet_shape,  planet_color, planet_rings)

        # #send a response to the client
        self.send_response(201)
        self.end_headers()
        
    def handleUpdateOnePlanet(self, memberID):
        if "userId" not in self.sessionData:
            self.handleNotAuthenticated()
            return
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the BODY:", body)

        # #2. parse the body into usable data
        parsed_body = parse_qs(body)
        print("parsed BODY:", parsed_body)

        # #3. append the new data to our data
        planet_name = parsed_body['name'][0]
        planet_color = parsed_body['color'][0]
        planet_rings = parsed_body['rings'][0]
        planet_shape = parsed_body['shape'][0]
        db.updatePlanet(planet_name, planet_shape,  planet_color, planet_rings, memberID)

        # #send a response to the client
        self.send_response(200)
        self.end_headers()



    def handleCreateUser(self):
        print("the HEADERS are:", self.headers)

        #1. read the request body
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the BODY:", body)

        # #2. parse the body into usable data
        parsed_body = parse_qs(body)
        print("parsed BODY:", parsed_body)

        # #3. append the new data to our data
        user_firstName = parsed_body['firstName'][0]
        user_lastName = parsed_body['lastName'][0]
        user_email = parsed_body['email'][0]
        user_password = bcrypt.hash(parsed_body['password'][0])
        user = db.emailExists(user_email)
        if user == None:
            db.insertUser(user_firstName, user_lastName, user_email, user_password)
            self.send_response(201)
        else:
            self.send_response(422)

        # #send a response to the client
        self.end_headers()

    def handleCreateSession(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the BODY:", body)

        parsed_body = parse_qs(body)
        print("parsed BODY:", parsed_body)

        user_email = parsed_body['email'][0]
        user_password = parsed_body['password'][0]

        
        user = db.emailExists(user_email)
        print(user)
        if user != None:
            if bcrypt.verify(user_password, user["password"]):
                
                self.sessionData["userId"] = user["id"]
                # self.cookie["sessionId"] = user["id"]
                print(self.sessionData)
                self.send_response(201)
                self.end_headers()
            else:
                print("Wrong Password")
                self.handleNotAuthenticated()
    
        else:
            print("No Email Exists")
            self.handleNotAuthenticated()


    def do_GET(self):
        self.loadSessionData()
        print("the PATH is: ", self.path)
        #print("the HEADERS are:", self.headers)
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            memberID = parts[2]
        else:
            memberID = None

        if collection == "planets":
            if memberID:
                #retrieve member
                self.handleGetOnePlanet(memberID)
            else:
                self.handleGetPlanets()
        else:
            self.handleNotFound()


    def do_POST(self):
        
        self.loadSessionData()
        if self.path == "/planets":
            self.handleCreatePlanet()

        elif self.path == "/users":
            self.handleCreateUser()

        elif self.path == "/sessions":
            self.handleCreateSession()

        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.loadSessionData()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST, DELETE, PUT")
        self.send_header("Access-Control-Allow-Methods", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        self.loadSessionData()
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            memberID = parts[2]
        else:
            memberID = None

        if collection == "planets":
            if memberID:
                #retrieve member
                self.handleDeleteOnePlanet(memberID)
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.loadSessionData()
        print(self.path)
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            memberID = parts[2]
        else:
            memberID = None

        if collection == "planets":
            if memberID:
                #retrieve member
                self.handleUpdateOnePlanet(memberID)
        else:
            self.handleNotFound()



def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyHTTPRequestHandler)

    print("Server is ready! Listening...")
    server.serve_forever()
    #Nothing past this will be exectuted

run()