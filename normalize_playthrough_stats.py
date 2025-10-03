from helper import *
import shutil

for filename in playthroughStats:
    for resolution in playthroughStats[filename]:
        if not re.search(r'\d+x\d+', resolution):
            continue
        for gamemode in playthroughStats[filename][resolution]:
            if gamemode == 'validation_result':
                continue
            if 'win_times' in playthroughStats[filename][resolution][gamemode] and len(playthroughStats[filename][resolution][gamemode]['win_times']):
                playthroughStats[filename][resolution][gamemode]['attempts'] = 1
                playthroughStats[filename][resolution][gamemode]['wins'] = 1
                playthroughStats[filename][resolution][gamemode]['win_times'] = [np.average(playthroughStats[filename][resolution][gamemode]['win_times'])]
            else:
                playthroughStats[filename][resolution][gamemode]['attempts'] = 0
                playthroughStats[filename][resolution][gamemode]['wins'] = 0
                playthroughStats[filename][resolution][gamemode]['win_times'] = []

shutil.copy('playthrough_stats.json', 'playthrough_stats_backup.json')

fp = open("playthrough_stats.json", "w")
fp.write(json.dumps(playthroughStats, indent=4))
fp.close()