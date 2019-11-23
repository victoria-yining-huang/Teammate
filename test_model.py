import unittest
import statistics
import numpy as np
import os
import datetime
import math
from model import run_model


def getTestReport(output, data_ids, data_conflicts, num_teams, team_size, test_name):
    num_students = len(data_ids)

    gpas = [int(round(float(row[4]))) for row in data_ids]
    class_avg = round(statistics.mean(gpas))
    sorted_gpas = sorted(gpas)

    num_tiers = math.ceil(num_students / num_teams)
    tier_size = num_teams
    tiers = []
    for i in range(num_tiers):
        tiers.append([])
        for j in range(tier_size):
            if (i*tier_size + j) < num_students:
                tiers[i].append(sorted_gpas[i*tier_size + j])

    bottom_tier = sorted_gpas[0:num_teams]
    top_tier = sorted_gpas[(num_students-num_teams):]

    f.write("\n### {} ###\n".format(test_name))

    f.write("\n## INPUT ##\n")

    f.write("Number of students: {}\n".format(num_students))

    f.write("Average gpa: {}\n".format(class_avg))
    f.write("Bottom tier gpas: {}\n".format(bottom_tier))
    f.write("Top tier gpas: {}\n".format(top_tier))
    for i in range(len(tiers)):
        f.write("Tier {}: {}\n".format(i + 1, tiers[i]))

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

        f.write("Team {} GPA Tiers\n".format(i + 1))
        for j in range(len(tiers)):
            if (any(elem in gpas_team for elem in tiers[j])):
                f.write("Contains tier {}\n".format(j + 1))
            else:
                f.write("Missing tier {}\n".format(j + 1))

        f.write("{}\t{}\t{}\t\t{}\t\t{}\t\t{}\n".format(
            i + 1, "%.1f" % round(statistics.mean(gpas_team)), "%.1f" % round(statistics.stdev(gpas_team)), b, t, sorted(gpas_team)))


def runTest(data_ids, data_conflicts, team_size, test_name="Test"):

    # Calculate number of students and teams
    num_students = len(data_ids)
    num_teams = num_students//team_size + min(1, num_students % team_size)

    # Deduplicate conflicts
    conflicts = []
    ids = [row[0] for row in data_ids]
    for i in range(len(data_conflicts)):
        conflict = [ids.index(data_conflicts[i][0]),
                    ids.index(data_conflicts[i][3])]
        inverse_conflict = [ids.index(data_conflicts[i][3]),
                            ids.index(data_conflicts[i][0])]
        if inverse_conflict not in conflicts:
            conflicts.append(conflict)

    # Get gpa vector
    gpas = [int(round(float(row[4]))) for row in data_ids]

    # Run model
    raw_output = run_model(num_students, num_teams,
                           team_size, conflicts, gpas)

    output = {
        "model": {
            "hasConflicts": raw_output["hasConflicts"]
        }
    }

    # Create empty teams
    output['teams'] = {}
    for team in range(num_teams):
        output['teams'][team + 1] = {
            'members': []
        }

    # Fill teams with assignments
    for i, a in enumerate(raw_output["assignments"]):
        output['teams'][a + 1]["members"].append(data_ids[i][0])

    # Create people
    output['people'] = {}
    for i in range(len(data_ids)):
        output['people'][data_ids[i][0]] = {
            'id': data_ids[i][0],
            'firstName': data_ids[i][1],
            'lastName': data_ids[i][2],
            'email': data_ids[i][3],
            'gpa': round(float(data_ids[i][4])),
            'conflicts': []
        }
        for j in range(len(data_conflicts)):
            if data_conflicts[j][0] == data_ids[i][0]:
                output['people'][data_ids[i][0]]['conflicts'].append(
                    data_conflicts[j][3])

    # Create test report file
    getTestReport(output, data_ids, data_conflicts,
                  num_teams, team_size, test_name)


class AverageClass(unittest.TestCase):
    def test(self):
        num_students = 60
        gpa_avg = 75
        gpa_stdev = 10
        num_conflicts = 0
        team_size = 6

        data_ids = buildDataIds(num_students, gpa_avg, gpa_stdev).tolist()

        data_conflicts = buildDataConflicts(data_ids, num_conflicts)

        runTest(data_ids, data_conflicts, team_size,
                test_name="Average Class, no Conflicts")


def buildDataIds(num_students, gpa_avg, gpa_stdev):

    first_names = np.random.choice(
        ["a", "b", "c", "d", "e", "f", "g"], size=num_students)

    last_names = np.random.choice(
        ["h", "i", "j", "k", "l", "m", "n"], size=num_students)

    ids = ["id" + str(i) for i in range(1, num_students + 1)]

    emails = ["email" for i in range(1, num_students + 1)]

    gpas = np.around(np.random.normal(
        gpa_avg, gpa_stdev, size=num_students), 1)

    return(np.column_stack((ids, first_names, last_names,
                            emails, gpas)))


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

    f = open("/Users/irkemp/Google Drive/Waterloo/TERM 3B/MSCI 342/Project/Repository/2019-project-team08/log.txt", "w+")

    f.write("teammate Model Tests\n")
    f.write("Date: {}\n\n".format(
        datetime.datetime.now()))

    unittest.main()
    f.close()
