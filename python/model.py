import random
import statistics
import json
import sys
import string
from mip import Model, xsum, minimize, BINARY, INTEGER, CONTINUOUS
# Includes COIN-OR Linear Programming Solver - CLP


def runModel(num_teams, team_size, num_students, conflicts, gpas, genders):

    #### MIP MODEL ####
    n = num_students * num_teams

    class_avg = int(round(statistics.mean(gpas), 0))
    gpa_devs = [abs(gpa - class_avg) for gpa in gpas]

    genders_w = [0 for i in range(num_students)]
    for i, gender in enumerate(genders):
        if gender.lower() == "w" or gender.lower() == "x":
            genders_w[i] = 1

    if team_size % 2 != 0:
        team_size_half = team_size // 2 + 1
    else:
        team_size_half = team_size // 2

    m = Model()

    # Decision variables
    x = [m.add_var(var_type=BINARY) for i in range(n)]  # Student i on team j
    xs = [m.add_var(var_type=BINARY) for c in range(
        len(conflicts)*num_teams)]  # Slack var for conflicts
    y = [m.add_var(var_type=INTEGER)
         for i in range(num_teams)]  # Slack var for team size
    # Slack var for total team gpa
    ygpa = [m.add_var(var_type=INTEGER) for i in range(num_teams * 2)]
    z = m.add_var(var_type=INTEGER)  # Sum of team size slack vars

    # GPA constraint decision variables
    ygpad = [m.add_var(var_type=INTEGER) for i in range(num_teams)]
    zgpa = m.add_var(var_type=INTEGER)

    # Gender constraint decision variables
    xwid = [m.add_var(var_type=BINARY) for i in range(num_teams)]

    # Objective function
    m.objective = minimize(100*z + 10000*xsum(xs) +
                           xsum(ygpa) + zgpa + 10*xsum(xwid))

    # Constraint: student can only be selected once
    for i in range(num_students):
        m += xsum(x[num_teams*i + j] for j in range(num_teams)) == 1

    # Constraint: team must be full, gap is team slack value
    for i in range(num_teams):
        m += xsum(x[i + j*num_teams]
                  for j in range(num_students)) + y[i] == team_size

    # Constraint: for each conflict, both people cannot be in the same team
    if (len(conflicts) > 0):
        for i, c in enumerate(conflicts):
            for j in range(num_teams):
                m += x[num_teams*c[0]+j] + x[num_teams*c[1]+j] - xs[i+j] <= 1

    # Constraint: the highest slack value is used in min objective
    for i in range(num_teams):
        m += xsum(x[i + j*num_teams]
                  for j in range(num_students)) + y[i] == team_size

    # Constraint: balance total team gpa to class average
    for i in range(num_teams):
        m += xsum((gpas[j] - class_avg) * x[i + j*num_teams]
                  for j in range(num_students)) + ygpa[i] - ygpa[i + num_teams] == 0

    # Constraint: minimize individual deviation from class average
    for j in range(num_teams):
        m += xsum(gpa_devs[i] * x[j + i*num_teams]
                  for i in range(num_students)) == ygpad[j]

    # Constraint: select largest deviation from average gpa
    for j in range(num_teams):
        m += zgpa >= ygpad[j]

    # Constraint: select largest deviation from team size
    for j in range(num_teams):
        m += z >= y[j]

    # Constraint: if less than half women, punish
    for j in range(num_teams):
        m += team_size_half - xsum(genders_w[i] * x[j + i*num_teams]
                                   for i in range(num_students)) <= 100 * xwid[j]

    # xij
    # yj if going to be all males
    # yj if team is going to be all males
    # cannot isolate x in group of m, cannot count as w on team (x can be minority of women team)
    # if not man, then marginalized

    # sum(marginalized) - if(all men) <= 0 for each team
    # sum(marginalized) + if(all men) >= allman size / 2

    # Run the model
    m.optimize(max_seconds=25)

    m.write('model.lp')

    return({'students': x, 'conflicts': xs})


def generateTeams(data_ids, data_conflicts, num_teams, team_size, num_students):

    print("Generating output")

    print("Deduplicate conflicts")

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

    print("Create gpa vector")

    # Get gpa vector
    gpas = [int(round(float(row[4]))) for row in data_ids]

    print("Create gender vector")

    # Get gender vector
    genders = [row[5] for row in data_ids]

    print("RUN MODEL")

    d_vars = runModel(num_teams, team_size, num_students,
                      conflicts, gpas, genders)

    print("CREATE OUTPUT")

    output = {}

    c_sum = 0
    for c in d_vars['conflicts']:
        if c.x == 1:
            c_sum = c_sum + 1

    if c_sum > 0:
        no_c = True
    else:
        no_c = False

    # Summarize solution
    output['model'] = {}
    output['model']['hasConflicts'] = no_c

    # Create empty teams
    output['teams'] = {}
    for team in range(num_teams):
        output['teams'][team + 1] = {
            'members': []
        }

    # Fill teams with assignments
    for i in range(num_students * num_teams):
        if d_vars['students'][i].x >= 0.99:
            team_number = i - (i//num_teams)*num_teams
            member_id = data_ids[i//num_teams][0]
            output['teams'][team_number + 1]['members'].append(member_id)

    #
    output['people'] = {}
    for i in range(len(data_ids)):
        output['people'][data_ids[i][0]] = {
            'id': data_ids[i][0],
            'firstName': data_ids[i][1],
            'lastName': data_ids[i][2],
            'email': data_ids[i][3],
            'gpa': round(float(data_ids[i][4])),
            'gender': data_ids[i][5],
            'conflicts': []
        }
        for j in range(len(data_conflicts)):
            if data_conflicts[j][0] == data_ids[i][0]:
                output['people'][data_ids[i][0]]['conflicts'].append(
                    data_conflicts[j][3])

    return output


def getTeams():

    print(sys.argv[1])
    print(sys.argv[2])

    data_ids = json.loads(sys.argv[1].replace(
        '\\', '').replace('\r', ''), strict=False)
    data_conflicts = json.loads(sys.argv[2].replace(
        '\\', '').replace('\r', ''), strict=False)

    print(data_ids)
    print(data_conflicts)

    team_size = int(sys.argv[3])
    num_students = len(data_ids)
    num_teams = num_students//team_size + min(1, num_students % team_size)

    output = generateTeams(data_ids, data_conflicts,
                           num_teams, team_size, num_students)

    print("json_result_output")
    print(json.dumps(output))


try:
    getTeams()
except Exception as e:
    print("python_error")
    print(e)
