def filter_in(l1, l2):
    return [x for x in l1 if x in l2]


def filter_out(l1, l2):
    return [x for x in l1 if x not in l2]


def find_index(adj_list, s):
    for i in range(len(adj_list)):
        if adj_list[i][0] == s:
            return i

    return -1


# prereq_chart: [[CS348, [...]], [CS138, [...], ]
def top_sort_util(prereq_chart, v, visited, stack):
    visited[v] = True

    for s in prereq_chart[v][1]:
        i = find_index(prereq_chart, s)
        if not visited[i]:
            top_sort_util(prereq_chart, i, visited, stack)

    stack.insert(0, v)


def top_sort(prereq_chart):
    num_courses = len(prereq_chart)
    visited = [False] * num_courses
    stack = []

    for i in range(num_courses):
        if not visited[i]:
            top_sort_util(prereq_chart, i, visited, stack)

    return stack
