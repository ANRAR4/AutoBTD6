from helper import *

if len(sys.argv) < 4 or not sys.argv[2] in ['before', 'after']:
    print(f'Usage: py {sys.argv[0]} "<name of the new map>" <before|after> "<name of adjacent map>"')
    exit()

nextMap = sys.argv[3]
nextMapKey = mapnameToKeyname(nextMap)
newMap = sys.argv[1]
newMapKey = mapnameToKeyname(newMap)
insertPosOffset = 0 if sys.argv[2] == 'before' else 1

if not nextMapKey in maps:
    print(f'Unknown map: {nextMap}')
    exit()
if newMapKey in maps:
    print(f'New map already inserted!')
    exit()

mapsByCategory[maps[nextMapKey]['category']].insert(mapsByCategory[maps[nextMapKey]['category']].index(nextMapKey) + insertPosOffset, newMapKey)
maps[newMapKey] = {'name': newMap}

newMaps = mapsByCategoryToMaplist(mapsByCategory, maps)

newMapsTmp = {}

i = 0
for mapname in newMaps:
    newMapsTmp[mapname] = f"%placeholder{i}%"
    i += 1

output = json.dumps(newMapsTmp, indent=4)

i = 0
for mapname in newMaps:
    output = output.replace(f"\"%placeholder{i}%\"", json.dumps(newMaps[mapname]))
    i += 1

fp = open('maps.json', "w")
fp.write(output)
fp.close()

print('"maps.json" successfully updated')