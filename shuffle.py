import json
import random

with open('questions.txt', 'r') as file:
    questions = json.load(file)

with open('answers.txt', 'r') as file:
    answers = json.load(file)

with open('questions_2.txt', 'r') as file:
    questions2 = json.load(file)

with open('answers_2.txt', 'r') as file:
    answers2 = json.load(file)

selected_numbers = random.sample(range(1, 101), 20)
selected_numbers.sort()  

i = 1
selected_questions = {}
selected_answers = {}
for key in selected_numbers:
    selected_questions[str(i)] = questions[str(key)][0]
    selected_answers[str(i)] = [answers[str(key)][0]]
    i += 1

selected_numbers = random.sample(range(1, 401), 80)
selected_numbers.sort() 
for key in selected_numbers:
    selected_questions[str(i)] = questions2[str(key)]
    selected_answers[str(i)] = [answers2[str(key)][0]]
    i += 1

# Print the resulting dictionary in a pretty JSON format.
# print(selected_questions)
# print(selected_answers)

with open('selected_questions.txt', 'w') as outfile:
    json.dump(selected_questions, outfile, indent=4)

with open('selected_answers.txt', 'w') as outfile:
    json.dump(selected_answers, outfile, indent=4)
