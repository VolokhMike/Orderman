from flask import Flask, render_template, request, url_for, flash, redirect, abort
import requests
import sqlite3
from connection import get_db_connection, create_table
from poll import poll_data

filename = "data.txt"

app = Flask(__name__)
app.config["SECRET_KEY"] = "q"
create_table()


@app.route("/")
def main():
    location = "Kherson"
    api_key = "9916e68360d417f5b8991f166eb233d4"
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric")
    session = weather.json()

    current_weather = session
    print(current_weather)
    weather_ivent = {
        "temp": current_weather["main"]["temp"]
    }
    return render_template("login.html", weather_ivent=weather_ivent)


def get_all_pizzas():
    try:
        sqlite_connection = sqlite3.connect("sql_pizza.db")
        sqlite_connection.row_factory = sqlite3.Row
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM pizza")
        pizzas = cursor.fetchall()
        return pizzas

    except sqlite3.Error as error:
        print("Помилка при отриманні піц:", error)
        return []

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Піца отримана")


@app.get("/add_pizza/")
def add_pizza_get():
    return render_template("add_pizza.html")


@app.post("/add_pizza/")
def add_pizza_post():
    if request.method == "POST":
        name = request.form.get("name")
        ingredients = request.form.get("ingredients")
        price = request.form.get("price")

        connection = get_db_connection()
        insert_query = """INSERT INTO pizza 
        (name, ingredients, price) 
        VALUES (?, ?, ?);"""
        connection.execute(insert_query, (name, ingredients, int(price)))
        connection.commit()

    return render_template("add_pizza.html")


@app.route('/')
def index():
    return render_template('login.html')


@app.post("/login/")
def login_page():
    username = request.form.get("username")
    if username == "admin":
        return redirect(url_for("admin_page"))
    return redirect(url_for("menu_page"))


@app.get("/poll/")
def poll_page():
    return render_template("poll.html", poll_data=poll_data)


@app.post("/poll/")
def poll_submit():
    answers = {
        'question1': request.form.get('question1'),
        'question2': request.form.get('question2'),
        'question3': request.form.get('question3')
    }
    print("Полученные ответы:", answers)  # для отладки
    return redirect(url_for("menu_page"))


@app.get("/admin")
def admin_page():
    pizzas = get_all_pizzas()
    context = {
        "back_button": "Повернутися на головну сторінку",
        "pizzas": pizzas
    }
    return render_template("admin.html", **context)


@app.get('/menu/')
def menu_page():
    weather_ivent = main()
    pizzas = get_all_pizzas()
    context = {
        "back_button": "Повернутися на головну сторінку",
        "pizzas": pizzas
    }
    return render_template("menu.html", **context, weather_ivent=weather_ivent)


def get_pizza_id(pizza_id):
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    pizza = connection.execute("SELECT * FROM pizza WHERE id = ?", (pizza_id,)).fetchone()
    connection.close()
    return pizza


@app.get("/<int:pizza_id>/edit/")
def get_edit(pizza_id):
    pizza = get_pizza_id(pizza_id)
    return render_template("edit.html", pizza=pizza)


@app.post("/<int:pizza_id>/edit/")
def post_edit(pizza_id):
    pizza = get_pizza_id(pizza_id)
    name = request.form["name"]
    ingredients = request.form["ingredients"]
    price = request.form["price"]
    if not name or len(name) < 4:
        flash("Name is not required!")
        return render_template("edit.html", pizza=pizza)
    else:
        connection = get_db_connection()
        connection.execute("UPDATE pizza SET name = ?, ingredients = ?, price = ? WHERE id =?",
                           (name, ingredients, price, pizza_id))
        connection.commit()
        connection.close()
        return redirect(url_for("menu_page"))


@app.post("/<int:pizza_id>/delete/")
def pizza_delete(pizza_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM pizza WHERE id =?", (pizza_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("menu_page"))


if __name__ == '__main__':
    app.run(port=9090, debug=True)
