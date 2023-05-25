import cherrypy
import json
from pymongo import MongoClient

#@cherrypy.expose
class MyController(object):
    records = [
        {
            "id": 1,
            "title": "Songs in the key of life",
            "artist": "Stevie Wonder",
            "year": 1976,
            "company": "Motown"
        },
        {
            "id": 2,
            "title": "Kind of Blue",
            "artist": "Miles Davis",
            "year": 1959,
            "company": "Columbia"      
        },
        {
            "id": 3,
            "title": "Synchronicity",
            "artist": "The Police",
            "year": 1983,
            "company": "A&M"      
        },
        {
            "id": 4,
            "title": "Bach - Goldberg Variations",
            "artist": "Glenn Gould",
            "year": 1955,
            "company": "Sony Classical"      
        }    
    ]

    USR = "Paolo"
    PWD = "Password123"
    RLM = "BasicAuthREST"

    def validate_password(self, username, password):
        if (username == MyController.USR and password == MyController.PWD):
            return True
        else:
            return False


    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["PaoloTest"]
        self.collection = self.db["Dischi"]
        #cancello tutto
        self.collection.delete_many({})
        #inserimento
        self.collection.insert_many(MyController.records)

    @cherrypy.expose
    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, id=-1):
        ###
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'ngrok-skip-browser-warning'    
        ###
        projection = { "_id": 0 }
        if (int(id) == -1):            
            return list(self.collection.find(projection=projection))
        else:
            disco = list(self.collection.find(filter={ "id": int(id) }, projection=projection))
            if (len(disco) == 1):
                return (disco[0])
            else:
                cherrypy.response.status = 404
                return {} 


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        ###
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'ngrok-skip-browser-warning'    
        ###
        data = cherrypy.request.json
        res = self.collection.insert_one(data)
        return 0


    #@cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def PUT(self):
        data = cherrypy.request.json
        #print("**********************")
        #print(data)
        #print("**********************")
        filter = { "id": data["id"] }
        update = { "$set": { 
            "artist": data["artist"], 
            "title": data["title"],
            "year": data["year"],
            "company": data["company"] 
        }}
        res = self.collection.update_one(filter, update)
        if (res.modified_count > 0):
            return data["id"]
        else:
            cherrypy.response.status = 404
            return {} 
            

    #@cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self, id=-1):
        res = self.collection.delete_one({ "id": int(id) })
        if (res.deleted_count > 0):
            return id
        else:
            cherrypy.response.status = 404
            return {}

#if __name__ == '__main__':
conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        #'tools.response_headers.headers': [('Content-Type', 'application/json')]
        #devo aggiungere l'header "Access-Control-Allow-Origin" per abilitare le richieste da un dominio differente
        'tools.response_headers.headers': [
            #('Content-Type', 'application/json'), 
            ('Access-Control-Allow-Origin', '*'), 
            #("Access-Control-Allow-Headers", "*")
            #("Access-Control-Allow-Headers", "X-Requested-With")
            ("Access-Control-Allow-Headers", "ngrok-skip-browser-warning")
        ],
        #tolgo l'autenticazione per il momento
        #'tools.auth_basic.on': True,
        #'tools.auth_basic.realm': MyController.RLM,
        #'tools.auth_basic.checkpassword': MyController.validate_password
    }
}  

#cherrypy.quickstart(MyController(), '/', conf)
cherrypy.quickstart(MyController())