from helper import *

keybinds = json.load(open('keybinds.json'))
costs = json.load(open('costs.json'))
maps = json.load(open('maps.json'))
gamemodes = json.load(open('gamemodes.json'))

monkeysByTypeCount = {'hero': 0}

for type in keybinds['monkeys']:
    monkeysByTypeCount[type] = 0

selectedMonkey = None
monkeys = {}
config = {'steps': []}

def getClosestMonkey(pos):
    closestMonkey = None
    closestDist = 10000
    dist = None
    for monkey in monkeys:
        dist = math.dist(pos, monkeys[monkey]['pos'])
        if dist < closestDist:
            closestMonkey = monkeys[monkey]
            closestDist = dist

    print("selected monkey: " + (closestMonkey['name'] or ""))
    return {'monkey': closestMonkey, 'dist': closestDist}

def signalHandler(signum, frame):
    keyboard.unhook_all()
    print('stopping recording!')
    writeBTD6InstructionsFile(config)
    sys.exit(0)

def onRecordingEvent(e):
    global selectedMonkey
    global config
    global monkeys
    global monkeysByTypeCount

    print(e)
    
    pos = pyautogui.position()
    
    activeWindow = ahk.get_active_window()
    if not activeWindow or activeWindow.title.decode() != 'BloonsTD6':
        print('BTD6 not focused')
        return
    if not pyautogui.onScreen(pos):
        print(tupleToStr(pos) + ' not on screen')
        return
    if e['action'] == 'select_monkey':
        selectedMonkey = getClosestMonkey(pos)['monkey']
    elif e['action'] == 'remove_obstacle':
        config['steps'].append({'action': 'remove', 'pos': pos})
        print('remove obstacle at ' + tupleToStr(pos) + ' for ???')
    elif e['action'] == 'retarget':
        if selectedMonkey is None:
            print('selectedMonkey unassigned!')
            return
        step = {'action': 'retarget', 'name': selectedMonkey['name']}
        if keyboard.is_pressed('space'):
            step['to'] = pos
            print('retarget ' + selectedMonkey['name'] + ' to ' + tupleToStr(pos))
        elif selectedMonkey['type'] == 'mortar':
            print('mortar can only be retargeted to a position(tab + space)!')
            return
        else:
            print('retarget ' + selectedMonkey['name'])
        config['steps'].append(step)
    elif e['action'] == 'monkey_special':
        if selectedMonkey is None:
            print('selectedMonkey unassigned!')
            return
        config['steps'].append({'action': 'special', 'name': selectedMonkey['name']})
        print('special ' + selectedMonkey['name'])
    elif e['action'] == 'sell':
        if selectedMonkey is None:
            print('selectedMonkey unassigned!')
            return
        config['steps'].append({'action': 'sell', 'name': selectedMonkey['name']})
        print('sell ' + selectedMonkey['name'])
        monkeys.pop(selectedMonkey['name'])
        selectedMonkey = None
    elif e['action'] == 'place' and e['type'] == 'hero':
        monkeyName = 'hero' + str(monkeysByTypeCount['hero'])
        config['steps'].append({'action': 'place', 'type': 'hero', 'name': monkeyName, 'pos': pos})
        print('place ' + config['hero'] + ' ' + monkeyName + ' at ' + tupleToStr(pos))
        monkeysByTypeCount['hero'] += 1
        monkeys[monkeyName] = {'name': monkeyName, 'type': config['hero'], 'pos': pos}
    elif e['action'] == 'place':
        monkeyName = e['type'] + str(monkeysByTypeCount[e['type']])
        config['steps'].append({'action': 'place', 'type': e['type'], 'name': monkeyName, 'pos': pos})
        print('place ' + e['type'] + ' ' + monkeyName + ' ' + tupleToStr(pos))
        monkeysByTypeCount[e['type']] += 1
        monkeys[monkeyName] = {'name': monkeyName, 'type': e['type'], 'pos': pos}
    elif e['action'] == 'upgrade':
        if selectedMonkey is None:
            print('selectedMonkey unassigned!')
            return
        config['steps'].append({'action': 'upgrade', 'name': selectedMonkey['name'], 'path': e['path']})
        print('upgrade ' + selectedMonkey['name'] + ' path ' + e['path'])

while True:
    print('mapname > ')
    config['map'] = input()
    if config['map'] in maps:
        break
    else:
        print('unknown map!')

while True:
    print('gamemode > ')
    config['gamemode'] = input()
    if config['gamemode'] in gamemodes:
        break
    else:
        print('unknown gamemode!')

while True:
    print('hero > ')
    config['hero'] = input()
    if config['hero'] in costs['heros']:
        break
    else:
        print('unknown hero!')

filename = getBTD6InstructionsFileNameByConfig(config)

argv = np.array(sys.argv)

extending = False

if len(np.where(argv == '-e')[0]):
    print('extending upon existing file')
    if not exists(filename):
        print('requested extending of file, but file not existing!')
        exit()
    extending = True
    newConfig = parseBTD6InstructionsFile(filename)
    config['steps'] = newConfig['steps']
    monkeys = newConfig['monkeys']

    for monkeyname in monkeys:
        monkeysByTypeCount[monkeys[monkeyname]['type']] += 1

if not extending and exists(filename):
    print('run for selected config already existing! rename or delete "' + filename + '" if you want to record again!')
    exit()

print('started recording to "' + filename + '"')

signal.signal(signal.SIGINT, signalHandler)

# filtering on all keypresses doesn't work as the provided key name is localized
# keyboard.hook(onKeyPress)

keyboard.on_press_key(keybinds['monkeys']['dart'], lambda e: onRecordingEvent({'action': 'place', 'type': 'dart'}))
keyboard.on_press_key(keybinds['monkeys']['boomerang'], lambda e: onRecordingEvent({'action': 'place', 'type': 'boomerang'}))
keyboard.on_press_key(keybinds['monkeys']['bomb'], lambda e: onRecordingEvent({'action': 'place', 'type': 'bomb'}))
keyboard.on_press_key(keybinds['monkeys']['tack'], lambda e: onRecordingEvent({'action': 'place', 'type': 'tack'}))
keyboard.on_press_key(keybinds['monkeys']['ice'], lambda e: onRecordingEvent({'action': 'place', 'type': 'ice'}))
keyboard.on_press_key(keybinds['monkeys']['glue'], lambda e: onRecordingEvent({'action': 'place', 'type': 'glue'}))
keyboard.on_press_key(keybinds['monkeys']['sniper'], lambda e: onRecordingEvent({'action': 'place', 'type': 'sniper'}))
keyboard.on_press_key(keybinds['monkeys']['sub'], lambda e: onRecordingEvent({'action': 'place', 'type': 'sub'}))
keyboard.on_press_key(keybinds['monkeys']['buccaneer'], lambda e: onRecordingEvent({'action': 'place', 'type': 'buccaneer'}))
keyboard.on_press_key(keybinds['monkeys']['ace'], lambda e: onRecordingEvent({'action': 'place', 'type': 'ace'}))
keyboard.on_press_key(keybinds['monkeys']['heli'], lambda e: onRecordingEvent({'action': 'place', 'type': 'heli'}))
keyboard.on_press_key(keybinds['monkeys']['mortar'], lambda e: onRecordingEvent({'action': 'place', 'type': 'mortar'}))
keyboard.on_press_key(keybinds['monkeys']['dartling'], lambda e: onRecordingEvent({'action': 'place', 'type': 'dartling'}))
keyboard.on_press_key(keybinds['monkeys']['wizard'], lambda e: onRecordingEvent({'action': 'place', 'type': 'wizard'}))
keyboard.on_press_key(keybinds['monkeys']['super'], lambda e: onRecordingEvent({'action': 'place', 'type': 'super'}))
keyboard.on_press_key(keybinds['monkeys']['ninja'], lambda e: onRecordingEvent({'action': 'place', 'type': 'ninja'}))
keyboard.on_press_key(keybinds['monkeys']['alchemist'], lambda e: onRecordingEvent({'action': 'place', 'type': 'alchemist'}))
keyboard.on_press_key(keybinds['monkeys']['druid'], lambda e: onRecordingEvent({'action': 'place', 'type': 'druid'}))
keyboard.on_press_key(keybinds['monkeys']['farm'], lambda e: onRecordingEvent({'action': 'place', 'type': 'farm'}))
keyboard.on_press_key(keybinds['monkeys']['engineer'], lambda e: onRecordingEvent({'action': 'place', 'type': 'engineer'}))
keyboard.on_press_key(keybinds['monkeys']['spike'], lambda e: onRecordingEvent({'action': 'place', 'type': 'spike'}))
keyboard.on_press_key(keybinds['monkeys']['village'], lambda e: onRecordingEvent({'action': 'place', 'type': 'village'}))
keyboard.on_press_key(keybinds['monkeys']['hero'], lambda e: onRecordingEvent({'action': 'place', 'type': 'hero'}))

keyboard.on_press_key(keybinds['path']['0'], lambda e: onRecordingEvent({'action': 'upgrade', 'path': '0'}))
keyboard.on_press_key(keybinds['path']['1'], lambda e: onRecordingEvent({'action': 'upgrade', 'path': '1'}))
keyboard.on_press_key(keybinds['path']['2'], lambda e: onRecordingEvent({'action': 'upgrade', 'path': '2'}))

keyboard.on_press_key(keybinds['recording']['select_monkey'], lambda e: onRecordingEvent({'action': 'select_monkey'}))
keyboard.on_press_key(keybinds['recording']['remove_obstacle'], lambda e: onRecordingEvent({'action': 'remove_obstacle'}))
keyboard.on_press_key(keybinds['recording']['retarget'], lambda e: onRecordingEvent({'action': 'retarget'}))
keyboard.on_press_key(keybinds['recording']['sell'], lambda e: onRecordingEvent({'action': 'sell'}))
keyboard.on_press_key(keybinds['recording']['monkey_special'], lambda e: onRecordingEvent({'action': 'monkey_special'}))
    
while True:
    time.sleep(60)