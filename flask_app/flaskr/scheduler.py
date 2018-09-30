import utility


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
    def __init__(self, terms_in_school, max_courses, terms_offered, prereqs, schedule):
        self.terms_in_school = terms_in_school
        self.max_courses = max_courses
        self.terms_offered = terms_offered
        self.prereqs = prereqs
        # self.all_courses = all_courses
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
    def wrap_courses(self, sorted_courses):
        course_list = []
        for course in sorted_courses:
            course_list.append((course, self.terms_offered[course]))

        return course_list

    # contructs the graph needed to be used to
    def prereq_graph(self):
        adjList = []
        for course, prerequisite in self.prereqs.items():
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
        for i in range(len(schedule)):
            for c in schedule[i]:
                if c == course:
                    return i

        return -1

    def is_course_taken(self, schedule, course):
        for t in schedule:
            for c in t:
                if course == c:
                    return True

        return False

    # schedule is a list that looks like [ [CS148], [CS238, CS212], ... ]
    # courses should be [ [CS348, [W, S] ], ...]
    def scheduler_util(self, schedule, courses):
        course = courses[0][0]  # the current course we want to insert into the schedule
        terms_offered = courses[0][1]  # the seasons the course is offered in

        if self.is_course_taken(schedule, course):
            ccourse = courses.copy()
            ccourse.pop(0)
            return self.scheduler_util(schedule.copy(), ccourse)

        indices = list(range(self.terms))  # possible terms the course can be scheduled in. Will be further filtered.

        # Remove terms that do not have course
        term_indices = self.map_term_to_index()
        offered_indices = []
        for season in terms_offered:
            offered_indices = offered_indices + term_indices[season]

        indices = utility.filter_in(indices, offered_indices)

        # Remove terms for which the student is not on campus
        toc = self.terms_on_campus()
        indices = utility.filter_in(indices, toc)

        # Remove terms for which the courses are maxed out
        for i in indices:
            if len(schedule[i]) >= self.max_courses:
                indices.remove(i)

        # find the term the latest prereq is in
        max_prereq_term = -1
        for p in self.prereqs[course]:
            t = self.find_term(schedule, p)
            if t > max_prereq_term:
                max_prereq_term = t

        # remove all terms that are earlier than max_prereq_term
        indices = utility.filter_out(indices, range(max_prereq_term + 1))

        if len(indices) == 0:
            return None

        for i in indices:
            cschedule = schedule.copy()
            ccourses = courses.copy()

            # add course into the schedule
            cschedule[i].append(course)
            # remove the first course
            ccourses.pop(0)
            if len(ccourses) == 0:
                return cschedule

            final = self.scheduler_util(cschedule, ccourses)
            if final is not None:
                return final

        return None

    # main function that will be called
    def scheduler(self):
        prereq_list = self.prereq_graph()
        sorted_courses = utility.top_sort(prereq_list)

        sorted_courses = self.wrap_courses(sorted_courses)
        schedule = self.scheduler_util(self.schedule.copy(), sorted_courses)

        return schedule


if __name__ == "__main__":
    terms_in_school = [ ["F2019", "yes"], ["W2019", "yes"], ["S2019", "no"],
                         ["F2020", "yes"], ["W2020", "no"], ["S2020", "yes"],
                        ["F2021", "no"], ["W2021", "yes"], ["S2021", "no"],
                        ["F2021", "yes"], ["W2021", "no"], ["S2021", "yes"],
                        ["F2021", "no"], ["W2021", "yes"], ["S2021", "no"] ]
    max_courses = 10

    prereqs = {
        'CS145': [],
        'CS146': ['CS145'],
        'CS240': ['SE212', 'CS247', 'STAT240'],
        'CS241': ['CS146'],
        'CS247': ['CS241'],
        'CS341': ['CS240', 'MATH249'],
        'MATH119': ['MATH147'],
        'MATH135': [],
        'MATH145': [],
        'MATH146': ['MATH145'],
        'MATH147': [],
        'MATH213': ['MATH119'],
        'MATH249': ['MATH145', 'MATH146'],
        'SE212': ['MATH135'],
        'SE380': ['MATH213'],
        'STAT240': ['MATH147']
    }

    terms_offered = {
        'CS145': ['F'],
        'CS146': ['W'],
        'CS240': ['F', 'W', 'S'],
        'CS241': ['F', 'W', 'S'],
        'CS247': ['S'],
        'CS341': ['F', 'W', 'S'],
        'MATH119': ['W', 'S'],
        'MATH135': ['F', 'W', 'S'],
        'MATH145': ['F'],
        'MATH146': ['W'],
        'MATH147': ['F'],
        'MATH213': ['S'],
        'MATH249': ['F', 'W'],
        'SE212': ['F'],
        'SE380': ['F'],
        'STAT240': ['F']
    }

    schedule = [ ["CS145"], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]

    scheduler = Scheduler(terms_in_school, max_courses, terms_offered, prereqs, schedule)

    print(scheduler.scheduler())
