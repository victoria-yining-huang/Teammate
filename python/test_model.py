import unittest
import statistics
import numpy as np
import os
import datetime
from model import generateTeams


def getTestReport(output, data_ids, data_conflicts, num_teams, team_size, test_name):
    num_students = len(data_ids)

    gpas = [int(round(float(row[4]))) for row in data_ids]
    class_avg = round(statistics.mean(gpas))
    sorted_gpas = sorted(gpas)
    bottom_tier = sorted_gpas[0:num_teams]
    top_tier = sorted_gpas[(num_students-num_teams):]

    num_m = [row[5] for row in data_ids].count("m")
    num_w = [row[5] for row in data_ids].count("w")
    num_x = [row[5] for row in data_ids].count("x")

    f.write("\n### {} ###\n".format(test_name))

    f.write("\n## INPUT ##\n")

    f.write("Number of students: {}\n".format(num_students))
    f.write("Genders: {}% men ({}), {}% women ({}), {}% other ({})\n".format(
        round(num_m/num_students*100, 1),
        num_m,
        round(num_w/num_students*100, 1),
        num_w,
        round(num_x/num_students*100, 1),
        num_x,
    ))

    f.write("Average gpa: {}\n".format(class_avg))
    f.write("Bottom tier gpas: {}\n".format(bottom_tier))
    f.write("Top tier gpas: {}\n".format(top_tier))

    f.write("Input team size: {}\n".format(team_size))
    s = 0
    i = 0
    teams = [0 for i in range(num_teams)]
    while s < num_students:
        for i in range(num_teams):
            if s == num_students:
                continue
            else:
                teams[i] = teams[i] + 1
                s = s + 1
    f.write("Expected number of teams: {}\n".format(num_teams))
    f.write("Expected team sizes: {}\n".format(teams))

    f.write("Input number of conflicts: {}\n".format(len(data_conflicts)))
    if (len(data_conflicts) > 0):
        f.write("Conflicts:\n")
        for c in data_conflicts:
            f.write("{} in conflict with {}\n".format(c[0], c[1]))

    f.write("\n## OUTPUT ##\n")

    f.write("\nTeams contain conflicts: {}\n".format(
        output['model']['hasConflicts']))

    # Validate team sizes and conflicts
    f.write("\nteam \tsize \tconflicts \tmembers\n")
    total_conflicts = 0
    team_sizes = []
    for i in range(len(output["teams"])):
        members = output["teams"][i + 1]["members"]
        team_sizes.append(len(members))
        num_conflicts = 0
        for member in members:
            for c in output["people"][member]["conflicts"]:
                if c in members:
                    num_conflicts = num_conflicts + 1
                    total_conflicts = total_conflicts + 1
        f.write("{}\t{}\t{}\t\t{}\n".format(
            i + 1, len(members), num_conflicts, members))
    if sorted(team_sizes) == sorted(teams):
        f.write("Number of teams and team sizes are correct.\n")
    else:
        f.write("Expected team sizes: {}. Produced team sizes: {}.\n".format(
            sorted(teams), sorted(team_sizes)))
    if total_conflicts == 0:
        f.write("No conflicts within teams.\n")
    else:
        f.write("Teams contain {} conflicts.\n".format(total_conflicts))

    # Validate team gpas
    f.write("\nteam \tavg gpa total dev \tbottom tier \ttop tier \tgpas\n")
    for i in range(len(output["teams"])):
        gpas_team = []
        members = output["teams"][i + 1]["members"]
        for member in members:
            gpas_team.append(output["people"][member]["gpa"])
        b = any(elem in gpas for elem in bottom_tier)
        t = any(elem in gpas for elem in top_tier)

        f.write("{}\t{}\t{}\t\t{}\t\t{}\t\t{}\n".format(
            i + 1, "%.1f" % round(statistics.mean(gpas_team)), "%.1f" % round(statistics.stdev(gpas_team)), b, t, sorted(gpas_team)))

    # Validate team genders
    f.write("\nteam \t% men \t% women % other genders\n")
    for i in range(len(output["teams"])):
        genders = []
        gender_counts = {"m": 0, "w": 0, "x": 0}
        members = output["teams"][i + 1]["members"]
        size = len(members)
        for member in members:
            gender = output["people"][member]["gender"]
            genders.append(gender)
            gender_counts[gender] = gender_counts[gender] + 1
        m = int(round(gender_counts["m"]/size, 2)*100)
        w = int(round(gender_counts["w"]/size, 2)*100)
        x = int(round(gender_counts["x"]/size, 2)*100)
        f.write("{}\t{}\t{}\t{}\t{}\n".format(
            i + 1, m, w, x, sorted(genders)))


def runTest(data_ids, data_conflicts, team_size, test_name="Test"):

    num_students = len(data_ids)
    num_teams = num_students//team_size + min(1, num_students % team_size)
    output = generateTeams(data_ids, data_conflicts,
                           num_teams, team_size, num_students)
    getTestReport(output, data_ids, data_conflicts,
                  num_teams, team_size, test_name)


class AverageClass(unittest.TestCase):
    def test(self):
        num_students = 75
        gpa_avg = 75
        gpa_stdev = 10
        prob_m = 0.475
        prob_w = 0.475
        prob_x = 0.05
        num_conflicts = 0
        team_size = 7

        data_ids = buildDataIds(num_students, gpa_avg,
                                gpa_stdev, prob_m, prob_w, prob_x).tolist()

        data_conflicts = buildDataConflicts(data_ids, num_conflicts)

        runTest(data_ids, data_conflicts, team_size,
                test_name="Average Class, no Conflicts")


# class AverageClassWithConflicts(unittest.TestCase):
#     def test(self):
#         num_students = 75
#         gpa_avg = 75
#         gpa_stdev = 10
#         prob_m = 0.475
#         prob_w = 0.475
#         prob_x = 0.05
#         num_conflicts = 15
#         team_size = 7

#         data_ids = buildDataIds(num_students, gpa_avg,
#                                 gpa_stdev, prob_m, prob_w, prob_x).tolist()

#         data_conflicts = buildDataConflicts(data_ids, num_conflicts)

#         runTest(data_ids, data_conflicts, team_size,
#                 test_name="Average Class, several Conflicts")


# class MaleClass(unittest.TestCase):
#     def test(self):
#         num_students = 75
#         gpa_avg = 75
#         gpa_stdev = 10
#         prob_m = 0.8
#         prob_w = 0.175
#         prob_x = 0.025
#         num_conflicts = 15
#         team_size = 10

#         data_ids = buildDataIds(num_students, gpa_avg,
#                                 gpa_stdev, prob_m, prob_w, prob_x).tolist()

#         data_conflicts = buildDataConflicts(data_ids, num_conflicts)

#         runTest(data_ids, data_conflicts, team_size,
#                 test_name="Mostly Male Class, several Conflicts")


# class FemaleClass(unittest.TestCase):
#     def test(self):
#         num_students = 75
#         gpa_avg = 75
#         gpa_stdev = 10
#         prob_m = 0.175
#         prob_w = 0.8
#         prob_x = 0.025
#         num_conflicts = 15
#         team_size = 10

#         data_ids = buildDataIds(num_students, gpa_avg,
#                                 gpa_stdev, prob_m, prob_w, prob_x).tolist()

#         data_conflicts = buildDataConflicts(data_ids, num_conflicts)

#         runTest(data_ids, data_conflicts, team_size,
#                 test_name="Mostly Female Class, several Conflicts")


# class LargeTeams(unittest.TestCase):
#     def test(self):
#         num_students = 75
#         gpa_avg = 75
#         gpa_stdev = 10
#         prob_m = 0.475
#         prob_w = 0.475
#         prob_x = 0.05
#         num_conflicts = 0
#         team_size = 20

#         data_ids = buildDataIds(num_students, gpa_avg,
#                                 gpa_stdev, prob_m, prob_w, prob_x).tolist()

#         data_conflicts = buildDataConflicts(data_ids, num_conflicts)

#         runTest(data_ids, data_conflicts, team_size,
#                 test_name="Large Teams")


# class LargeTeamsWithConflicts(unittest.TestCase):
#     def test(self):
#         num_students = 75
#         gpa_avg = 75
#         gpa_stdev = 10
#         prob_m = 0.475
#         prob_w = 0.475
#         prob_x = 0.05
#         num_conflicts = 300
#         team_size = 20

#         data_ids = buildDataIds(num_students, gpa_avg,
#                                 gpa_stdev, prob_m, prob_w, prob_x).tolist()

#         data_conflicts = buildDataConflicts(data_ids, num_conflicts)

#         runTest(data_ids, data_conflicts, team_size,
#                 test_name="Large Teams with Many Conflicts")


def buildDataIds(num_students, gpa_avg, gpa_stdev, prob_m, prob_w, prob_x):

    first_names = np.random.choice(
        ["a", "b", "c", "d", "e", "f", "g"], size=num_students)

    last_names = np.random.choice(
        ["h", "i", "j", "k", "l", "m", "n"], size=num_students)

    ids = ["id" + str(i) for i in range(1, num_students + 1)]

    emails = ["email" for i in range(1, num_students + 1)]

    genders = np.random.choice(
        ["m", "w", "x"], size=num_students, p=[prob_m, prob_w, prob_x])
    gpas = np.around(np.random.normal(
        gpa_avg, gpa_stdev, size=num_students), 1)

    return(np.column_stack((ids, first_names, last_names,
                            emails, gpas, genders)))


def buildDataConflicts(data_ids, num_conflicts):

    ids = [row[0] for row in data_ids]
    all_possible_conflicts = []
    dedup_all_possible_conflicts = []

    for i in ids:
        for j in ids:
            if i != j:
                all_possible_conflicts.append([i, "", "", j, "", ""])

    for c in all_possible_conflicts:
        if [c[3], c[0]] not in dedup_all_possible_conflicts:
            dedup_all_possible_conflicts.append(c)

    conflict_i = np.random.choice(len(dedup_all_possible_conflicts),
                                  size=num_conflicts, replace=False)

    return([dedup_all_possible_conflicts[i] for i in conflict_i])


if __name__ == '__main__':

    f = open("/Users/irkemp/Google Drive/Waterloo/TERM 3B/MSCI 342/Project/Repository/2019-project-team08/python/tests/log.txt", "w+")

    f.write("teammate Model Tests\n")
    f.write("Date: {}\n\n".format(
        datetime.datetime.now()))

    unittest.main()
    f.close()
