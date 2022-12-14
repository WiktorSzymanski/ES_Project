from flask import Flask, render_template, request
from Game.main import Game
from multiprocessing import Process, Queue

import os

app = Flask(__name__)

def run_game(queue):
    game = Game()
    game.run(queue)

queue = Queue()
process = Process(target=run_game, args=(queue,))
flag = 0

@app.route('/')
def start():
    global flag
    if not(flag):
        flag = 1
        process.start()
    return render_template("webpage.html")


@app.route('/player1', methods=["GET","POST"])
def player1():
    if request.method == "POST":
        queue.put((1, request.data.decode("utf-8")))
    return render_template("player1.html")

@app.route('/player2', methods=["GET","POST"])
def player2():
    if request.method == "POST":
        queue.put((2, request.data.decode("utf-8")))
    return render_template("player2.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)

