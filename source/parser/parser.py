import re
import string
import os

#       '^[!-.0-9?-Z^-z]+$'
#       at least 1 symbol
#       latin letters only
#       numbers
#       some specials
#       ASCII codes allowed: <33,46> + <48,57> + <63,90> + <94, 122>
input_path = 'G:/BreachCompilation/data/'
output_path = '../../resources/passwords/real'
raw_passwords = [[], 0]
comprehensive8_passwords = [[], 0]
regular8_passwords = [[], 0]
passwords_per_file = 1000000


def parse_file(input_path):
    with open(input_path, encoding='utf-8', errors='ignore') as infile:
        for line in infile:
            password = parse_line(line)
            if password is not None:
                filter_password(password)


def parse_line(line):
    # dump lines are in format 'email:password'
    i = line.strip().rfind(':')
    if i == -1:
        return None
    line = line[i + 1:]
    if re.match('^[!-.0-9?-Z^-z]+$', line) is not None:
        return line
    else:
        return None


def filter_password(password):
    global raw_passwords
    global comprehensive8_passwords
    raw_passwords[0].append(password)
    if (len(password) >= 8):
        regular8_passwords[0].append(password)
        # !@#$%^&*()-_=+[]{};’:”,./<>?
        if re.search('[0-9]', password) is None:
            return
        if re.search('[A-Z]', password) is None:
            return
        if re.search('[!@#$%^&*\-_=+’”,\/.?]', password) is None:
            return
        comprehensive8_passwords[0].append(password)


def count_lines_in_file(file):
    return sum(1 for _ in file)


# probably can be pythonized and improved a lot
def write_passwords(filename, passwords):
    print(f'saving {filename} {len(passwords[0])} {passwords[1]}')
    if len(passwords[0]) < 1:
        return

    outfile = open(f'{output_path}/{filename}_{passwords[1]}.txt',
                   'a+',
                   encoding='utf-8')
    outfile.seek(0)

    lines = 0
    for line in outfile:
        lines += 1
    if lines >= passwords_per_file:
        passwords[1] += 1
        outfile.close()
        write_passwords(filename, passwords)
        return

    for i in range(passwords_per_file - lines):
        if len(passwords[0]) < 1:
            return
        outfile.write(passwords[0].pop())

    if len(passwords[0]) > 0:
        outfile.close()
        write_passwords(filename, passwords)


def main():
    # dumps are split into files named 0-9 and a-z (first letter of email)
    namerange = string.digits + string.ascii_lowercase

    parse_file(f'{input_path}/0/00')
    write_passwords('raw', raw_passwords)
    write_passwords('comprehensive8', comprehensive8_passwords)
    write_passwords('regular8', regular8_passwords)
    return

    for dirname in namerange:
        for filename in namerange:
            print(f'working on {dirname}-{filename}')
            parse_file(f'{input_path}/{dirname}/{filename}')
            write_passwords('raw', raw_passwords)
            write_passwords('comprehensive8', comprehensive8_passwords)


if __name__ == '__main__':
    main()