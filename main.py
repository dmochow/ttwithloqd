import pandas as pd
from flask import Flask, render_template, request, session
import random
import pygame
import numpy as np
import datetime


app = Flask(__name__)
app.secret_key = '3432'

# Initialize pygame
pygame.mixer.init()

correct_mp3=["Coolesteva.mp3","better.mp3","smooth.mp3"]
incorrect_mp3=["suprsuck.mp3","sob.mp3","u-stink.mp3","Anderson.mp3","dammit.mp3","smackyou.mp3"]

# Sound files for correct and incorrect answers
correct_sounds = [pygame.mixer.Sound(x) for x in correct_mp3]
incorrect_sounds = [pygame.mixer.Sound(x) for x in incorrect_mp3]

correct_answers = 0
total_questions_attempted = 0
answer_log = {'num1':[], 'num2':[], 'answer':[], 'is_correct':[]}
datestr = datetime.datetime.now().strftime('%m%d%y-%H%M%S')

# Define the range of multiplication questions
min_number = 1
max_number = 12

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    name = request.form['name']
    age = request.form['age']

    session['name'] = name
    session['age'] = age

    # Generate random numbers for the question
    num1 = random.randint(min_number, max_number)
    num2 = random.randint(min_number, max_number)

    # Calculate the correct answer
    correct_answer = num1 * num2

    return render_template('question.html', num1=num1, num2=num2, correct_answer=correct_answer, name=name, age=age)



@app.route('/check_answer', methods=['POST'])
def check_answer():

    #name = session.get('name', 'Guest')
    #age = session.get('age', 'N/A')

    name = request.form['name']
    age = request.form['age']

    user_answer = int(request.form['user_answer'])
    correct_answer = int(request.form['correct_answer'])

    global correct_answers
    global total_questions_attempted
    global answer_log
    global datestr

    total_questions_attempted += 1

    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])

    answer_log['num1'].append(str(num1))
    answer_log['num2'].append(str(num2))
    answer_log['answer'].append(str(user_answer))
    answer_log['is_correct'].append(str(user_answer==correct_answer))
    print(answer_log)

    csv_filename=datestr+'_'+name+'_'+age+'_test_answer_log'
    pd.DataFrame(answer_log,index=np.array(range(total_questions_attempted))).to_csv(csv_filename)

    if user_answer == correct_answer:
        correct_answers += 1
        ii=random.randint(0,len(correct_sounds)-1)
        pygame.mixer.Sound.play(correct_sounds[ii])
        return render_template('correct.html', num1=num1, num2=num2, correct_answer=correct_answer)
    else:
        ii=random.randint(0,len(incorrect_sounds)-1)
        pygame.mixer.Sound.play(incorrect_sounds[ii])
        return render_template('incorrect.html', num1=num1, num2=num2, correct_answer=correct_answer)





@app.context_processor
def scoreboard():
    return dict(correct_answers=correct_answers, total_questions_attempted=total_questions_attempted)

if __name__ == '__main__':
    app.run(debug=True)
