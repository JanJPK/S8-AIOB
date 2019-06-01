import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input path')
parser.add_argument('output', help='output path')
parser.add_argument('--count', type=int, default=50000)
args = parser.parse_args()


def main():
    lines = []
    selected_lines = []
    with open(args.input, encoding='utf-8', errors='ignore') as infile:
        for line in infile:
            lines.append(line)

    for i in range(args.count):
        selected_lines.append(random.choice(lines))

    with open(args.output, 'a+', encoding='utf-8') as outfile:
        for selected_line in selected_lines:
            outfile.write(selected_line)


if __name__ == '__main__':
    main()