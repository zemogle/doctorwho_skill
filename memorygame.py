import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

DOCTORS = ["William Hartnell", "Patrick Troughton", "Jon Pertwee", "Tom Baker", "Peter Davison",
    "Colin Baker", "Silvester McCoy", "Paul McGann", "Christopher Eccleston", "David Tennent",
    "Matt Smith", "Peter Capaldi", "Jodi Whittacker"]

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("YesIntent")
def next_round():
    number = randint(1, 13)
    doctor_name = DOCTORS[number-1]
    round_msg = render_template('round', doctor=doctor_name)
    session.attributes['number'] = number

    return question(round_msg)

@ask.intent("AnswerIntent")
def answer(doctor_number):
    true_number = session.attributes['number']
    if int(doctor_number) == int(true_number):
        msg = render_template('win')
    else:
        msg = render_template('lose', doctor_name=DOCTORS[session.attributes['number']-1], number=true_number, answer=doctor_number)

    return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)
