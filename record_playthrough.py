from helper import *

monkeysByTypeCount = {"hero": 0}

for type in keybinds["monkeys"]:
    monkeysByTypeCount[type] = 0

selectedMonkey = None
monkeys = {}
config = {"steps": []}


def getClosestMonkey(pos):
    closestMonkey = None
    closestDist = 10000
    dist = None
    for monkey in monkeys:
        dist = math.dist(pos, monkeys[monkey]["pos"])
        if dist < closestDist:
            closestMonkey = monkeys[monkey]
            closestDist = dist

    print("selected monkey: " + (closestMonkey["name"] or ""))
    return {"monkey": closestMonkey, "dist": closestDist}


def signalHandler(signum, frame):
    keyboard.unhook_all()
    print("stopping recording!")
    writeBTD6InstructionsFile(config)
    sys.exit(0)


def onRecordingEvent(e):
    global selectedMonkey
    global config
    global monkeys
    global monkeysByTypeCount

    pos = pyautogui.position()

    activeWindow = ahk.get_active_window()
    if not activeWindow or not isBTD6Window(activeWindow.title):
        print("BTD6 not focused")
        return
    if not pyautogui.onScreen(pos):
        print(tupleToStr(pos) + " not on screen")
        return
    if e["action"] == "select_monkey":
        selectedMonkey = getClosestMonkey(pos)["monkey"]
    elif e["action"] == "remove_obstacle":
        config["steps"].append({"action": "remove", "pos": pos})
        print("remove obstacle at " + tupleToStr(pos) + " for ???")
    elif e["action"] == "retarget":
        if selectedMonkey is None:
            print("selectedMonkey unassigned!")
            return
        step = {"action": "retarget", "name": selectedMonkey["name"]}
        if keyboard.is_pressed("space"):
            step["to"] = pos
            print("retarget " + selectedMonkey["name"] + " to " + tupleToStr(pos))
        elif selectedMonkey["type"] == "mortar":
            print("mortar can only be retargeted to a position(tab + space)!")
            return
        else:
            print("retarget " + selectedMonkey["name"])
        config["steps"].append(step)
    elif e["action"] == "monkey_special":
        if selectedMonkey is None:
            print("selectedMonkey unassigned!")
            return
        config["steps"].append({"action": "special", "name": selectedMonkey["name"]})
        print("special " + selectedMonkey["name"])
    elif e["action"] == "sell":
        if selectedMonkey is None:
            print("selectedMonkey unassigned!")
            return
        config["steps"].append({"action": "sell", "name": selectedMonkey["name"]})
        print("sell " + selectedMonkey["name"])
        monkeys.pop(selectedMonkey["name"])
        selectedMonkey = None
    elif e["action"] == "place" and e["type"] == "hero":
        monkeyName = "hero" + str(monkeysByTypeCount["hero"])
        config["steps"].append(
            {"action": "place", "type": "hero", "name": monkeyName, "pos": pos}
        )
        print("place " + config["hero"] + " " + monkeyName + " at " + tupleToStr(pos))
        monkeysByTypeCount["hero"] += 1
        monkeys[monkeyName] = {"name": monkeyName, "type": config["hero"], "pos": pos}
    elif e["action"] == "place":
        monkeyName = e["type"] + str(monkeysByTypeCount[e["type"]])
        config["steps"].append(
            {"action": "place", "type": e["type"], "name": monkeyName, "pos": pos}
        )
        print("place " + e["type"] + " " + monkeyName + " " + tupleToStr(pos))
        monkeysByTypeCount[e["type"]] += 1
        monkeys[monkeyName] = {"name": monkeyName, "type": e["type"], "pos": pos}
        selectedMonkey = getClosestMonkey(pos)["monkey"]
    elif e["action"] == "upgrade":
        if selectedMonkey is None:
            print("selectedMonkey unassigned!")
            return
        config["steps"].append(
            {"action": "upgrade", "name": selectedMonkey["name"], "path": e["path"]}
        )
        print("upgrade " + selectedMonkey["name"] + " path " + e["path"])
    elif e["action"] == "await_round":
        e["round"] = input("wait for round: ")
        try:
            e["round"] = int(e["round"])
            if e["round"] > 0 and not any((x["action"] == "await_round" and x["round"] >= e["round"]) for x in config["steps"]):
                config["steps"].append({"action": "await_round", "round": e["round"]})
                print("await round " + str(e["round"]))
                return
        except ValueError:
            pass
        print("invalid round! aborting entry!")
        

while True:
    print("mapname > ")
    config["map"] = input().replace(" ", "_").lower()
    if config["map"] in maps:
        break
    else:
        print("unknown map!")

while True:
    print("gamemode > ")
    config["gamemode"] = input().replace(" ", "_").lower()
    if config["gamemode"] in gamemodes:
        break
    else:
        print("unknown gamemode!")

while True:
    print("hero > ")
    config["hero"] = input().replace(" ", "_").lower()
    if config["hero"] in towers["heros"]:
        break
    else:
        print("unknown hero!")

filename = getBTD6InstructionsFileNameByConfig(config)

argv = np.array(sys.argv)

extending = False

if len(np.where(argv == "-e")[0]):
    print("extending upon existing file")
    if not exists(filename):
        print("requested extending of file, but file not existing!")
        exit()
    extending = True
    newConfig = parseBTD6InstructionsFile(filename)
    config["steps"] = newConfig["steps"]
    monkeys = newConfig["monkeys"]

    for monkeyname in monkeys:
        monkeysByTypeCount[monkeys[monkeyname]["type"]] += 1

if not extending and exists(filename):
    print(
        'run for selected config already existing! rename or delete "'
        + filename
        + '" if you want to record again!'
    )
    exit()

print('started recording to "' + filename + '"')

signal.signal(signal.SIGINT, signalHandler)

# filtering on all keypresses doesn't work as the provided key name is localized
# keyboard.hook(onKeyPress)

def createKeybind(key, data):
    keyboard.on_press_key(
        key,
        lambda e: onRecordingEvent(data),
    )

for monkey, key in keybinds["monkeys"].items():
    createKeybind(key, {"action": "place", "type": monkey})

createKeybind(keybinds["path"]["0"], {"action": "upgrade", "path": "0"})
createKeybind(keybinds["path"]["1"], {"action": "upgrade", "path": "1"})
createKeybind(keybinds["path"]["2"], {"action": "upgrade", "path": "2"})

createKeybind(keybinds["recording"]["select_monkey"], {"action": "select_monkey"})
createKeybind(keybinds["recording"]["remove_obstacle"], {"action": "remove_obstacle"})
createKeybind(keybinds["recording"]["retarget"], {"action": "retarget"})
createKeybind(keybinds["recording"]["sell"], {"action": "sell"})
createKeybind(keybinds["recording"]["monkey_special"], {"action": "monkey_special"})
createKeybind(keybinds["recording"]["await_round"], {"action": "await_round", "round": "0"})

while True:
    time.sleep(60)
