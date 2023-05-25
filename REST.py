import cherrypy
#import cherrypy_cors

@cherrypy.expose
class MyController(object):
    dischi = [
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


    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, id=-1):
        if (int(id) == -1):
            return self.dischi
        else:
            #return self.dischi[int(id)]
            disco = [d for d in self.dischi if d["id"] == int(id)]
            if (len(disco) == 1):
                return (disco[0])
            else:
                cherrypy.response.status = 404
                return {} 



    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        data = cherrypy.request.json
        self.dischi.append(data)
        return {}


    @cherrypy.tools.json_out()
    def PUT(self, id=-1, **kwargs):
        #TODO
        return int(id)


    @cherrypy.tools.json_out()
    def DELETE(self, id=-1):
        index = -1
        for d in range(0, len(self.dischi)) :
            if self.dischi[d]["id"] == int(id):
                index = d
                break
        if index != -1:
            self.dischi.pop(index)
        return 0


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            #'tools.response_headers.headers': [('Content-Type', 'application/json')]
            #devo aggiungere l'header "Access-Control-Allow-Origin" per abilitare le richieste da un dominio differente
            'tools.response_headers.headers': [
                ('Content-Type', 'application/json'), 
                ('Access-Control-Allow-Origin', '*'),
                #('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
                ('Access-Control-Allow-Headers', '*'),
                ('ngrok-skip-browser-warning', '*'),
                ('User-Agent', 'plutopippopaperino')
            ]
        }
    }  

    cherrypy.quickstart(MyController(), '/', conf)