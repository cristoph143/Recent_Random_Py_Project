class hi:
    def __init__(self,left,right,root):
        left = left
        right = right
        root = root
        
    def is_empty_root(name):
        print('hello world' + name)
        
        
        
'''temp = eval(input('Enter a temperature in Celsius: '))
print('In Fahrenheit, that is', 9/5*temp+32)

for i in range(1,10):
    if i < 10:
        print(i , 'Your Name -- ', i*i, '    -- ', ' * ' *i)
    else:
        print(i , 'Your Name -- ', i*i, ' -- ', ' * ' *i)

print(''.join([chr(i) for i in range(1000)]))


 
class inputted:
    def __init__(self,first_num,second_num,operator):
        first_num = first_num
        second_num = second_num
        operator = operator    


first_num = float(input())
second_num = float(input())
oper = input()
calc(first_num,second_num,oper)
    
def calc(first_num,second_num,operator):
    if operator in "/, mod, div" and second_num == 0:
        print("Division by 0!")
    elif operator == '+':
        print(first_num ,' + ', second_num, first_num + second_num)
    elif operator == '-':
        print(first_num ,' - ', second_num, first_num - second_num)
    elif operator == '/':
        print(first_num ,' / ', second_num, first_num / second_num)
    elif operator == 'div':
        print(first_num ,' div ', second_num, first_num // second_num)
    elif operator == '*':
        print(first_num ,' * ', second_num, first_num * second_num)
    elif operator == 'mod':
        print(first_num ,' mod ', second_num, first_num % second_num)
    elif operator == 'pow':
        print(first_num ,' pow ', second_num, first_num ** second_num)
    else:
        print("Invalid Operation!")
        


num = eval(input('Enter a number: '))
print(num)
'''

from random import shuffle
word = input('Enter a word: ')
letter_list = list(word)
print(letter_list)
shuffle(letter_list)
anagram = ''.join(letter_list)
print(anagram)