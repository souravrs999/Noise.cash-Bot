import random

with open('red.txt','r') as f:
    jokes = f.read()

joke = [x.split('\n') for x in jokes]
print(joke)
