import random

while True:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password = ''
    length = input('Input length of the password')
    length = int(length)
    if length == 0:
        print('goodbye')
        exit()
    else:
        for c in range(length):
            password += random.choice(chars)
        print(password)





