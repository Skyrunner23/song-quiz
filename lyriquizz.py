from flask import Flask, request, jsonify, make_response, render_template
from flask_bootstrap import Bootstrap5
from http import HTTPStatus
from app.services import Services
from datetime import datetime
from logging.config import dictConfig
from model.puzzle import *
import re
from unidecode import unidecode


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
#  /api/today, will provide just the clue for today's puzzle as a JSON (GET)
#  /api/today?part=clue, same as /today
#  /api/today?part=puzzle, will provide the whole of today's puzzle as a JSON (GET)
#  /api/yesterday, will provide all of yesterday's (or the most recent day's) puzzle as a JSON (GET)
#  /api/submit, will handle submissions not from the web form
#  /, will provide a web form with today's clue and yesterday's full puzzle (GET)
#  /result, handles submission/grading from web form (POST)
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
    past = services.get_yesterday().serialize()
    if not clue:
        return nottoday(now, past)
    clue = clue.serialize()
    return render_template('quiz.html',
                            todaysdate=now.strftime("%B %-d, %Y"),
                            renderdatetime=now.strftime("%c"),
                            year=clue['year'], genre=clue['genre'], lyric=clue['lyric'],
                            past_date=past['date'],
                            past_year=past['clue']['year'],
                            past_genre=past['clue']['genre'],
                            past_lyric=past['clue']['lyric'],
                            past_song=past['answer']['title'],
                            past_artist=past['answer']['artist'])


@app.route("/result", methods=['POST'])
def scorequiz():
    now = datetime.now(tz=services.LOCALTZ)
    puzzle = services.get_today(justclue=False)
    if not puzzle:
        past = services.get_yesterday().serialize()
        return nottoday(now, past)

    puzzledate = puzzle.date

    #  Store user's submission
    guessUserName = sanitize_input(request.form.get('guessUserName'))
    guessSongTitle = sanitize_input(request.form.get('guessSongTitle'))
    guessArtist = sanitize_input(request.form.get('guessArtist'))
    userSub = Submission(guessUserName, puzzledate, guessSongTitle, guessArtist)
    sub_status = services.record_submission(userSub)

    if not sub_status:
        error_message = "app.py, scorequiz(): services.record_submission returned False"
        return render_template('error.html', error_msg=error_message)

    userscore = puzzle.answer.grade(userSub)

    return render_template('result.html',
                           todaysdate=now.strftime("%B %-d, %Y"),
                           renderdatetime=now.strftime("%c"),
                           year=puzzle.clue.year,
                           genre=puzzle.clue.genre,
                           lyric=puzzle.clue.lyric,
                           title=puzzle.answer.title,
                           artist=puzzle.answer.artist,
                           user_title=guessSongTitle,
                           user_artist=guessArtist,
                           userscore=userscore)


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


def nottoday(now, past):
    return render_template('nottoday.html',
                           todaysdate=now.strftime("%B %-d, %Y"),
                           renderdatetime=now.strftime("%c"),
                           past_date=past['date'],
                           past_year=past['clue']['year'],
                           past_genre=past['clue']['genre'],
                           past_lyric=past['clue']['lyric'],
                           past_song=past['answer']['title'],
                           past_artist=past['answer']['artist'])


def sanitize_input(incoming: str) -> str:
    """keep only ascii text and limited punctuation, whitespace to one"""
    allowed = re.compile(r"[^,.?!'’;:#$@\w ]", flags=re.IGNORECASE)
    incoming = unidecode(incoming)                       # accented chars to base char
    incoming = re.sub(allowed, '', incoming)        # keep only the allowed chars
    incoming = re.sub(r'\s+', ' ', incoming) # shorten multiple spaces to one
    incoming = incoming.strip()                          # strip leading/trailing whitespace
    return incoming


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
