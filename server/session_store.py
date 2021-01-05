import base64, os

class SessionStore:

    def __init__(self):
        #dictionary of dictionaries one for each client
        self.sessions = {}
        

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def createSession(self):
        #generate a new session ID
        sessionId = self.generateSessionId()
        # create a new session dictionary inside the sessions dictionary
        self.sessions[sessionId] =  {}
        # return the new session ID for future access to this session
        return sessionId

    def getSessionData(self, sessionId):
        if sessionId in self.sessions:
            # if found, return the session data for this session ID
            return self.sessions[sessionId]
        else:
            # otherwise, return nothing
            return None

