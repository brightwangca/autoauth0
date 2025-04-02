"""Python Flask WebApp Auth0 integration example - Modified to remove Auth0"""

from os import environ as env
from flask import Flask, render_template # Removed json, urllib, authlib, dotenv, redirect, session, url_for

# ENV_FILE loading removed

app = Flask(__name__)
# app.secret_key removed - No session needed without login

# oauth object registration removed

# Controllers API
@app.route("/")
def home():
    # Simplified home page - removed session and pretty printing user info
    return render_template("home.html")

# /callback route removed

# /login route removed

# /logout route removed

if __name__ == "__main__":
    # Keep the PORT logic but remove dependency on env potentially set by dotenv
    port = int(env.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
