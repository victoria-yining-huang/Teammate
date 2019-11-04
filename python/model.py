import random
import statistics
import json
import sys
from mip import Model, xsum, minimize, BINARY, INTEGER, CONTINUOUS
# Includes COIN-OR Linear Programming Solver - CLP


def runModel(num_teams, team_size, num_students, conflicts, gpas):

    #### MIP MODEL ####
    n = num_students * num_teams
    class_avg = int(round(statistics.mean(gpas), 0))
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

    # Objective function
    m.objective = minimize(z + 1000*xsum(xs) + xsum(ygpa))

    # Constraint: student can only be selected once
    for i in range(num_students):
        m += xsum(x[num_teams*i + j] for j in range(num_teams)) == 1

    # Constraint: team must be full, gap is team slack value
    for i in range(num_teams):
        m += xsum(x[i + j*num_teams]
                  for j in range(num_students)) + y[i] == team_size

    # Constraint: for each conflict, both people cannot be in the same team
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

    # Constraint:
    for i in range(num_teams):
        m += z >= y[i]

    # Run the model
    m.optimize()

    return({'students': x, 'conflicts': xs})


def generateTeams(data_ids, data_conflicts, num_teams, team_size, num_students):

    conflicts = []
    ids = [row[2] for row in data_ids]
    for i in range(len(data_conflicts)):
        conflict = [ids.index(data_conflicts[i][0]),
                    ids.index(data_conflicts[i][1])]
        inverse_conflict = [ids.index(data_conflicts[i][1]),
                            ids.index(data_conflicts[i][0])]
        if inverse_conflict not in conflicts:
            conflicts.append(conflict)

    gpas = [row[4] for row in data_ids]

    d_vars = runModel(num_teams, team_size, num_students,
                      conflicts, gpas)

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
            'gpa': data_ids[i][4],
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


def testWithData():
    data_ids = [
        ["A", "A", "a", "email", 55],
        ["B", "B", "b", "email", 60],
        ["C", "C", "c", "email", 50],
        ["D", "D", "d", "email", 70],
        ["E", "E", "e", "email", 70],
        ["F", "F", "f", "email", 75],
        ["G", "G", "g", "email", 75],
        ["H", "H", "h", "email", 75],
        ["I", "I", "i", "email", 75],
        ["J", "J", "j", "email", 75],
        ["K", "K", "k", "email", 75],
        ["L", "L", "l", "email", 75],
        ["M", "M", "m", "email", 70],
        ["N", "N", "n", "email", 100],
        ["O", "O", "o", "email", 90],
        ["P", "P", "p", "email", 90]
    ]

    data_conflicts = [
        ["a", "b"],
        ["b", "a"],
        ["c", "a"],
        ["d", "a"],
        ["e", "a"],
        ["f", "a"]
    ]

    team_size = 4
    num_students = len(data_ids)
    num_teams = num_students//team_size + min(1, num_students % team_size)

    output = generateTeams(data_ids, data_conflicts,
                           num_teams, team_size, num_students)

    #print(json.dumps(output, indent=4))


def testWithGeneratedData(num_students, team_size, num_conflicts):

    num_teams = num_students//team_size + min(1, num_students % team_size)
    conflicts = []

    if num_conflicts > 0:
        for i in range(num_conflicts):
            p = random.randrange(start=0, stop=num_students-1)
            c = random.randrange(start=0, stop=num_students-1)
            conflicts.append([p, c])

    d_vars = runModel(num_teams, team_size, num_students, conflicts)

    # Student-team assignments
    s = []
    for i in range(num_students * num_teams):
        if d_vars['students'][i].x >= 0.99:
            s.append([i//num_teams + 1, i - (i//num_teams)*num_teams + 1])

    sizes = [0 for i in range(num_teams)]
    total = 0
    for student in s:
        total = total + 1
        sizes[student[1] - 1] = sizes[student[1] - 1] + 1

    c_sum = 0
    for c in d_vars['conflicts']:
        if c.x == 1:
            c_sum = c_sum + 1

    if c_sum > 0:
        no_c = True
    else:
        no_c = False

    print("INPUT")
    print("Number of students: ", num_students)
    print("Number of Teams: ", num_teams)
    print("Team Size: ", team_size)
    print("Number of random conflicts: ", num_conflicts)
    print("OUTPUT")
    print("Placed Students: ", len(s))
    print("Team Sizes: ", sizes)
    print("Contains Conflicts: ", no_c)
    print(s)


# testWithGeneratedData(num_students=74, team_size=7, num_conflicts=10)
# testWithData()

try:
    # getTeams()
    testWithData()
except Exception as e:
    print("python_error")
    print(e)
