from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/menu')
def menu():
    pizza = [
        {'name': 'Байрактар новий', 'description': 'Metal, dought, salami, fire, program', 'price': '23 euro'},
        {'name': 'Python vs C++', 'description': 'Pycharm, visual_studio, dought, server, fish, maus ', 'price': '36 euro'},
        {'name': 'Git_hub', 'description': 'Senior, dought, salami, fire, program', 'price': '45 euro'},
]

    return render_template('menu.html', pizzas=pizza)


if __name__ == '__main__':
    app.run(port=5000, debug=True)