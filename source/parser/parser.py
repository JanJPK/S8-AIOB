def main():
    counter = 0
    #with open("./test_data/input.txt") as infile:
    with open("../../pwned/pwned-passwords-sha1-ordered-by-count-v4.txt"
              ) as infile:
        for line in infile:
            counter += 1
            if (counter > 100):
                return
            print(line.strip())


if __name__ == '__main__':
    main()