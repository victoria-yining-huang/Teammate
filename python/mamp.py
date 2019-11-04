import json
import sys
import time

print("json_result_output")
output = '{"model": {"hasConflicts": true},"teams": {"1": {"members": ["jdoe2", "kbrown3"]},"2": {"members": ["jsmith1", "mlee4"]}},"people": {"jsmith1": {"id": "jsmith1","firstName": "John","lastName": "Smith","email": "jsmith1@uwaterloo.ca","conflicts": ["jdoe2"]},"jdoe2": {"id": "jdoe2","firstName": "Jane","lastName": "Doe","email": "jdoe2@uwaterloo.ca","conflicts": ["jsmith1", "kbrown3", "mlee4"]},"kbrown3": {"id": "kbrown3","firstName": "Kelly","lastName": "Brown","email": "kbrown3@uwaterloo.ca","conflicts": ["mlee4", "jsmith1", "jdoe2"]},"mlee4": {"id": "mlee4","firstName": "Mike","lastName": "Lee","email": "mlee4@uwaterloo.ca","conflicts": []}}}'
output = {
    "model": {
        "hasConflicts": True
    },
    "teams": {
        1: {
            "members": ["jdoe2", "kbrown3", "rryan7"]
        },
        2: {
            "members": ["jsmith1", "mlee4", "jcros4"]
        },
        3: {
            "members": ["dgoul9", "smcca9"]
        }
    },
    "people": {
        "jsmith1": {
            "id": "jsmith1",
            "firstName": "John",
            "lastName": "Smith",
            "email": "jsmith1@uwaterloo.ca",
            "gpa": 85,
            "gender": "m",
            "conflicts": ["jdoe2"]
        },
        "jdoe2": {
            "id": "jdoe2",
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jdoe2@uwaterloo.ca",
            "gpa": 60,
            "gender": "f",
            "conflicts": ["jsmith1"]
        },
        "kbrown3": {
            "id": "kbrown3",
            "firstName": "Kelly",
            "lastName": "Brown",
            "email": "kbrown3@uwaterloo.ca",
            "gpa": 95,
            "gender": "f",
            "conflicts": ["mlee4", "jsmith1", "jdoe2"]
        },
        "mlee4": {
            "id": "mlee4",
            "firstName": "Mike",
            "lastName": "Lee",
            "email": "mlee4@uwaterloo.ca",
            "gpa": 75,
            "gender": "m",
            "conflicts": []
        },
        "jcros4": {
            "id": "jcros4",
            "firstName": "Johnathan",
            "lastName": "Crosby",
            "email": "jcros4@uwaterloo.ca",
            "gpa": 80,
            "gender": "m",
            "conflicts": []
        },
        "rryan7": {
            "id": "rryan7",
            "firstName": "Ray",
            "lastName": "Ryan",
            "email": "rryan7@uwaterloo.ca",
            "gpa": 62,
            "gender": "x",
            "conflicts": []
        },
        "smcca9": {
            "id": "smcca9",
            "firstName": "Sally",
            "lastName": "Mccann",
            "email": "smcca9@uwaterloo.ca",
            "gpa": 90,
            "gender": "f",
            "conflicts": []
        },
        "dgoul9": {
            "id": "dgoul9",
            "firstName": "Debra",
            "lastName": "Gould",
            "email": "dgoul9@uwaterloo.ca",
            "gpa": 78,
            "gender": "m",
            "conflicts": []
        }
    }
}

print(json.dumps(output))
