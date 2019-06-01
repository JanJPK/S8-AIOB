import os
import json

input_path = '../../resources/passwords/fake/test.txt'
output_path = '../../resources/weir_prep'

lcs_occurence = {}
# { 'structure': { 'terminal': occurence } }
# example:
# {
#   "LL": { "aa": 3, "bb": 1, "cc": 1, "dd": 1, "ee": 1 },
#   "DD": { "11": 3, "22": 1, "33": 1, "55": 1, "66": 1 },
#   "LLLLLL": { "aabbcc": 1 },
#   "DDDD": { "1122": 1, "6666": 1 },
#   "LLLL": { "hhhh": 1 }
# }


def get_structure_char(char):
    if char.isalpha():
        return 'L'
    if char.isdigit():
        return 'D'
    return 'S'


def get_structure(text):
    structure = ''
    for char in text:
        structure += get_structure_char(char)
    return structure


def get_lcs_list(text):
    print(f'lcs list for: {text}')
    previous_structure = get_structure_char(text[0])
    lcs = text[0]
    lcs_list = []
    for char in text[1:]:
        structure_char = get_structure_char(char)
        if structure_char != previous_structure:
            lcs_list.append(lcs)
            lcs = ''
        lcs += char
        previous_structure = structure_char
    lcs_list.append(lcs)
    return lcs_list


# def get_lcs_list(text):
#     print(f'lcs list for: {text}')
#     previous_char = get_structure_char(text[0])
#     lcs = previous_char
#     lcs_list = []
#     for char in text[1:]:
#         structure_char = get_structure_char(char)
#         if structure_char != previous_char:
#             lcs_list.append(lcs)
#             lcs = ''
#         lcs += structure_char
#         previous_char = structure_char
#     print(lcs_list)
#     return lcs_list


def write_terminal(terminal, structure):
    with open(f'{output_path}/{structure}.txt', 'a+',
              encoding='utf-8') as outfile:
        outfile.write(f'{terminal}\n')


def add_lcs_occurence(lcs_list):
    global lcs_occurence
    for lcs in lcs_list:
        lcs_structure = get_structure(lcs)
        if lcs_structure not in lcs_occurence:
            lcs_occurence[lcs_structure] = {lcs: 1}
        elif lcs not in lcs_occurence[lcs_structure]:
            lcs_occurence[lcs_structure][lcs] = 1
        else:
            lcs_occurence[lcs_structure][lcs] += 1


def parse_input_file():
    with open(input_path, encoding='utf-8', errors='ignore') as infile:
        for line in infile:
            terminal = line.strip()
            lcs_list = get_lcs_list(terminal)
            structure = get_structure(terminal)
            write_terminal(terminal, structure)
            add_lcs_occurence(lcs_list)


def write_lcs_occurence():
    global lcs_occurence
    with open(f'{output_path}/lcs.json', 'a+', encoding='utf-8') as outfile:
        outfile.write(json.dumps(lcs_occurence))


def main():
    parse_input_file()
    write_lcs_occurence()


if __name__ == '__main__':
    main()