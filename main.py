from flask import Flask, render_template, request, redirect, url_for
import random
import pygame

app = Flask(__name__)

# Initialize pygame
pygame.mixer.init()

correct_mp3=["Coolesteva.mp3","better.mp3","smooth.mp3"]
incorrect_mp3=["suprsuck.mp3","sob.mp3","u-stink.mp3","Anderson.mp3","dammit.mp3","smackyou.mp3"]

# Sound files for correct and incorrect answers
correct_sounds = [pygame.mixer.Sound(x) for x in correct_mp3]
incorrect_sounds = [pygame.mixer.Sound(x) for x in incorrect_mp3]

correct_answers = 0
total_questions_attempted = 0

#correct_sound = pygame.mixer.Sound("Coolesteva.mp3")
#incorrect_sound = pygame.mixer.Sound("suprsuck.mp3")

# Define the range of multiplication questions
min_number = 1
max_number = 12

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    # Generate random numbers for the question
    num1 = random.randint(min_number, max_number)
    num2 = random.randint(min_number, max_number)

    # Calculate the correct answer
    correct_answer = num1 * num2

    return render_template('question.html', num1=num1, num2=num2, correct_answer=correct_answer)

""" 
@app.route('/check_answer', methods=['POST'])
def check_answer():
    #num1 = int(request.form['num1'])
    #num2 = int(request.form['num2'])
    user_answer = int(request.form['user_answer'])
    correct_answer = int(request.form['correct_answer'])

    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])

    global correct_answers
    global total_questions_attempted

    total_questions_attempted += 1

    if user_answer == correct_answer:
        correct_answers += 1
        ii=random.randint(0,len(correct_sounds)-1)
        pygame.mixer.Sound.play(correct_sounds[ii])
        #pygame.mixer.Sound.play(correct_sound)
        return render_template('correct.html', num1=num1, num2=num2, correct_answer=correct_answer)
    else:
        ii=random.randint(0,len(incorrect_sounds)-1)
        pygame.mixer.Sound.play(incorrect_sounds[ii])
        #pygame.mixer.Sound.play(incorrect_sound)
        return render_template('incorrect.html', num1=num1, num2=num2, correct_answer=correct_answer)
"""

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = int(request.form['user_answer'])
    correct_answer = int(request.form['correct_answer'])

    global correct_answers
    global total_questions_attempted

    total_questions_attempted += 1

    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])

    if user_answer == correct_answer:
        correct_answers += 1
        ii=random.randint(0,len(correct_sounds)-1)
        pygame.mixer.Sound.play(correct_sounds[ii])
        #pygame.mixer.Sound.play(correct_sound)
        return render_template('correct.html', num1=num1, num2=num2, correct_answer=correct_answer)
    else:
        ii=random.randint(0,len(incorrect_sounds)-1)
        pygame.mixer.Sound.play(incorrect_sounds[ii])
        #pygame.mixer.Sound.play(incorrect_sound)
        return render_template('incorrect.html', num1=num1, num2=num2, correct_answer=correct_answer)



@app.context_processor
def scoreboard():
    return dict(correct_answers=correct_answers, total_questions_attempted=total_questions_attempted)

if __name__ == '__main__':
    app.run(debug=True)
