import os
import random

# https://keepass.info/help/base/pwgenerator.html
# wIZpjhqGn6cBovKi6loO - default example
charset_def = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
charset_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
charset_lower = 'abcdefghijklmnopqrstuvwxyz'
charset_number = '0123456789'
charset_special = '!"#$%&()*+,-:;<=>?@^_`'


def generate_default():
    password = ''
    for i in range(20):
        password = password + random.choice(charset_def)
    return password


def generate_comprehensive16():
    password = ''
    password = password + random.choice(charset_upper)
    password = password + random.choice(charset_number)
    password = password + random.choice(charset_special)
    print(len(password))
    print(password)
    for i in range(len(password), 20):
        password = password + random.choice(charset_def + charset_special)
    print(len(password))
    print(password)
    return password


def main():

    with open('./output.txt', 'a+', encoding='utf-8',
              errors='ignore') as outfile:
        for i in range(50000):
            outfile.write(generate_comprehensive16() + '\n')


if __name__ == '__main__':
    main()