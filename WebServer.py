from flask import Flask, render_template, request
from Game.main import Game

import os

app = Flask(__name__)

game = Game()

@app.route('/')
def start():
    fork = os.fork()

    if fork > 0:
        game.run()

    return render_template("webpage.html")

@app.route('/player1', methods=["GET","POST"])
def player1():
    if request.method == "POST":
        game.players[1].newDirection = 'left'
        print(request.data)
    return render_template("player1.html")

@app.route('/player2', methods=["GET","POST"])
def player2():
    if request.method == "POST":
        print(request.data)
    return render_template("player2.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)

