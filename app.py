from flask import Flask, request, jsonify, make_response, render_template
from flask_bootstrap import Bootstrap5
from http import HTTPStatus
from app.services import Services
from datetime import datetime
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
#  /today?part=clue, same as /today
#  /today?part=puzzle, will provide the whole of today's puzzle as a JSON (GET)
#  /yesterday, will provide all of yesterday's (or the most recent day's) puzzle as a JSON (GET)
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
bootstrap = Bootstrap5(app)


@app.route("/", methods=['GET'])
def lyriquizz():
    now = datetime.now(tz=services.LOCALTZ)
    clue = services.get_today(justclue=True)
    past = services.get_yesterday()
    if clue:
        clue = clue.serialize()
        past = past.serialize()
        return render_template('quiz.html',
                               todaysdate=now.strftime("%B %-d, %Y"),
                               renderdatetime=now.strftime("%c"),
                               year=clue['year'], genre=clue['genre'], lyric=clue['lyric'],
                               past_date=past['date'],
                               past_year=past['clue']['year'], past_genre=past['clue']['genre'],
                               past_lyric=past['clue']['lyric'],
                               past_song=past['answer']['title'],
                               past_artist=past['answer']['artist'])
    else:
        past = past.serialize()
        return render_template('nottoday.html',
                               todaysdate=now.strftime("%B %-d, %Y"),
                               renderdatetime=now.strftime("%c"),
                               past_date=past['date'],
                               past_year=past['clue']['year'], past_genre=past['clue']['genre'],
                               past_lyric=past['clue']['lyric'],
                               past_song=past['answer']['title'],
                               past_artist=past['answer']['artist'])


@app.route("/result", methods=['POST'])
def scorequiz():
    now = datetime.now(tz=services.LOCALTZ)
    puzzledate = now.strftime(services.repo.DATEFORMAT)
    user_name = request.form.get('guessUserName')
    user_title = request.form.get('guessSongTitle')
    user_artist = request.form.get('guessArtist')
    user_sub = Submission(user_name, puzzledate, user_title, user_artist)
    sub_status = services.record_submission(user_sub)
    print(f"Submission status: {sub_status}")
    #return render_template()


@app.route("/api/today")
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


@app.route("/api/yesterday")
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
