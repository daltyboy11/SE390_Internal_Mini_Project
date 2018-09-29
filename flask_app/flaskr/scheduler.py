import copy
from utility import *


class Scheduler(object):
    # terms_in_school: [ [W2019, yes], [S2019, no], [F2019, yes] ]
    # max_courses: maximum number of courses student can take every term
    # terms_offered: hash map with a list of courses and what terms they're offered in
    #                {CS348: ["W", "S"]}
    # prereqs: hash map with a list of courses their prerequisites
    #                {CS348: ["CS138", "CS241"]}
    # all_courses: list of courses the student are interested in taking and their prerequisites
    # schedule: a schedule containing courses the student already knows he/she is going to take,
    #           to be filled out with interested_courses
    #           [ [CS138, MATH119], [], [CS241], [] ]
    def __init__(self, terms_in_school, max_courses, terms_offered, prereqs, all_courses, schedule):
        self.terms_in_school = terms_in_school
        self.max_courses = max_courses
        self.terms_offered = terms_offered
        self.prereqs = prereqs
        self.all_courses = all_courses
        self.schedule = schedule

        self.terms = len(terms_in_school)
        # is the first term F, W, S?
        self.first_term = terms_in_school[0][0][:1]

    # returns the array indices of each season
    def map_term_to_index(self):
        k = 0
        if self.first_term == "W":
            k = 1
        elif self.first_term == "S":
            k = 2

        term_order = ["F", "W", "S"]
        term = {"F": [], "W": [], "S": []}
        j = 0
        while True:
            if j >= self.terms:
                break
            term[term_order[k]].append(j)
            k = (k + 1) % 3
            j += 1

        return term

    # takes the courses, and creates a new list that contains all interested courses and the terms
    # they are offered
    def courses_needed(self):
        course_list = []
        for course in self.all_courses:
            course_list.append((course, self.terms_offered[course]))

        return course_list

    # contructs the graph needed to be used to
    def prereq_graph(self):
        adjList = []
        for course, prerequisite in self.prereqs:
            adjList.append((course, prerequisite))

        return adjList

    # gets list of terms on campus represented by indices
    def terms_on_campus(self):
        on_campus = []
        for i in range(len(self.terms_in_school)):
            if terms_in_school[i][1] == "yes":
                on_campus.append(i)

        return on_campus

    # finds the term course is in the schedule, -1 otherwise
    def find_term(self, schedule, course):
        for i in range(schedule):
            for c in schedule[i][1]:
                if c == course:
                    return i

        return -1

    # schedule is a list that looks like [(CS348, [list of prereqs])]
    # courses should be [ [CS348, [W, S] ], ...]
    def scheduler_util(self, schedule, courses):
        course = courses[0][0]  # the current course we want to insert into the schedule
        terms_offered = courses[0][1]  # the seasons the course is offered in

        indices = list(range(self.terms))   # possible terms the course can be scheduled in. Will be further filtered.

        # Remove terms that do not have course
        term_indices = self.map_term_to_index()
        for season in terms_offered:
            indices = filter_in(indices, term_indices[season])

        # Remove terms for which the student is not on campus
        indices = filter_in(indices, self.terms_on_campus())

        # Remove terms for which the courses are maxed out
        for i in indices:
            if len(schedule[i][1]) >= self.max_courses:
                indices.remove(i)

        # find the term the latest prereq is in
        max_prereq_term = -1
        for p in self.prereqs[course]:
            t = self.find_term(schedule, p)
            if t > max_prereq_term:
                max_prereq_term = t

        # remove all terms that are earlier than max_prereq_term
        indices = filter_out(indices, range(max_prereq_term+1))

        if len(indices) == 0:
            return None

        for i in indices:
            cschedule = copy.deepcopy(schedule)
            ccourses = copy.deepcopy(courses)

            # add course into the schedule
            cschedule[i].append(course)
            ccourses.pop(0)

            if len(ccourses) == 0:
                return cschedule

            return self.scheduler_util(cschedule, ccourses)

    # main function that will be called
    def scheduler(self):
        return 0


if __name__ == "__main__":
    print("Hello world")
