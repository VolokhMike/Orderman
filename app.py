from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


def get_all_pizzas():
    try:
        sqlite_connection = sqlite3.connect("sql_pizza.db")
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM db_pizza")
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
def add_pizza():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("ingrediens")
        price = request.form.get("price")

        try:
            sqlite_connection = sqlite3.connect('sql_pizza.db')
            cursor = sqlite_connection.cursor()
            insert_query = "INSERT INTO db_pizza (name, description, price) VALUES (?, ?, ?)"
            print(name, description, float(price))
            cursor.execute(insert_query, (name, description, float(price)))


            sqlite_connection.commit()
            print("Данные успешно добавлены")

        except sqlite3.IntegrityError as e:
            print("Ошибка: такие данные уже существуют или нарушены ограничения целостности.", e)

        except sqlite3.Error as error:
            print("Ошибка при работе с базой данных:", error)

        finally:
            if sqlite_connection:
               sqlite_connection.close()

    return render_template("add_pizza.html")

@app.route('/')
def index():
    sqlite_connection = sqlite3.connect('sql_pizza.db')
    cursor = sqlite_connection.cursor()


    create_table_query = '''
                CREATE TABLE IF NOT EXISTS db_pizza (
                    name TEXT NOT NULL,
                    description TEXT UNIQUE,
                    price REAL  
                );
                '''
    cursor.execute(create_table_query)
    return render_template('login.html')

@app.post("/login/")
def login_page():
    username = request.form.get("username")
    if username == "admin":
        return redirect(url_for("admin_page"))
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
    pizzas = get_all_pizzas()
    context = {
        "back_button": "Повернутися на головну сторінку",
        "pizzas": pizzas
    }
    return render_template("menu.html", **context)


if __name__ == '__main__':
    app.run(port=6060, debug=True)