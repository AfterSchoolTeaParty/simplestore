from flask import Flask, request, render_template, redirect, url_for, session
import settings
import os
import shutil
from datetime import datetime
import requests

app = Flask(__name__, template_folder="views", static_folder="media", static_url_path="/media")
app.secret_key = "apa ini anjir"

# First time initialization only to make sure there's no storages
if os.path.isdir(settings.STORAGES_DIR):
    shutil.rmtree(settings.STORAGES_DIR)
    os.mkdir(settings.STORAGES_DIR)
else:
    os.mkdir(settings.STORAGES_DIR)

class Storage:
    def __init__(self, name, passkey):
        self.name = name
        self.passkey = passkey
        self.files = {}
        self.refresh()

    def refresh(self):
        requests.post(f"{settings.DATABASE_API_URL}/storages", data={"name" : self.name, "passkey" : self.passkey})    

    def items(self):
        return [file.replace(f"{self.name}_", "") for file in os.listdir(settings.STORAGES_DIR) if file.startswith(self.name)]

    @staticmethod
    def get(name=None):
        if name:
            try:
                return requests.get(f"{settings.DATABASE_API_URL}/storages/{name}").json()
            except:
                return requests.get(f"{settings.DATABASE_API_URL}/storages").json()
        else:
            return requests.get(f"{settings.DATABASE_API_URL}/storages").json()


class File:
    def __init__(self, name, storage, uploaded = None):
        self.name = name
        self.filename = "".join(self.name.split(".")[:-1])
        self.fileext = self.name.split(".")[-1]
        self.path = os.path.join(settings.STORAGES_DIR, f"{storage}_{self.name}")
        self.storage = storage
        if uploaded:
            self.uploaded = float(uploaded)
        else:
            self.uploaded = datetime.now().timestamp()

        self.refresh()

    def refresh(self):
        requests.post(f"{settings.DATABASE_API_URL}/files", data={"name" : self.filename, "storage" : self.storage, "extension" :  self.fileext, "uploaded" : self.uploaded})

    
    def delete(self):
        os.remove(self.path)

    @staticmethod
    def get(name=None):
        if name:
            try:
                return requests.get(f"{settings.DATABASE_API_URL}/files/{name}").json()
            except:
                return requests.get(f"{settings.DATABASE_API_URL}/files").json()
        else:
            return requests.get(f"{settings.DATABASE_API_URL}/files").json()

    
# Checking the existence of data
database_data_storages = requests.get(f"{settings.DATABASE_API_URL}/storages").json()
if database_data_storages:
    database_data_storages = list(database_data_storages.values())
else:
    database_data_storages = []

database_data_files = requests.get(f"{settings.DATABASE_API_URL}/files").json()
if database_data_files:
    database_data_files = list(database_data_files.values())
else:
    database_data_files = []

stores = {}
for storage in database_data_storages:
    stores[storage["name"]] = Storage(storage["name"], storage["passkey"])

files = {}
for file in database_data_files:
    files[file["file"]] = File(file["file"], file["storage"], file["uploaded"])


@app.route("/", methods=["GET"])
def index():
    if request.args.get("storage"):
        return redirect(url_for("storage", name=request.args.get("storage")))
    context = {}
    return render_template("index.html", **context)

@app.route("/<name>", methods=["POST", "GET"])
def storage(name):
    # Check if the storage is exist if not then create the storage
    if name not in stores.keys():
        if request.method == "POST":
            stores[name] = Storage(name, request.form.get("passkey"))
            return redirect(url_for("storage", name=name))
        return render_template("storageauth.html", pagetitle="Create Storage")

    # Check if the requested user is authenticated if not the do authentication
    if "authenticated" not in session.keys():
        if request.method == "POST":
            if stores[name].passkey == request.form.get("passkey"):
                session["authenticated"] = True
                return redirect(url_for("storage", name=name))
        return render_template("storageauth.html", pagetitle="Enter Storage")


    context = {
        "pagetitle" : name.capitalize(),
        "storage" : stores[name]
    }

    buffer_ = files.copy()
    for file in buffer_:
        if datetime.fromtimestamp(files[file].uploaded).hour != datetime.now().hour:
            files[file].delete()
            del files[file]

    if request.method == "POST":
        if request.files.get('file'):
            file = request.files.get("file")
            file.save(os.path.join(settings.STORAGES_DIR, f"{context['storage'].name}_{file.filename}"))
            filebuf = File(file.filename, context["storage"].name)
            context["storage"].files[file.filename] = filebuf
            files[file.filename] = filebuf
        if request.form.get("filename"):
            filename = request.form.get("filename")
            if filename in context["storage"].items():
                context["storage"].files[filename].delete()
                del context["storage"].files[filename]

    return render_template("storage.html", **context)

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=True)