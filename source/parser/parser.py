import re
import string
from os import listdir
from os.path import isfile, join

#       '^[!-.0-9?-Z^-z]+$'
#       at least 1 symbol
#       latin letters only
#       numbers
#       some specials
#       ASCII codes allowed: <33,46> + <48,57> + <63,90> + <94, 122>
input_path = 'G:/BreachCompilation/data'
output_path = 'G:/BreachCompilation/real'
#output_path = '../../resources/passwords/real'
raw_passwords = [[], 0]
regular8_passwords = [[], 0]
regular16_passwords = [[], 0]
#nospecial8_passwords = [[], 0]
comprehensive8_passwords = [[], 0]
comprehensive16_passwords = [[], 0]
passwords_per_file = 500000


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


# old method
#def filter_password(password):
#    global raw_passwords
#    global regular8_passwords
#    #global nospecial8_passwords
#    global comprehensive8_passwords
#    raw_passwords[0].append(password)
#    if (len(password.strip()) >= 8):
#        regular8_passwords[0].append(password)
#        # !@#$%^&*()-_=+[]{};’:”,./<>?
#        if re.search('[0-9]', password) is None:
#            return
#        if re.search('[A-Z]', password) is None:
#            return
#        if re.search('[!@#$%^&*\-_=+’”,\/.?]', password) is None:
#            return
#        comprehensive8_passwords[0].append(password)


# quick shitpatch to get 16s
def filter_password(password):
    global regular16_passwords
    global comprehensive16_passwords
    if (len(password.strip()) >= 16):
        regular16_passwords[0].append(password)
        # !@#$%^&*()-_=+[]{};’:”,./<>?
        if re.search('[0-9]', password) is None:
            return
        if re.search('[A-Z]', password) is None:
            return
        if re.search('[!@#$%^&*\-_=+’”,\/.?]', password) is None:
            return
        comprehensive16_passwords[0].append(password)


def count_lines_in_file(file):
    return sum(1 for _ in file)


# probably can be pythonized and improved a lot
def write_passwords(filename, passwords):
    print(f'saving {filename}: {len(passwords[0])} (file-{passwords[1]})')
    if len(passwords[0]) < 1:
        return

    outfile = open(f'{output_path}/{filename}/{filename}_{passwords[1]}.txt',
                   'a+',
                   encoding='utf-8')
    outfile.seek(0)

    lines = 0
    for line in outfile:
        lines += 1
    if lines >= passwords_per_file:
        print(f'file full, creating new')
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


def parse_directory(dir_path):
    print(f'working on {dir_path}...')
    contents = listdir(dir_path)
    for content in contents:
        content_path = join(dir_path, content)
        if isfile(content_path):
            parse_file(content_path)
        else:
            print(f'nested folder {content_path}')
            parse_directory(content_path)
        #write_passwords('raw', raw_passwords)
        write_passwords('regular16', regular16_passwords)
        write_passwords('comprehensive16', comprehensive16_passwords)


def main():
    # dumps are split into files named 0-9 and a-z (first letter of email)
    namerange = string.digits + string.ascii_lowercase
    namerange2 = string.ascii_lowercase

    for dirname in namerange:
        parse_directory(f'{input_path}/{dirname}')

    # for dirname in namerange2:
    #     for filename in namerange:
    #         print(f'working on {dirname}-{filename}')
    #         if os.path.isfile(f'{input_path}/{dirname}/{filename}'):
    #             parse_file(f'{input_path}/{dirname}/{filename}')
    #         else:
    #             print(f'{dirname}-{filename}: nested directory detected')
    #             for nested_filename in namerange:
    #                 parse_file(
    #                     f'{input_path}/{dirname}/{filename}/{nested_filename}')

    #         write_passwords('raw', raw_passwords)
    #         write_passwords('regular8', regular8_passwords)
    #         #write_passwords('nospecial8', nospecial8_passwords)
    #         write_passwords('comprehensive8', comprehensive8_passwords)


if __name__ == '__main__':
    main()