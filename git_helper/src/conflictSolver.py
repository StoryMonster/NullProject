import sys
from collections import namedtuple


conflict_prefix = "<<<<<<< HEAD"
conflict_suffix = ">>>>>>> "
solution_prefix = "##==>>>"
solution_suffix = "##<<<=="
conflict_indicator = "CONFLICT "
Solution = namedtuple('Solution', ['file', 'start_line', 'end_line', 'content'])
Conflict = namedtuple('Conflict', ['file', 'start_line', 'end_line', 'content'])
conflict_file = "conflicts.txt"

Conflict.__str__ = lambda conflict : \
"""
{solution_prefix} {file} : {start_line}
{content}
{solution_suffix} {file} : {end_line}"""\
.format(file=conflict.file, start_line=conflict.start_line, end_line=conflict.end_line,
        content=''.join(conflict.content), solution_prefix=solution_prefix, solution_suffix=solution_suffix)


def extract_conflict_files():
    conflict_files = list()
    while True:
        try:
            line = raw_input()
            print line
            if -1 != line.find(conflict_indicator):
                conflict_files.append(line.split()[-1])
        except EOFError:
            return conflict_files


def extract_conflicts_in_file(file):
    conflicts = list()
    with open(file, "r") as fd:
        start_line, end_line, line_counter, content, act_record_conflict = 0, 0, 0, list(), False
        for line in fd:
            line_counter += 1
            if act_record_conflict == False and line.find(conflict_prefix) != -1:
                act_record_conflict = True
                start_line = line_counter
                content.append(line)
            elif act_record_conflict == True and -1 != line.find(conflict_suffix):
                act_record_conflict = False
                end_line = line_counter
                content.append(line.rstrip('\n'))
                conflicts.append(Conflict(file, start_line, end_line, content))
                content = []
            elif act_record_conflict == True:
                content.append(line)
            else: pass
    return conflicts


def show_conflicts():
    conflict_files = extract_conflict_files()
    conflicts = list()
    for file in conflict_files:
        conflicts += extract_conflicts_in_file(file)
    if len(conflicts) == 0: return
    with open(conflict_file, "w") as fd:
        for conflict in conflicts:
            fd.write(conflict.__str__())
    print "\033[40;32mAll conflicts save in file {}\033[0m".format(conflict_file)


def extract_solutions_in_file(file):
    file_name, start_line, end_line, content, solutions = '', 0, 0, list(), list()
    with open(file, "r") as fd:
        act_get_one_solution = False
        for line in fd:
            if act_get_one_solution == False and -1 != line.find(solution_prefix):
                act_get_one_solution = True
                lst = line.split()
                file_name = lst[1]
                start_line = int(lst[-1])
            elif act_get_one_solution == True and -1 != line.find(solution_suffix):
                act_get_one_solution = False
                lst = line.split()
                end_line = int(lst[-1])
                if file_name == lst[1]:
                    solutions.append(Solution(file_name, start_line, end_line, content))
                content = []
            elif act_get_one_solution == True:
                content.append(line)
            else: pass
    return solutions


def sort_solutions(solutions):
    table = dict()
    sorted = list()
    for solution in solutions:
        if table.has_key(solution[0]):
            for i in range(0, len(table[solution[0]])):
                if int(solution[1]) > int(table[solution[0]][i][2]):
                    table[solution[0]].insert(i, solution)
        else:
           table[solution[0]] = [solution]
    for key in table.keys():
        sorted += table[key]
    return sorted


def apply_solutions(file):
    solutions = extract_solutions_in_file(file)
    for solution in sort_solutions(solutions):
        file, start_line, end_line, content = solution[:]
        lines = list()
        with open(file, "r") as fd:
            line_counter = 0
            act_apply_solution = False
            for line in fd:
                line_counter += 1
                if act_apply_solution == False and line_counter == start_line:
                    act_apply_solution = True
                    lines += content
                elif act_apply_solution == True and line_counter == end_line:
                    act_apply_solution = False
                elif act_apply_solution == False:
                    lines.append(line)
                else: pass
        with open(file, "w") as fd:
            for line in lines:
                fd.write(line)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "--apply":
        apply_solutions(conflict_file)
    elif len(sys.argv) == 3 and sys.argv[1] == "--apply":
        apply_solutions(sys.argv[2])
    elif len(sys.argv) == 1:
        show_conflicts()
    else:
        print "Error: Unknow action"
