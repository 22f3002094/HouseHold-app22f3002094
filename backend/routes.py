from app import app

@app.route("/")
def index():
    return "hello world"


@app.route("/login")
def login():
    return "<h1>Login Page</h1>"