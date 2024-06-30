from flask import Flask, request, jsonify, make_response
from http import HTTPStatus
from app.services import Services
from logging.config import dictConfig
from model.puzzle import *


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Endpoints:
#  /today, will provide just the clue for today's puzzle as a JSON (GET)
#  /yesterday, will provide all of yesterday's puzzle as a JSON (GET)
#  /, will provide a web form with today's clue and yesterday's full puzzle (GET)
#
# Eventually, we'll want to
#  (0) receive guesses, add to a database? (current G Forms functionality)
#  (1) implement user-level authentication,
#  (2) evaluate users' guesses
#  (3) store users' history
#  (4) make the game history available, also?
#  (5) provide overall statistics?
#  (6) provide a monthly leaderboard?


app = Flask(__name__)
services = Services()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/today")
def today():
    # parameters: part=puzzle, part=clue (default)
    part = request.args.get('part')
    if part in {'clue', None}:
        justclue = True
    elif part in {'puzzle'}:
        justclue = False
    else:
        return jsonify(""), HTTPStatus.BAD_REQUEST
    lookup = services.get_today(justclue=justclue)
    if lookup:
        response = make_response(lookup.serialize())
        response.status = HTTPStatus.OK
        return response
    else:
        return jsonify(), HTTPStatus.NO_CONTENT


@app.route("/yesterday")
def yesterday():
    puzzle = services.get_yesterday()
    if puzzle:
        response = make_response(puzzle.serialize())
        response.status = HTTPStatus.OK
        return response
    else:
        return jsonify(), HTTPStatus.NO_CONTENT

if __name__ == "__main__":
    app.run()