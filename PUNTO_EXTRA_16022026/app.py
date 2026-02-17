from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

api = "http://127.0.0.1:5000/v1/usuarios/"

@app.route("/")
def index():
    response = requests.get(api)
    if response.status_code == 200:
        usuarios = response.json().get("data", [])
    else:
        usuarios = []
    return render_template("Usuarios.html", usuarios=usuarios)

@app.route("/agregar", methods=["POST"])
def agregar_usuario():
    nombre = request.form.get("nombre")
    edad = request.form.get("edad")
    id_usuario = request.form.get("id")
    
    if nombre and edad and id_usuario:
        usuario = {"id": int(id_usuario), "nombre": nombre, "edad": int(edad)}
        response = requests.post(api, json=usuario)
        if response.status_code == 200:
            return redirect(url_for("index"))
    return "Error al agregar usuario", 400

@app.route("/eliminar", methods=["POST"])
def eliminar_usuario():
    usuario_id = request.form.get("id")
    
    if usuario_id:
        response = requests.delete(f"{api}{usuario_id}")
        
        if response.status_code == 200:
            return redirect(url_for("index"))
        else:
            return "Error al eliminar el usuario. Puede que no exista.", 400
    return "Error: ID no proporcionado.", 400

if __name__ == "__main__":
    app.run(debug=True, port=5010)
