import time
from uuid import uuid4
from flask import Flask, request, Response
from flask_cors import CORS
from flask_cors import cross_origin

# platform_run = 'window'
# if platform.system().lower() == 'windows':
#     platform_run = 'windows'
# elif platform.system().lower() == 'linux':
#     platform_run = 'linux'
# print('platform_run', platform_run)

father_path = os.path.dirname(os.path.realpath(sys.argv[0]))
save_path = os.path.join(father_path, 'static', 'music')

app = Flask(__name__)
CORS(app, automatic_options=True)


# first add ten more routes to load routing system
# ------------------------------------------------
@app.route("/api/download/<name>", methods=["GET"])
def api_download(name):
	pass
@app.route("/api/add_audio", methods=["POST"])
def api_add_audio():
    data = request.get_json()
    language_type = data.get("language_type").lower()


@app.route("/route-<int:n>")
def route_n(n):
    return "ok"

@app.route("/route-dyn-<int:n>/<part>")
def route_dyn_n(n, part):
    return "ok"

for n in range(5):
    app.add_url_rule(f"/route-{n}", f"route_{n}", route_n)
    app.add_url_rule(f"/route-dyn-{n}/<part>", f"route_dyn_{n}", route_dyn_n)

# then prepare endpoints for the benchmark
# ----------------------------------------
@app.route("/html")
def html():
    """Return HTML content and a custom header."""
    content = "<b>HTML OK</b>"
    headers = {"X-Time": f"{time.time()}"}
    return Response(content, headers=headers)

@app.route("/upload", methods=["POST"])
def upload():
    """Load multipart data and store it as a file."""
    if "file" not in request.files:
        return Response("ERROR", status=400)
    
    filename = f"/tmp/{uuid4().hex}"
    request.files["file"].save(filename)
    return Response(filename)

@app.route("/api/users/<int:user>/records/<int:record>", methods=["PUT"])
def api(user, record):
    """Check headers for authorization, load JSON/query data and return as JSON."""
    if "authorization" not in request.headers:
        return Response("ERROR", status=401)
    
    data = {
        "params": {"user": user, "record": record},
        "query": dict(request.args),
        "data": request.get_json(),
    }
    return Response(json.dumps(data), mimetype="application/json")


# RESTful风格
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    # 我们的数据库模型 - 与以前相同

class UserResource(Resource):
    # 描绘了所有 CRUD 操作的 Flask-RESTful 资源类 - 与以前相同

api.add_resource(UserResource, '/user', '/user/<int:user_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
