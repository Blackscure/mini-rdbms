from flask import Blueprint, render_template, request, redirect, url_for
from web.db import manager
from rdbms.sql.ast import Insert, Update, Delete
from rdbms.executor.insert import execute_insert
from rdbms.executor.update import execute_update
from rdbms.executor.delete import execute_delete

web_bp = Blueprint("web", __name__)

# READ — list all users
@web_bp.route("/")
def index():
    table = manager.current.get_table("users")
    users = table.select()  # Returns all rows
    return render_template("users/list.html", users=users)

# CREATE
@web_bp.route("/users/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        execute_insert(
            Insert("users", [
                request.form["id"],
                request.form["name"]
            ]),
            manager
        )
        return redirect(url_for("web.index"))
    return render_template("users/create.html")

# UPDATE
@web_bp.route("/users/edit/<id>", methods=["GET", "POST"])
def edit_user(id):
    table = manager.current.get_table("users")
    user_list = table.select(("id", id))
    if not user_list:
        return "User not found", 404
    user = user_list[0]

    if request.method == "POST":
        execute_update(
            Update(
                "users",
                {"name": request.form["name"]},
                ("id", "=", id)
            ),
            manager
        )
        return redirect(url_for("web.index"))

    return render_template("users/edit.html", user=user)

# DELETE
@web_bp.route("/users/delete/<id>")
def delete_user(id):
    execute_delete(
        Delete("users", ("id", "=", id)),
        manager
    )
    return redirect(url_for("web.index"))