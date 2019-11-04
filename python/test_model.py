import unittest
import statistics
import os
from model import generateTeams


def getTestReport(output, data_ids, data_conflicts, num_teams, team_size):

    num_students = len(data_ids)
    class_avg = round(statistics.mean([row[4] for row in data_ids]), 1)
    sorted_gpas = sorted([row[4] for row in data_ids])
    bottom_tier = sorted_gpas[0:num_teams]
    top_tier = sorted_gpas[(num_students-num_teams):]
    num_m = [row[5] for row in data_ids].count("m")
    num_w = [row[5] for row in data_ids].count("w")
    num_x = [row[5] for row in data_ids].count("x")

    f = open("/Users/irkemp/Google Drive/Waterloo/TERM 3B/MSCI 342/Project/Repository/2019-project-team08/python/tests/log.txt", "w+")
    f.write("teammate Model Tests\n\n")

    f.write("### Test ###\n")

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

    f.write("\n## OUTPUT ##\n")

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
        f.write("{}\t\t{}\t\t{}\t\t\t{}\n".format(
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
    f.write("\nteam \tavg gpa \tbottom tier \ttop tier \tgpas\n")
    for i in range(len(output["teams"])):
        gpas = []
        members = output["teams"][i + 1]["members"]
        for member in members:
            gpas.append(output["people"][member]["gpa"])
        b = any(elem in gpas for elem in bottom_tier)
        t = any(elem in gpas for elem in top_tier)

        f.write("{}\t\t{}\t\t{}\t\t\t{}\t\t{}\n".format(
            i + 1, "%.1f" % round(statistics.mean(gpas), 1), b, t, sorted(gpas)))

    # Validate team genders
    f.write("\nteam \t% men \t% women \t% other \tgenders\n")
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
        f.write("{}\t\t{}\t\t{}\t\t\t{}\t\t\t{}\n".format(
            i + 1, m, w, x, sorted(genders)))

    f.close()


class MyTest(unittest.TestCase):
    def test(self):

        data_ids = [
            ["A", "A", "a", "email", 55, "m"],
            ["B", "B", "b", "email", 60, "x"],
            ["C", "C", "c", "email", 50, "m"],
            ["D", "D", "d", "email", 65, "w"],
            ["E", "E", "e", "email", 70, "m"],
            ["F", "F", "f", "email", 75, "m"],
            ["G", "G", "g", "email", 75, "w"],
            ["H", "H", "h", "email", 75, "w"],
            ["I", "I", "i", "email", 75, "m"],
            ["J", "J", "j", "email", 75, "m"],
            ["K", "K", "k", "email", 75, "m"],
            ["L", "L", "l", "email", 75, "w"],
            ["M", "M", "m", "email", 70, "m"],
            ["N", "N", "n", "email", 99, "x"],
            ["O", "O", "o", "email", 95, "m"],
            ["P", "P", "p", "email", 90, "w"]
        ]

        data_conflicts = [
            ["a", "b"],
            ["b", "a"],
            ["c", "a"],
            ["d", "a"],
            ["e", "a"],
            ["f", "a"]
        ]

        team_size = 3
        num_students = len(data_ids)
        num_teams = num_students//team_size + min(1, num_students % team_size)

        output = generateTeams(data_ids, data_conflicts,
                               num_teams, team_size, num_students)

        getTestReport(output, data_ids, data_conflicts, num_teams, team_size)


if __name__ == '__main__':
    unittest.main()
