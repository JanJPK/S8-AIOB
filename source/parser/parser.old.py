import re
import string
import os

regex = '^[!-.0-9?-Z^-z]+$'
#       at least 1 symbol
#       latin letters only
#       numbers
#       some specials
#       ASCII codes allowed: <33,46> + <48,57> + <63,90> + <94, 122>
input_path = 'G:/BreachCompilation/data/'
output_path = '../../resources/passwords/real/'


def parse_file(input_path, output_path):
    with open(output_path, 'a+', encoding='utf-8') as outfile:
        with open(input_path, encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                result = parse_line(line)
                if result is not None:
                    outfile.write(result)


def parse_line(line):
    # dump lines are in format 'email:password'
    i = line.strip().rfind(':')
    if i == -1:
        return None
    line = line[i + 1:]
    if re.match(regex, line) is not None:
        return line
    else:
        return None


def exceeded_output_file_size(path):
    size = os.path.getsize(path)
    size = size / 1000000  # b to mb
    return size > 10


def main():
    # dumps are split into files named 0-9 and a-z (first letter of email)
    namerange = string.digits + string.ascii_lowercase

    output_files_created = 0
    for dirname in namerange:
        for filename in namerange:
            print(f'working on {dirname}-{filename}')
            parse_file(f'{input_path}/{dirname}/{filename}',
                       f'{output_path}/real_{output_files_created}.txt')
            if exceeded_output_file_size(
                    f'{output_path}/real_{output_files_created}.txt'):
                output_files_created += 1


if __name__ == '__main__':
    main()