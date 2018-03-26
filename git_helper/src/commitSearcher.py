import sys


def print_commit(commit):
    print "\033[40;33m{}\033[0m".format(commit[0])
    for i in range(1, len(commit)):
        print commit[i]


if __name__ == '__main__':
    assert len(sys.argv) == 2
    keyword = sys.argv[1]
    commit = list()
    act_findout = False
    while True:
        try:
            line = raw_input()
        except EOFError:
            break

        if line.find("commit ") != -1 and len(line) == 47:
            if act_findout == True:
                print_commit(commit)
            act_findout = False
            commit = [line]
        else:
            if line.find(keyword) != -1:
                act_findout = True
            commit.append(line)
