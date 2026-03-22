import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

def create_app():
    load_dotenv()
    
    app = Flask(__name__)

    MONGO_URI = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("MONGODB_DB")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    entries_collection = db["entries"]


    @app.route("/")
    def home():
        entries = list(entries_collection.find().sort("timestamp", -1))
        
        return render_template("home.html", entries=entries)


    @app.route("/entry", methods=["POST"])
    def add_entry():
        content = request.form.get("content", "").strip()
        if content:
            entries_collection.insert_one({"content": content, "timestamp": datetime.utcnow()})
        return redirect(url_for("home"))


    if __name__ == "__main__":
        app.run(debug=True)
    return app

