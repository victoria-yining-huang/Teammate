import json
import sys
import time


def start():

    print("TEMP 1")
    print("TEMP 2")

    time.sleep(3)

    #print(json.loads(sys.argv[1].replace('\\', ''), strict=False))

    output = '{"model": {"hasConflicts": true},"teams": {"1": {"members": ["jdoe2", "kbrown3"]},"2": {"members": ["jsmith1", "mlee4"]}},"people": {"jsmith1": {"id": "jsmith1","firstName": "John","lastName": "Smith","email": "jsmith1@uwaterloo.ca","conflicts": ["jdoe2"]},"jdoe2": {"id": "jdoe2","firstName": "Jane","lastName": "Doe","email": "jdoe2@uwaterloo.ca","conflicts": ["jsmith1", "kbrown3", "mlee4"]},"kbrown3": {"id": "kbrown3","firstName": "Kelly","lastName": "Brown","email": "kbrown3@uwaterloo.ca","conflicts": ["mlee4", "jsmith1", "jdoe2"]},"mlee4": {"id": "mlee4","firstName": "Mike","lastName": "Lee","email": "mlee4@uwaterloo.ca","conflicts": []}}}'
    print(json.dumps(output, indent=4))


start()
