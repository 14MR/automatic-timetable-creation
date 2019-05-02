import random
import json


# genetic alg accepts as input number of courses (in our case it is 50 just for our course), the courses, population size which is number of scjedulesa passed to the funcitons
# the timeslots, auditoriums and maximum number of iterations for the algprothms, elicistism

def mutate(schedule, number_of_courses, timeslots):
    sched = schedule[:]
    time = timeslots[random.randrange(0, len(timeslots))]
    #     room = auditoriums[random.randrange(0, len(auditoriums))]
    course = random.randrange(0, number_of_courses)

    sched[course * 2] = time
    #     sched[course * 2 + 1][''] = room

    return sched


def fitness(population, population_size, number_of_courses):
    fit = []
    for i in range(0, population_size):
        afit = 0
        curr_chromosome = i * number_of_courses * 2  # number of courses is 51, each chromosome starts at position i out of 100 and each ith has 51 course with 1 timeslot each, so i*2*num_of_courses overall
        #         print(curr_chromosome)
        for j in range(0, number_of_courses,
                       2):  # each first is the timeslot suggested, each second is a dict with preferences information
            requested_time_and_room = 2  # cost if both match
            requested_time_and_prof = 2  # cost if both match
            #             requested_room = 0  # cost if only one matches
            requested_time = 0
            requested_room_size = 1  # cost if room size matches

            temp_time = population[curr_chromosome + j]  # next timeslot
            #             temp_room = population[curr_chromosome + j][]  # next room
            temp_prof = population[curr_chromosome + j + 1]['teacher_id']  # next professor

            #             for k in range(0, len(population[curr_chromosome + j + 5])):  # if requested room matches
            #                 if (population[curr_chromosome + j + 5][k] == temp_room):
            #                     requested_room = 1
            #                     break

            #             print(population[curr_chromosome + j+1]['timespaceslots'][0]['slot_id'])
            for k in range(0, len(population[curr_chromosome + j + 1]['timespaceslots'])):
                if (population[curr_chromosome + j + 1]['timespaceslots'][k][
                    'slot_id'] == temp_time):  # if requested time matches
                    requested_time = 1
                    break

            for k in range(j + 2, number_of_courses * 2, 2):
                #                 if (temp_time == population[curr_chromosome + k]) and (
                #                         temp_room == population[curr_chromosome + k + 1]):  # if both match - the cost is minimal
                #                     requested_time_and_room = 0
                if (temp_time == population[curr_chromosome + k]) and (
                        temp_prof == population[curr_chromosome + k + 1]['teacher_id']):
                    requested_time_and_prof = 0

            afit += requested_time_and_prof + requested_time + requested_room_size
        fit.append(afit)
    return fit


def genetic(number_of_courses, courses, population_size, timeslots,
            max_iterations):  # non-elite version is used, since it allows more variation
    population = []
    #     print(courses)
    #     print(population_size) #population size is 100, there are 100 samples of table
    #     print(number_of_courses)
    for i in range(0, population_size):  # population is an instance of the schedule
        for j in range(0, number_of_courses):  # chromosomes are tuples of type: proposed timespace slot and a requested
            population.append(timeslots[random.randrange(0, len(
                timeslots))])  # for each schedule (100 of them) there are 51 such tuples
            population.append(
                courses[j])  # the population array looks like: [ts, {a row of course with preferences}, ts, {}, ts, {}]
    #     print(population)
    #     print(len(population))
    # population now is a list of 100 of such tuples [ts, {a row of course with preferences}, ts, {}, ts, {}], each 102th is the starting point
    #     print(population)
    fit = fitness(population, population_size, number_of_courses)  # calculating the fitness function

    i = 0  # iterations count
    while (i < max_iterations) and ((float(max(fit)) / (number_of_courses * 7)) < 0.9):  # at least 90 percent of fit
        new_population = []
        top_indices = []
        temp_population = []
        temp_fit = fit[:]
        to_pull = fit[:]

        to_pull.sort()  # sorting the array of fits
        to_pull = to_pull[
                  (len(to_pull) - int(0.1 * len(to_pull))):len(to_pull)]  # leave 10% (the most fitting 10 percent)
        for j in range(0, len(to_pull)):
            top_indices.append(temp_fit.index(to_pull[j]))
            temp_fit[top_indices[j]] = 0
            temp_population += population[top_indices[j] * 2 * number_of_courses:(top_indices[
                                                                                      j] * 2 * number_of_courses) + 2 * number_of_courses]

        for j in range(0, population_size):
            first_choice = random.randrange(0, population_size)
            second_choice = random.randrange(0, population_size)
            if fit[first_choice] > fit[second_choice]:
                dominant = first_choice
            else:
                dominant = second_choice

            dominant = population[(dominant * number_of_courses * 2):(
                    (dominant * number_of_courses * 2) + (number_of_courses * 2))]

            to_reproduce = random.random()

            if to_reproduce < 0.15:
                child = mutate(dominant, number_of_courses, timeslots)
            else:
                to_reproduce = random.randrange(0, 3)
                #                 if to_reproduce == 0:
                #                     child = swap_rooms(dominant, auditoriums)
                if to_reproduce == 1:
                    child = swap_timeslots(dominant, timeslots)
                else:
                    child = change_timeslot(dominant, number_of_courses, timeslots)

            if fitness(child, 1, number_of_courses)[0] > fitness(dominant, 1, number_of_courses)[0]:
                new_population += child
            else:
                new_population += dominant

        population = new_population[:]
        fit = fitness(population, population_size, number_of_courses)
        i += 1
        print(f'Iteration #{i}, fitness is {(float(max(fit)) / (number_of_courses * 7))}')


    max_index = fit.index(max(fit))
    return population[2 * max_index:2 * max_index + 2 * number_of_courses]


def swap_timeslots(schedule, timeslots):
    sched = schedule[:]
    first_timeslot = timeslots[random.randrange(0, len(timeslots))]
    second_timeslot = timeslots[random.randrange(0, len(timeslots))]
    for i in range(0, len(sched), 2):
        if sched[i] == first_timeslot:
            sched[i] = second_timeslot
        elif sched[i] == second_timeslot:
            sched[i] = first_timeslot

    return sched


def change_timeslot(schedule, num_of_courses, timeslots):
    sched = schedule[:]
    timeslot = timeslots[random.randrange(0, len(timeslots))]
    course = random.randrange(0, num_of_courses)

    sched[course * 2] = timeslot

    return sched


# this is not a real data, just a generated one (for demonstartion purposes)
def generate(final, times, import_to_csv=True):
    courses = list(range(1, 5))
    profs = list(range(1, 19))
    # times = list(range(1, 559))

    # final = json.loads(final)
    #         print(final)

    res = genetic(len(final), final, 100, times, 1000)
    print(res)
    timetable_to_json(res)
    if import_to_csv:
        timetable_to_csv(res)  # for debug

    arr = []
    for i in range(1, len(res), 2):
        arr.append({
            **res[i],
            "timespaceslot_id": res[i-1]
        })

    return arr


def timetable_to_csv(course):
    import csv

    with open('results_table.csv', mode='w') as csv_file:
        fieldnames = ['time', 'course', 'professor', 'req_time', 'groups']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0, len(course), 2):
            writer.writerow({'time': str(course[i]), 'course': str(course[i + 1]['course_id']),
                             'professor': str(course[i + 1]['teacher_id']),
                             'req_time': str(course[i + 1]['timespaceslots']),
                             'groups': str(course[i + 1]['groups_ids'])})


def timetable_to_json(course):
    import json
    with open('results.json', 'w') as f:  # writing JSON object
        jstr = json.dumps(course, indent=4)
        f.write(jstr)

