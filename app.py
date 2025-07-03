import json
import random
import datetime
from flask import Flask, make_response, render_template, redirect, request, abort
from functools import wraps
from env import webring_name, public_url, password
from webring import create_db, insert_site, list_all_sites, get_site_index
from auth import generate, verify

version = "0.0.1"
app = Flask(__name__)

create_db()

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401)
        
        token = auth_header.split(" ")[1]

        if not verify(token):
            abort(403)
        
        return f(*args, **kwargs)

    return wrapper

@app.route("/")
def index(name=None):
    res = make_response(json.dumps({
        "name": webring_name,
        "url": public_url,
        "version": version
    }))
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/next")
def next_site():
    url = request.args.get("url")
    if not url:
        return 400

    sites = list_all_sites()
    i = get_site_index(url, sites)
    if i is None:
        return "site not found", 404
    
    next_index = (i + 1) % len(sites)
    return redirect(sites[next_index][1])

@app.route("/prev")
def prev_site():
    url = request.args.get("url")
    if not url:
        return 400

    sites = list_all_sites()
    i = get_site_index(url, sites)
    if i is None:
        return "site not found", 404
    
    prev_index = (i - 1) % len(sites)
    return redirect(sites[prev_index][1])

@app.route("/random")
def random_site():
    sites = list_all_sites()
    return redirect(random.choice(sites)[1])

@app.route("/list")
def sitelist():
    sites = list_all_sites()
    schema = [
        {
            "name": name,
            "url": url,
            "owner": owner,
            "added": added
        }
        for name, url, owner, added in sites
    ]
    res = make_response(json.dumps(schema))
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/token", methods=["POST"])
def generate_token():
    data = request.json
    if not data or data.get("password") != password:
        res = make_response(json.dumps({
            "success": False,
            "message": "unauthorized"
        }))
        res.headers["Content-Type"] = "application/json"
        return res, 401
    
    token = generate()

    res = make_response(json.dumps({
        "success": True,
        "message": "here is your JWT token! remember not to share it with anyone!",
        "token": token
    }))
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/insert", methods=["POST"])
@require_auth
def insert():
    data = request.json
    name = data.get("name")
    url = data.get("url")
    owner = data.get("owner")
    date = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if not all([name, url, owner]):
        res = make_response(json.dumps({
            "success": False,
            "message": "missing required fields"
        }))
        res.headers["Content-Type"] = "application/json"
        return res, 400

    insert_site(name, url, owner, date)

    res = make_response(json.dumps({
        "success": True,
        "message": f"site {url} has been added to the webring!"
    }))
    res.headers["Content-Type"] = "application/json"
    return res

if __name__ == '__main__':
    app.run()