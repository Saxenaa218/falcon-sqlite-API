import falcon,json
from regex1 import hit_count
import sqlite3
from waitress import serve
conn = sqlite3.connect("database.db",check_same_thread=False)
c = conn.cursor()
#c.execute("""CREATE TABLE IF NOT EXISTS db (id text primary key,rule text)""")
class testAPI:
    def on_post(self,req,resp):
        data = json.loads(req.stream.read())
        for i in data.keys():
            c.execute("INSERT INTO db(id,rule) VALUES (?,?)",(i, data[i]))
        conn.commit()
        resp.body = json.dumps({"id":"Inserted !!"})



class retrievalAPI:
    def on_post(self,req,resp):
        data = json.loads(req.stream.read())
        d = {}
        for i in data.keys():
            c.execute("SELECT rule FROM db WHERE id = (?)",(i))
            pattern = list(c.fetchone())[0]
            d[i] = hit_count(pattern,data[i])
        conn.commit()
        resp.body = json.dumps(d)


api = falcon.API()
api.add_route('/', testAPI())
api.add_route('/r', retrievalAPI())
serve(api,host="0.0.0.0",port="8800")