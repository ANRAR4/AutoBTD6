from helper import *

extraComments = {
    'playthroughs/spice_islands#alternate_bloons_rounds#2560x1440#noMK#noWaterTowers.btd6': ['no water towers(achievement)'],
}

mapComments = {
    'geared': 'changing monkey positions (1)',
    'sanctuary': 'changing monkey positions (1)',
}

output = ''
output += '<table border=1 style="border-collapse: collapse">' + '\n'
output += '\t<tr>' + '\n'
output += '\t\t<th>Map</th>' + '\n'
output += '\t\t<th>Category</th>' + '\n'

for gamemode in gamemodes:
    output += '\t\t<th>' + gamemodes[gamemode]['name'] + '</th>' + '\n'

output += '\t\t<th>Comment</th>' + '\n'
output += '\t</tr>' + '\n'

playthroughs = getAllAvailablePlaythroughs()

mapsByCategory = {}

for mapname in maps:
    if not maps[mapname]['category'] in mapsByCategory:
        mapsByCategory[maps[mapname]['category']] = []
    mapsByCategory[maps[mapname]['category']].append((mapname, maps[mapname]))

for category in mapsByCategory:
    firstRow = True
    for mapData in mapsByCategory[category]:
        mapname = mapData[0]
        mapData = mapData[1]
        if firstRow:
            output += '\t<tr style="border-top: 2px solid white">' + '\n'
            output += '\t<th>' + mapData['name'] + '</th>' + '\n'
            output += '\t<td rowspan=' + str(len(mapsByCategory[category])) + '>' + category + '</th>' + '\n'
            firstRow = False
        else:
            output += '\t<tr>' + '\n'
            output += '\t<th>' + mapData['name'] + '</th>' + '\n'

        for gamemode in gamemodes:
            output += '\t\t<td>'
            firstPlaythroughRow = True
            for playthrough in ((playthroughs[mapname] if mapname in playthroughs else {})[gamemode] if gamemode in (playthroughs[mapname] if mapname in playthroughs else {}) else []):
                noMK = False
                noLL = False
                noLLwMK = False
                for m in re.finditer('(?P<noMK>noMK(?:#|$))?(?:(?P<singleType>[a-z]+)Only(?:#|$))?(?P<noLL>noLL(?:#|$))?(?P<noLLwMK>noLLwMK(?:#|$))?', playthrough['fileConfig']['comment'] if 'comment' in playthrough['fileConfig'] and playthrough['fileConfig']['comment'] else ''):
                    if m.group('noMK'):
                        noMK = True
                    if m.group('noLL'):
                        noLL = True
                    if m.group('noLLwMK'):
                        noLLwMK = True
                description = ''
                if noMK:
                    description += 'supported'
                else:
                    description += 'with MK'

                mapConfig = parseBTD6InstructionsFile(playthrough['filename'])
                
                if 'hero' in mapConfig:
                    description += ', ' + ' '.join([w.capitalize() for w in mapConfig['hero'].split(' ')])
                else:
                    description += ', -'
                
                singleType = checkForSingleMonkeyType(mapConfig['monkeys'])
                if singleType:
                    description += ', ' + singleType + ' only'
                singleGroup = checkForSingleMonkeyGroup(mapConfig['monkeys'])
                if singleGroup:
                    description += ', ' + singleGroup + ' monkeys only'
                
                if noLL:
                    NOP
                elif noLLwMK:
                    description += ', (*)'
                else:
                    description += ', *'

                if playthrough['filename'] in extraComments:
                    for extraComment in extraComments[playthrough['filename']]:
                        description += ', ' + extraComment
                
                description += ', native: ' + playthrough['fileConfig']['resolution'] + (', tested for: ' + ', '.join(filter(lambda x: 'validation_result' in playthroughStats[playthrough['filename']][x] and playthroughStats[playthrough['filename']][x]['validation_result'] == True, playthroughStats[playthrough['filename']].keys())) if playthrough['filename'] in playthroughStats and len(playthroughStats[playthrough['filename']].keys()) and len(list(filter(lambda x: 'validation_result' in playthroughStats[playthrough['filename']][x] and playthroughStats[playthrough['filename']][x]['validation_result'] == True, playthroughStats[playthrough['filename']].keys()))) else '')

                title = ''
                monkeyUpgradeRequirements = getMonkeyUpgradeRequirements(mapConfig['monkeys'])
                for monkey in monkeyUpgradeRequirements:
                    if len(title):
                        title += ', '
                    title += monkey + '(' + monkeyUpgradesToString(monkeyUpgradeRequirements[monkey]) + ')'
                
                if firstPlaythroughRow:
                    firstPlaythroughRow = False
                else:
                    output += '<br><br>'
                output += '<a href="' + playthrough['filename'] + '"' + ('title="required monkeys: ' + title + '"' if len(title) else '') + '>' + ('<i>' + description + '</i>' if not playthrough['isOriginalGamemode'] else description) + '</a>'
            output += '</td>' + '\n'

        if mapname in mapComments:
            output += '\t\t<td>' + mapComments[mapname] + '</td>' + '\n'
        else:
            output += '\t\t<td></td>' + '\n'
        output += '\t</tr>' + '\n'
        
output += '</table>' + '\n'

fp = open('README.md')
oldREADME = fp.read()
fp.close()

output = re.sub('<div id="supported_maps">.*<\/div>', '<div id="supported_maps">\n' + output + '</div>', oldREADME, 1, re.DOTALL)

if output == oldREADME:
    print('README identical after replacement')

fp = open('README.md', 'w')
fp.write(output)
fp.close()
