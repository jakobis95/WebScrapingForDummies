import json

def showcontent():
    with open('Info.json', 'r') as c:
        obj = json.load(c)
        print(obj['content'][1]['masterData'])
        #for elements in obj['content']:
        for stuff in obj['content'][1]:
            print(stuff)


if __name__ == '__main__':
    showcontent()