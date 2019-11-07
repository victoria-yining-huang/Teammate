import random
import statistics
import json
import sys
from mip import Model, xsum, minimize, BINARY, INTEGER, CONTINUOUS
# Includes COIN-OR Linear Programming Solver - CLP


def runModel(num_teams, team_size, num_students, conflicts, gpas, genders):

    #### MIP MODEL ####
    n = num_students * num_teams

    class_avg = int(round(statistics.mean(gpas), 0))
    gpa_devs = [abs(gpa - class_avg) for gpa in gpas]

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

    # Objective function
    m.objective = minimize(100*z + 10000*xsum(xs))

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

    # Constraint: select largest deviation from team size
    for j in range(num_teams):
        m += z >= y[j]

    # Run the model
    m.optimize()

    return({'students': x, 'conflicts': xs})


def generateTeams(data_ids, data_conflicts, num_teams, team_size, num_students):

    print(data_ids)
    print(data_conflicts)

    # Deduplicate conflicts
    conflicts = []
    ids = [row[2] for row in data_ids]
    for i in range(len(data_conflicts)):
        conflict = [ids.index(data_conflicts[i][0]),
                    ids.index(data_conflicts[i][1])]
        inverse_conflict = [ids.index(data_conflicts[i][1]),
                            ids.index(data_conflicts[i][0])]
        if inverse_conflict not in conflicts:
            conflicts.append(conflict)

    # Get gpa vector
    gpas = [int(round(float(row[4]))) for row in data_ids]

    # Get gender vector
    genders = [row[5] for row in data_ids]

    d_vars = runModel(num_teams, team_size, num_students,
                      conflicts, gpas, genders)

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
            member_id = data_ids[i//num_teams][2]
            output['teams'][team_number + 1]['members'].append(member_id)

    #
    output['people'] = {}
    for i in range(len(data_ids)):
        output['people'][data_ids[i][2]] = {
            'id': data_ids[i][2],
            'firstName': data_ids[i][0],
            'lastName': data_ids[i][1],
            'email': data_ids[i][3],
            'gpa': round(float(data_ids[i][4])),
            'gender': data_ids[i][5],
            'conflicts': []
        }
        for j in range(len(data_conflicts)):
            if data_conflicts[j][0] == data_ids[i][2]:
                output['people'][data_ids[i][2]]['conflicts'].append(
                    data_conflicts[j][1])

    return output


def getTeams():

    data_ids = json.loads(sys.argv[1].replace(
        '\\', '').replace('\r', ''), strict=False)
    data_conflicts = json.loads(sys.argv[2].replace(
        '\\', '').replace('\r', ''), strict=False)
    team_size = int(sys.argv[3])
    num_students = len(data_ids)
    num_teams = num_students//team_size + min(1, num_students % team_size)

    output = generateTeams(data_ids, data_conflicts,
                           num_teams, team_size, num_students)

    print("json_result_output")
    print(json.dumps(output))


try:
    # getTeams()
    print("START")
except Exception as e:
    print("python_error")
    print(e)
