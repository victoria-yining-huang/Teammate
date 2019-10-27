import random
import json
import sys
from mip import Model, xsum, minimize, BINARY, INTEGER
# Includes COIN-OR Linear Programming Solver - CLP


def runModel(num_teams, team_size, num_students, conflicts):

    #### MIP MODEL ####

    n = num_students * num_teams
    m = Model()

    # Decision variables
    x = [m.add_var(var_type=BINARY) for i in range(n)]
    xs = [m.add_var(var_type=BINARY) for c in range(len(conflicts)*num_teams)]
    y = [m.add_var(var_type=INTEGER) for i in range(num_teams)]
    z = m.add_var(var_type=INTEGER)

    # Objective function
    m.objective = minimize(z + 1000*xsum(xs))

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
            m += x[team_size*c[0]+j] + x[team_size*c[1]+j] - xs[i+j] <= 1

    # Constraint: the highest slack value is used in min objective
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

    d_vars = runModel(num_teams, team_size, num_students, conflicts)

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
        ["John", "Smith", "jsmith1", "jsmith1@uwaterloo.ca"],
        ["Jane", "Doe", "jdoe2", "jdoe2@uwaterloo.ca"],
        ["Kelly", "Brown", "kbrown3", "kbrown3@uwaterloo.ca"],
        ["Mike", "Lee", "mlee4", "mlee4@uwaterloo.ca"]
    ]

    data_conflicts = [
        ["jsmith1", "jdoe2"],
        ["kbrown3", "mlee4"],
        ["kbrown3", "jsmith1"],
        ["kbrown3", "jdoe2"],
        ["jdoe2", "jsmith1"],
        ["jdoe2", "kbrown3"],
        ["jdoe2", "mlee4"]
    ]

    team_size = 2
    num_students = len(data_ids)
    num_teams = num_students//team_size + min(1, num_students % team_size)

    output = generateTeams(data_ids, data_conflicts,
                           num_teams, team_size, num_students)

    print(json.dumps(output, indent=4))


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
    getTeams()
except Exception as e:
    print("error")
    print(e)
