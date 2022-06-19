import json
import pprint

import code

with open("data.json", "r") as read_file:
    data = json.load(read_file)


def my_main():
    pprint.pprint(code.groups(data))
    # pprint.pprint(code.parse1(10))


if __name__ == '__main__':
    my_main()


