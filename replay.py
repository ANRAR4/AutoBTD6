from helper import *
from ocr import custom_ocr
import argparse
import colorama #i like colors


smallActionDelay = 0.05
actionDelay = 0.2
menuChangeDelay = 1

def getResolutionDependentData(resolution = pyautogui.size()):
    nativeResolution = (2560, 1440)
    requiredComparisonImages = [{'category': 'screens', 'name': 'startmenu'}, {'category': 'screens', 'name': 'map_selection'}, {'category': 'screens', 'name': 'difficulty_selection'}, {'category': 'screens', 'name': 'gamemode_selection'}, {'category': 'screens', 'name': 'hero_selection'}, {'category': 'screens', 'name': 'ingame'}, {'category': 'screens', 'name': 'ingame_paused'}, {'category': 'screens', 'name': 'victory_summary'}, {'category': 'screens', 'name': 'victory'}, {'category': 'screens', 'name': 'defeat'}, {'category': 'screens', 'name': 'overwrite_save'}, {'category': 'screens', 'name': 'levelup'}, {'category': 'screens', 'name': 'apopalypse_hint'}, {'category': 'screens', 'name': 'round_100_insta'}, {'category': 'game_state', 'name': 'game_paused'}, {'category': 'game_state', 'name': 'game_playing_slow'}, {'category': 'game_state', 'name': 'game_playing_fast'}]
    optionalComparisonImages = [{'category': 'screens', 'name': 'collection_claim_chest', 'for': [Mode.CHASE_REWARDS.name]}]
    requiredLocateImages = [{'name': 'remove_obstacle_confirm_button'}, {'name': 'button_home'}]
    optionalLocateImages = [{'name': 'unknown_insta', 'for': [Mode.CHASE_REWARDS.name]}, {'name': 'unknown_insta_mask', 'for': [Mode.CHASE_REWARDS.name]}]

    rawSegmentCoordinates = {
        "2560x1440": {
            'lives': (158, 32, 330, 84),
            # 'mana_lives': (90, 81, 154, 131),
            'mana_lives': (60, 74, 173, 142),
            # 'money': (458, 32, 955, 84),
            # 'money': (455, 18, 955, 99),
            'money': (459, 31, 959, 80),
            # 'round': (1900, 43, 2075, 87),
            'round': (1847, 39, 2084, 95),
        }
    }

    if getResolutionString(resolution) in rawSegmentCoordinates:
        segmentCoordinates = rawSegmentCoordinates[getResolutionString(resolution)]
    else:
        segmentCoordinates = {}
        for key in rawSegmentCoordinates[getResolutionString(nativeResolution)]:
            segmentCoordinates[key] = [round(x * resolution[0] / nativeResolution[0]) if i % 2 == 0 else round(x * resolution[1] / nativeResolution[1]) for i, x in enumerate(rawSegmentCoordinates[getResolutionString(nativeResolution)][key])]

    imagesDir = 'images/' + getResolutionString(resolution) + '/'

    comparisonImages = {}
    locateImages = {}

    if not exists(imagesDir):
        return None

    supportedModes = dict.fromkeys([e.name for e in Mode], True)

    for img in requiredComparisonImages:
        filename = (img['filename'] if 'filename' in img else img['name']) + '.png'
        if not exists(imagesDir + filename):
            print(filename + ' missing!')
            return None
        elif 'category' in img:
            if not img['category'] in comparisonImages:
                comparisonImages[img['category']] = {}
            comparisonImages[img['category']][img['name']] = cv2.imread(imagesDir + filename)
        else:
            comparisonImages[img['name']] = cv2.imread(imagesDir + filename)
    
    for img in optionalComparisonImages:
        filename = (img['filename'] if 'filename' in img else img['name']) + '.png'
        if not exists(imagesDir + filename):
            if 'for' in img:
                for mode in img['for']:
                    supportedModes.pop(mode, None)
        elif 'category' in img:
            if not img['category'] in comparisonImages:
                comparisonImages[img['category']] = {}
            comparisonImages[img['category']][img['name']] = cv2.imread(imagesDir + filename)
        else:
            comparisonImages[img['name']] = cv2.imread(imagesDir + filename)
    
    for img in requiredLocateImages:
        filename = (img['filename'] if 'filename' in img else img['name']) + '.png'
        if not exists(imagesDir + filename):
            print(filename + ' missing!')
            return None
        elif 'category' in img:
            if not img['category'] in locateImages:
                locateImages[img['category']] = {}
            locateImages[img['category']][img['name']] = cv2.imread(imagesDir + filename)
        else:
            locateImages[img['name']] = cv2.imread(imagesDir + filename)
    
    for img in optionalLocateImages:
        filename = (img['filename'] if 'filename' in img else img['name']) + '.png'
        if not exists(imagesDir + filename):
            if 'for' in img:
                for mode in img['for']:
                    supportedModes.pop(mode, None)
        elif 'category' in img:
            if not img['category'] in locateImages:
                locateImages[img['category']] = {}
            locateImages[img['category']][img['name']] = cv2.imread(imagesDir + filename)
        else:
            locateImages[img['name']] = cv2.imread(imagesDir + filename)

    locateImages['collection'] = {}
    if exists(imagesDir + 'collection_events'):
        for filename in os.listdir(imagesDir + 'collection_events'):
            locateImages['collection'][filename.replace('.png', '')] = cv2.imread(imagesDir + 'collection_events/' + filename)
    
    return {'comparisonImages': comparisonImages, 'locateImages': locateImages, 'segmentCoordinates': segmentCoordinates, 'supportedModes': supportedModes, 'resolution': resolution}

class State(Enum):
    UNDEFINED = 0
    IDLE = 1
    INGAME = 2
    GOTO_HOME = 3
    GOTO_INGAME = 4
    SELECT_HERO = 5
    FIND_HARDEST_INCREASED_REWARDS_MAP = 6
    MANAGE_OBJECTIVES = 7
    EXIT = 8

class Screen(Enum):
    UNKNOWN = 0
    STARTMENU = 1
    MAP_SELECTION = 3
    DIFFICULTY_SELECTION = 4
    GAMEMODE_SELECTION = 5
    HERO_SELECTION = 6
    INGAME = 7
    INGAME_PAUSED = 8
    VICTORY_SUMMARY = 9
    VICTORY = 10
    DEFEAT = 11
    OVERWRITE_SAVE = 12
    LEVELUP = 13
    APOPALYPSE_HINT = 14
    ROUND_100_INSTA = 15
    COLLECTION_CLAIM_CHEST = 16
    BTD6_UNFOCUSED = 17

class Mode(Enum):
    ERROR = 0
    SINGLE_MAP = 1
    RANDOM_MAP = 2
    CHASE_REWARDS = 3
    DO_ACHIEVEMENTS = 4
    MISSING_MAPS = 5
    XP_FARMING = 6
    MM_FARMING = 7
    MISSING_STATS = 8
    VALIDATE_PLAYTHROUGHS = 9
    VALIDATE_COSTS = 10

def getGamemodePosition(gamemode):
    while not isinstance(imageAreas["click"]["gamemode_positions"][gamemode], list):
        gamemode = imageAreas["click"]["gamemode_positions"][gamemode]
    return imageAreas["click"]["gamemode_positions"][gamemode]

def getNextNonSellAction(steps):
    for step in steps:
        if step['action'] != 'sell':
            return step
    return {'action': 'nop', 'cost': 0}

def sumAdjacentSells(steps):
    gain = 0
    for step in steps:
        if step['action'] != 'sell':
            return gain
        gain += -step['cost']
    return gain

exitAfterGame = False

def setExitAfterGame():
    global exitAfterGame
    activeWindow = ahk.get_active_window()
    if not activeWindow or activeWindow.title.decode() != 'BloonsTD6':
        return
    customPrint("Script will stop after finishing the current game!",  infoType=InfoType.INFO)
    exitAfterGame = True

def signalHandler(signum, frame):
    customPrint('Received SIGINT! exiting!',  infoType=InfoType.INFO)
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signalHandler)

    data = getResolutionDependentData()

    if not data:
        print('Unsupported resolution! Reference images missing!')
        return

    comparisonImages = data['comparisonImages']
    locateImages = data['locateImages']
    segmentCoordinates = data['segmentCoordinates']
    supportedModes = data['supportedModes']
    resolution = data['resolution']

    allAvailablePlaythroughs = getAllAvailablePlaythroughs(['own_playthroughs'], considerUserConfig=True)
    allAvailablePlaythroughsList = allPlaythroughsToList(allAvailablePlaythroughs)

    mode = Mode.ERROR
    logStats = True
    isContinue = False
    repeatObjectives = False
    doAllStepsBeforeStart = False
    listAvailablePlaythroughs = False
    handlePlaythroughValidation = ValidatedPlaythroughs.EXCLUDE_NON_VALIDATED
    usesAllAvailablePlaythroughsList = False

    collectionEvent = None
    valueUnit = ''

    originalObjectives = []
    objectives = []

    categoryRestriction = None
    gamemodeRestriction = None


    # PARSER TREE
    #
    # parser
    #     -mk
    #     -r
    #     -l
    #     -nv
    #     -ns
    #     file
    #         filename: argparse.FileType
    #         gamemode{easy, medium, hard, chimps, impoppable, etc}
    #         continue: int
    #             until: int
    #     random
    #         category{easy, intermediate, advanced, expert}
    #         gamemode{easy, medium, hard, chimps, impoppable, etc}
    #     collection
    #         event: <totem | halloween>
    #         category{easy, intermediate, advanced, expert}
    #         gamemode{easy, medium, hard, chimps, impoppable, etc}
    #     achievement
    #         throw NotImplemented
    #     missing
    #         throw NotImplemented
    #     xp
    #         n: int
    #     validate
    #         file
    #           file: argparse.FileType
    #         all
    #           category{easy, intermediate, advanced, expert}
    #           gamemode{easy, medium, hard, chimps, impoppable, etc}
    #     costs
    #       hero: bool

    def checkPositive(value : int) -> int: #used for input validation
        if value <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive integer value")
        return value

    parser = argparse.ArgumentParser(description="Automation of BTD6")
    
    #this trick allows for global flags
    base_subparser = argparse.ArgumentParser(add_help=False)
    base_subparser.add_argument('-r', '--repeat', action='store_true', required=False, help="repeat indefinitely") #Repeat?
    base_subparser.add_argument('-mk', '--monkeyknowledge', action='store_true', required=False, help="include playthroughs with monkey knowledge as a requirement") #Removes the whole need for the -noMK flag, assumes no MK if flag not specified, it doesn't really hurt if we assume they don't have monkey knowledge and they do
    base_subparser.add_argument('-l', '--list', action="store_true", required=False, help='list all found playthroughs') # NOTE: can only be used if not file mode
    base_subparser.add_argument('-nv', '--nonvalidated', action="store_true", required=False, help='include nonvalidated playthroughs') # include nonvalidated playthrus
    base_subparser.add_argument('-ns', '--nostats', action="store_false", required=False, help="disable stats logging (not recommended)")
    subparsers = parser.add_subparsers(dest='command')
    # achievementParser = subparsers.add_parser('achievements')
    # missingParser = subparsers.add_parser('missing')

    fileParser = subparsers.add_parser('file', help='plays the playthrough in the specified file', parents=[base_subparser])
    fileParser.add_argument('-f', '--file', required=True, type=argparse.FileType('r'), help='file where .btd6 run is stored')
    fileParser.add_argument('-gm', '--gamemode', required=False, choices=gamemodes.keys(), help='can be specified to overwrite the gamemode in the files title', default=None)
    fileParser.add_argument('--continue', required=False, help="if specified, starts from instruction. if -1, all instructions are executed before the game starts", type=int, dest="_continue", default=-2)
    fileParser.add_argument('--until', required=False, help="script will end at this instruction number", type=int, default=-1)
    # fileParser.add_argument('continue', required=False)
   
    randomParser = subparsers.add_parser('random', help='plays a random playthrough from all available playthroughs',parents=[base_subparser])
    randomParser.add_argument('-c', '--category', required=False, choices=mapsByCategory, default=None)
    randomParser.add_argument('-gm', '--gamemode', required=False, choices=gamemodes.keys(), default=None)

    collectionParser = subparsers.add_parser('collect', help='plays for most optimal rewards for collection event',parents=[base_subparser])
    collectionParser.add_argument('-e', '--event', required=True, choices=['halloween', 'totem'])
    collectionParser.add_argument('-c', '--category', required=False, choices=mapsByCategory, default=None)
    collectionParser.add_argument('-gm', '--gamemode', required=False, choices=gamemodes.keys(), default=None)

    xpParser = subparsers.add_parser('xp', help='plays a random playthrough out of n most efficient playthroughs',parents=[base_subparser])
    xpParser.add_argument('-n', type=checkPositive, required=False, default=1)
    
    mmParser = subparsers.add_parser('mm', help='plays a random playthrough out of n most efficient playthroughs',parents=[base_subparser])
    mmParser.add_argument('-n', type=checkPositive, required=False, default=1)

    validateParser = subparsers.add_parser('validate', help='validates a playthrough by setting up the monkeys in sandbox mode and checking if all actions are performed correctly', parents=[base_subparser])
    validateSubparser = validateParser.add_subparsers(dest='validate_func')
    
    file_validateSubparser = validateSubparser.add_parser('file', help='file of a playthrough to validate')
    file_validateSubparser.add_argument('-f', '--file', required=True, type=argparse.FileType('r'))

    all_validateSubparser = validateSubparser.add_parser('all', help="validates all playthroughs")
    all_validateSubparser.add_argument('-c', '--category', required=False, choices=mapsByCategory, help="only validate playthroughs in this category", default=None)
    all_validateSubparser.add_argument('-gm', '--gamemode', required=False, choices=gamemodes.keys(), help="only validate playthroughs in this gamemode", default=None)

    costsParser = subparsers.add_parser('costs', help="determines the cost of each monkey and each upgrade of each monkey",parents=[base_subparser])
    costsParser.add_argument('-hr', '--hero', required=False, action='store_true', help="additionally determines the base cost of each hero, if specified")

    args = parser.parse_args(sys.argv[1:])
    

    #Handle flags

    #Monkey knowledge
    setMonkeyKnowledgeStatus(args.monkeyknowledge)
    customPrint(f"Using playthoughs {colorama.Fore.GREEN +'with' if args.monkeyknowledge else colorama.Fore.RED + 'without'}{colorama.Fore.RESET} monkey knowledge enabled!", infoType=InfoType.INFO)
    
    #Stat logging
    logStats = args.nostats
    customPrint(f"Stats logging {colorama.Fore.GREEN +'enabled!' if args.nostats else colorama.Fore.RED + 'disabled (not recommended!)'}{colorama.Fore.RESET}", infoType=InfoType.INFO)
    
    #Repeat objectives
    repeatObjectives = args.repeat
    if args.repeat:
        customPrint(f"Repeating playthrough indefintely! Cancel with {colorama.Fore.MAGENTA}ctrl + c{colorama.Fore.RESET}!", infoType=InfoType.INFO)
    
    #nonvalidated playthroughs    
    if args.nonvalidated:
        handlePlaythroughValidation = ValidatedPlaythroughs.INCLUDE_ALL
    
    #list available playthrus
    listAvailablePlaythroughs = args.list

    #HANDLE COMMANDS
    if args.command == "file":
        #Alert user if they are trying to repeat playthrough, disable repeat
        if args.__contains__('until') and not args.__contains__('_continue'):
            customPrint("Invalid argument setup", infoType=InfoType.ERROR)
            return
        if args.repeat and args.__contains__('_continue'):
            repeatObjectives = False
            customPrint("Repeating playthroughs is unavailable if you are continuing a game! Disabling repeats", infoType=InfoType.WARN)


        filename = args.file.name
        instructionOffset = -1
        instructionLast = -1
        gamemode = args.gamemode
        if not parseBTD6InstructionFileName(filename): 
            customPrint('"' + filename + '" can\'t be recognized as a playthrough filename! Exiting!', infoType=InfoType.ERROR)
            return
        
        mapConfig = parseBTD6InstructionsFile(filename, gamemode=gamemode)
        mode = Mode.SINGLE_MAP

        if args.__contains__('_continue'):
            isContinue = True
            if args._continue == -1:
                instructionOffset = 0
                doAllStepsBeforeStart = True
            elif args._continue == -2: 
                pass #do nothing because instructionOffset is already -1
            else: 
                instructionOffset = args._continue

            customPrint(f"Stats logging {colorama.Fore.RED}disabled{colorama.Fore.RESET}!", infoType=InfoType.INFO)
            logStats = False

            if args.__contains__("until"):
                if args.until == -1:
                    pass # Do nothing because instructionLast is already -1    
                else:
                    instructionLast = args.until
        #NOTE: how did you live with yourself after writing this code

        # if len(argv) > iAdditional + 1 and argv[iAdditional] == 'continue':
        #     parsedArguments.append(argv[iAdditional])

        #     isContinue = True

        #     if str(argv[iAdditional + 1]) == '-':
        #         instructionOffset = 0
        #         doAllStepsBeforeStart = True
        #     elif str(argv[iAdditional + 1]).isdigit():
        #         instructionOffset = int(argv[iAdditional + 1])
        #     else:
        #         customPrint('Continue of playthrough requested but no instruction offset provided!',  infoType=InfoType.ERROR)
        #         return
        #     customPrint('Stats logging disabled!',  infoType=InfoType.INFO)
        #     logStats = False
        #     parsedArguments.append(argv[iAdditional + 1])
        #     iAdditional += 2

        #     if len(argv) >= iAdditional + 1 and argv[iAdditional] == 'until':
        #         if str(argv[iAdditional + 1]).isdigit():
        #             instructionLast = int(argv[iAdditional + 1])
        #         else:
        #             customPrint('Cutting of instructions for playthrough requested but no index provided!', infoType=InfoType.ERROR)
        #             return
        #         parsedArguments.append(argv[iAdditional])
        #         parsedArguments.append(argv[iAdditional + 1])
        #         iAdditional += 2
        
        if instructionOffset == -1:
            originalObjectives.append({'type': State.GOTO_HOME})
            if 'hero' in mapConfig:
                originalObjectives.append({'type': State.SELECT_HERO, 'mapConfig': mapConfig})
                originalObjectives.append({'type': State.GOTO_HOME})
            originalObjectives.append({'type': State.GOTO_INGAME, 'mapConfig': mapConfig})
        else:
            if instructionOffset >= len(mapConfig['steps']) or (instructionLast != -1 and instructionOffset >= instructionLast):
                customPrint(f'Instruction offset > last instruction ({str(instructionLast) if instructionLast != 1 else len(mapConfig["steps"])})', infoType=InfoType.ERROR)
                return
        
            if instructionLast != -1:
                mapConfig['steps'] = mapConfig['steps'][(instructionOffset + mapConfig['extrainstructions']):instructionLast]
            else:
                mapConfig['steps'] = mapConfig['steps'][(instructionOffset + mapConfig['extrainstructions']):]
            customPrint('Continuing playthrough. first instruction:', infoType=InfoType.INFO)
            customPrint(mapConfig['steps'][0])
        originalObjectives.append({'type': State.INGAME, 'mapConfig': mapConfig})
        originalObjectives.append({'type':  State.MANAGE_OBJECTIVES})

    if args.command == 'random':
        categoryRestriction = args.category
        gamemodeRestriction = args.gamemode
        customPrint('Playing random games' + (' on ' + args.gamemode if args.gamemode else '') + (' on ' + args.category + ' maps' if args.category else '') + '!',  infoType=InfoType.INFO)

        allAvailablePlaythroughs = filterAllAvailablePlaythroughs(allAvailablePlaythroughs, getMonkeyKnowledgeStatus(), handlePlaythroughValidation, args.category, args.gamemode)
        allAvailablePlaythroughsList = allPlaythroughsToList(allAvailablePlaythroughs)
        originalObjectives.append({'type': State.MANAGE_OBJECTIVES})
        mode = Mode.RANDOM_MAP
        usesAllAvailablePlaythroughsList = True

    if args.command == 'chase':
        customPrint('Playing games with increased ' + args.event + ' collection event rewards' + (' on ' + args.gamemode if args.gamemode else '') + (' on ' + args.category + ' maps' if args.category else '') + '!', infoType=InfoType.INFO)

        allAvailablePlaythroughs = filterAllAvailablePlaythroughs(allAvailablePlaythroughs, getMonkeyKnowledgeStatus(), handlePlaythroughValidation, categoryRestriction, gamemodeRestriction)
        allAvailablePlaythroughsList = allPlaythroughsToList(allAvailablePlaythroughs)

        originalObjectives.append({'type': State.MANAGE_OBJECTIVES})
        mode = Mode.CHASE_REWARDS
        usesAllAvailablePlaythroughsList = True

    # py replay.py achievements [achievement]
    # plays all achievement related playthroughs
    # if achievement is provided it just plays plays until said achievement is unlocked
    # userconfig.json can be used to specify which achievements have already been unlocked or to document progress(e. g. games won only using primary monkeys)
    # refer to userconfig.example.json for an example

    # py replay.py missing [category]
    # plays all playthroughs with missing medals
    # if category is not provided from easiest category to hardest
    # if category is provided in said category
    # requires userconfig.json to specify which medals have already been earned
    # unlocking of maps has do be done manually (Could potentially be done automatically)
    
    if args.command == 'xp':
        allAvailablePlaythroughsList = sortPlaythroughsByXPGain(allAvailablePlaythroughsList)[:args.n] #This should never be a problem since args.n defaults to 1 and we validated it to be non-negative

        originalObjectives.append({'type': State.MANAGE_OBJECTIVES})
        mode = Mode.XP_FARMING
        valueUnit = 'XP/h'
        usesAllAvailablePlaythroughsList = True

    if args.command == 'mm':
        allAvailablePlaythroughsList = sortPlaythroughsByMonkeyMoneyGain(allAvailablePlaythroughsList)[:args.n] 

        
        originalObjectives.append({'type': State.MANAGE_OBJECTIVES})
        mode = Mode.MM_FARMING
        valueUnit = 'MM/h'
        usesAllAvailablePlaythroughsList = True
    
    if args.command == 'validate':
        if args.repeat:
            repeatObjectives = False
            customPrint("Repeating playthroughs is unavailable with the selected mode! Disabling repeats", infoType=InfoType.WARN)

        if args.monkeyknowledge or getMonkeyKnowledgeStatus():
            customPrint('Validate only works with monkey knowledge disabled!',  infoType=InfoType.ERROR)
            return
        
        
        if args.validate_func == 'file':
            if not parseBTD6InstructionFileName(args.file.name): 
                customPrint('"' + args.file.name + '" can\'t be recognized as a playthrough filename! Exiting!', infoType=InfoType.ERROR)
                return
            fileConfig = parseBTD6InstructionFileName(args.file.name)
            allAvailablePlaythroughsList = [{'filename': filename, 'fileConfig': fileConfig, 'gamemode': fileConfig['gamemode', 'isOriginalGamemode': True]}]
        if args.validate_func == 'all':
            customPrint('Validating all playthroughs' + (' on ' + args.gamemode if args.gamemode else '') + (' on ' + args.category + ' maps' if args.category else '') + '!', infoType=InfoType.INFO)
            allAvailablePlaythroughs = filterAllAvailablePlaythroughs(
                    allAvailablePlaythroughs,
                    True,
                    ValidatedPlaythroughs.EXCLUDE_VALIDATED if handlePlaythroughValidation == ValidatedPlaythroughs.INCLUDE_ALL else ValidatedPlaythroughs.INCLUDE_ALL,
                    args.category,
                    args.gamemode,
                    onlyOriginalGamemodes=True)
            allAvailablePlaythroughsList = allPlaythroughsToList(allAvailablePlaythroughs)


        originalObjectives.append({'type': State.MANAGE_OBJECTIVES})
        usesAllAvailablePlaythroughsList = True
        mode = Mode.VALIDATE_PLAYTHROUGHS
    
    if args.command == 'costs':
        if args.mk or getMonkeyKnowledgeStatus():
            customPrint('Validating costs only works with monkey knowledge disabled!',  infoType=InfoType.ERROR)
            return
        customPrint('Validating monkey costs' + (' including heros' if args.hero else '') + '!', infoType=InfoType.INFO)

        allTestPositions = json.load(open('test_positions.json'))
        if getResolutionString() in allTestPositions:
            testPositions = allTestPositions(getResolutionString())
        else:
            testPositions = json.loads(convertPositionsInString(json.dumps(testPositions['2560x1440']), (2560, 1440), pyautogui.size()))

        selectedMap = None
        for mapname in testPositions:
            if getAvailableSandbox(mapname, ['medium_sandbox']):
                selectedMap = mapname
                break
        
        if selectedMap is None:
            customPrint('This mode requires access to medium sandbox for one of the maps in "test_positions.json"!', infoType = InfoType.ERROR)
            return
        
        costs = {'monkeys': {}}

        baseMapConfig = {'category': maps[selectedMap]['category'], 'map': selectedMap, 'page': maps[selectedMap]['page'], 'pos': maps[selectedMap]['pos'], 'difficulty': 'medium', 'gamemode': 'medium_sandbox', 'steps': [], 'extrainstructions': 1, 'filename': None}

        monkeySteps = []
        monkeySteps.append({'action': 'click', 'pos': imageAreas['click']['gamemode_deflation_message_confirmation'], 'cost': 0})
        pos = testPositions[selectedMap]
        pos['any'] = pos['land']
        for monkeyType in towers['monkeys']:
            costs['monkeys'][monkeyType] = {'base': 0, 'upgrades': np.zeros((3, 5))}
            for iPath in range(0, 3):
                monkeySteps.append({'action': 'place', 'type': monkeyType, 'name': f"{monkeyType}{iPath}", 'key': keybinds['monkeys'][monkeyType], 'pos': pos[towers['monkeys'][monkeyType]['class']], 'cost': 1, 'extra': {'group': 'monkeys', 'type': monkeyType}})
                for iUpgrade in range(1, 6):
                    monkeySteps.append({'action': 'upgrade', 'name': f"{monkeyType}{iPath}", 'key': keybinds['path'][str(iPath)], 'pos': pos[towers['monkeys'][monkeyType]['class']], 'path': iPath, 'cost': 1, 'extra': {'group': 'monkeys', 'type': monkeyType, 'upgrade': (iPath, iUpgrade)}})
                    if upgradeRequiresConfirmation({'type': monkeyType, 'upgrades': [(iUpgrade if iTmp == iPath else 0) for iTmp in range(0, 3)]}, iPath):
                        monkeySteps.append({'action': 'click', 'name': f"{monkeyType}{iPath}", 'pos': imageAreas['click']['paragon_message_confirmation'], 'cost': 0})
                monkeySteps.append({'action': 'sell', 'name': f"{monkeyType}{iPath}", 'key': keybinds['others']['sell'], 'pos': pos[towers['monkeys'][monkeyType]['class']], 'cost': -1})
        
        monkeyMapConfig = copy.deepcopy(baseMapConfig)
        monkeyMapConfig['steps'] = monkeySteps
        
        originalObjectives.append({'type': State.GOTO_HOME})
        originalObjectives.append({'type': State.GOTO_INGAME, 'mapConfig': monkeyMapConfig})
        originalObjectives.append({'type': State.INGAME, 'mapConfig': monkeyMapConfig})

        if args.hero:
            costs['heros'] = {}
            
            for hero in towers['heros']:
                costs['heros'][hero] = {'base' : 0}
                heroMapConfig = copy.deepcopy(baseMapConfig)
                heroMapConfig['hero'] = hero
                heroMapConfig['steps'] = [{'action': 'click', 'pos': imageAreas['click']['gamemode_deflation_message_confirmation'], 'cost': 0}, {'action': 'place', 'type': 'hero', 'name': 'hero0', 'key': keybinds['monkeys']['hero'], 'pos': pos[towers['heros'][hero]['class']], 'cost': 1, 'extra': {'group': 'heros', 'type': hero}}]
                originalObjectives.append({'type': State.GOTO_HOME})
                originalObjectives.append({'type': State.SELECT_HERO, 'mapConfig': heroMapConfig})
                originalObjectives.append({'type': State.GOTO_HOME})
                originalObjectives.append({'type': State.GOTO_INGAME, 'mapConfig': heroMapConfig})
                originalObjectives.append({'type': State.INGAME, 'mapConfig': heroMapConfig})

        originalObjectives.append({'type': State.MANAGE_OBJECTIVES})
        usesAllAvailablePlaythroughsList = False
        mode = Mode.VALIDATE_COSTS

        

    if mode == Mode.ERROR:
        customPrint('Invalid arguments! Exiting!', infoType=InfoType.ERROR)
        return

    if not mode.name in supportedModes:
        customPrint('Mode not supported due to missing images!', infoType=InfoType.ERROR)
        return

    if listAvailablePlaythroughs:
        if usesAllAvailablePlaythroughsList:
            customPrint(str(len(allAvailablePlaythroughsList)) + ' playthroughs found:', infoType=InfoType.INFO)
            for playthrough in allAvailablePlaythroughsList:
                customPrint(playthrough['filename'] + ': ' + playthrough['fileConfig']['map'] + ' - ' + playthrough['gamemode'] + (' with ' + str(playthrough['value']) + (' ' + valueUnit if len(valueUnit) else '') if 'value' in playthrough else ''))
        else:
            customPrint('Mode doesn\'t qualify for listing all available playthroughs', infoType=InfoType.ERROR)
        return

    if usesAllAvailablePlaythroughsList and len(allAvailablePlaythroughsList) == 0:
        customPrint('No playthroughs matching requirements found!', infoType=InfoType.ERROR)
        return

    keyboard.add_hotkey('ctrl+space', setExitAfterGame)

    objectives = copy.deepcopy(originalObjectives)
        
    state = objectives[0]['type']
    lastStateTransitionSuccessful = True
    objectiveFailed = False
    mapConfig = objectives[0]['mapConfig'] if 'mapConfig' in objectives[0] else None

    gamesPlayed = 0

    lastIterationBalance = -1
    lastIterationScreenshotAreas = []
    lastIterationCost = 0
    iterationBalances = []
    thisIterationAction = None
    lastIterationAction = None

    validationResult = None

    playthroughLog = {}

    lastHeroSelected = None

    increasedRewardsPlaythrough = None

    lastPlaythrough = None
    lastPlaythroughStats = {}

    lastScreen = Screen.UNKNOWN
    lastState = State.UNDEFINED

    unknownScreenHasWaited = False

    while True:
        screenshot = np.array(pyautogui.screenshot())[:, :, ::-1].copy()

        screen = Screen.UNKNOWN
        activeWindow = ahk.get_active_window()
        if not activeWindow or activeWindow.title.decode() != 'BloonsTD6':
            screen = Screen.BTD6_UNFOCUSED
        else:
            bestMatchDiff = None
            # TODO: not 100%, but would using smaller images make this more efficient?
            for screenCfg in [
                (Screen.STARTMENU, comparisonImages["screens"]["startmenu"], imageAreas["compare"]["screens"]["startmenu"]),
                (Screen.MAP_SELECTION, comparisonImages["screens"]["map_selection"], imageAreas["compare"]["screens"]["map_selection"]),
                (Screen.DIFFICULTY_SELECTION, comparisonImages["screens"]["difficulty_selection"], imageAreas["compare"]["screens"]["difficulty_selection"]),
                (Screen.GAMEMODE_SELECTION, comparisonImages["screens"]["gamemode_selection"], imageAreas["compare"]["screens"]["gamemode_selection"]),
                (Screen.HERO_SELECTION, comparisonImages["screens"]["hero_selection"], imageAreas["compare"]["screens"]["hero_selection"]),
                (Screen.INGAME, comparisonImages["screens"]["ingame"], imageAreas["compare"]["screens"]["ingame"]),
                (Screen.INGAME_PAUSED, comparisonImages["screens"]["ingame_paused"], imageAreas["compare"]["screens"]["ingame_paused"]),
                (Screen.VICTORY_SUMMARY, comparisonImages["screens"]["victory_summary"], imageAreas["compare"]["screens"]["victory_summary"]),
                (Screen.VICTORY, comparisonImages["screens"]["victory"], imageAreas["compare"]["screens"]["victory"]),
                (Screen.DEFEAT, comparisonImages["screens"]["defeat"], imageAreas["compare"]["screens"]["defeat"]),
                (Screen.OVERWRITE_SAVE, comparisonImages["screens"]["overwrite_save"], imageAreas["compare"]["screens"]["overwrite_save"]),
                (Screen.LEVELUP, comparisonImages["screens"]["levelup"], imageAreas["compare"]["screens"]["levelup"]),
                (Screen.APOPALYPSE_HINT, comparisonImages["screens"]["apopalypse_hint"], imageAreas["compare"]["screens"]["apopalypse_hint"]),
                (Screen.ROUND_100_INSTA, comparisonImages["screens"]["round_100_insta"], imageAreas["compare"]["screens"]["round_100_insta"]),
                (Screen.COLLECTION_CLAIM_CHEST, comparisonImages["screens"]["collection_claim_chest"], imageAreas["compare"]["screens"]["collection_claim_chest"]),
            ]:
                diff = cv2.matchTemplate(cutImage(screenshot, screenCfg[2]), cutImage(screenCfg[1], screenCfg[2]), cv2.TM_SQDIFF_NORMED)[0][0]
                if diff < 0.05 and (bestMatchDiff is None or diff < bestMatchDiff):
                    bestMatchDiff = diff
                    screen = screenCfg[0]

        if screen != lastScreen:
            customPrint("Screen " + screen.name + "!", infoType=InfoType.INFO)

        if screen == Screen.BTD6_UNFOCUSED:
            pass
        # don't do anything when ctrl is pressed: useful for alt + tab / sending SIGINT(ctrl + c) to the script
        elif keyboard.is_pressed('ctrl'):
            pass
        elif state == State.MANAGE_OBJECTIVES:
            customPrint("Entered objective management!", infoType=InfoType.INFO)
            
            if exitAfterGame:
                state = State.EXIT
                continue
            
            if mode == Mode.VALIDATE_PLAYTHROUGHS:
                if validationResult != None:
                    customPrint('Validation result: playthrough ' + lastPlaythrough['filename'] + ' is ' + ('valid' if validationResult else 'invalid') + '!',  infoType=InfoType.INFO)
                    updatePlaythroughValidationStatus(lastPlaythrough['filename'], validationResult)
                if len(allAvailablePlaythroughsList):
                    playthrough = allAvailablePlaythroughsList.pop(0)
                    customPrint('validation playthrough chosen: ' + playthrough['fileConfig']['map'] + ' on ' + playthrough['gamemode'] + ' (' + playthrough['filename'] + ')', infoType=InfoType.INFO)
                    
                    gamemode = getAvailableSandbox(playthrough['fileConfig']['map'])
                    if gamemode:
                        mapConfig = parseBTD6InstructionsFile(playthrough['filename'], gamemode=gamemode)
                        objectives = []
                        objectives.append({'type': State.GOTO_HOME})
                        if 'hero' in mapConfig and lastHeroSelected != mapConfig['hero']:
                            objectives.append({'type': State.SELECT_HERO, 'mapConfig': mapConfig})
                            objectives.append({'type': State.GOTO_HOME})
                        objectives.append({'type': State.GOTO_INGAME, 'mapConfig': mapConfig})
                        objectives.append({'type': State.INGAME, 'mapConfig': mapConfig})
                        objectives.append({'type': State.MANAGE_OBJECTIVES})

                        validationResult = True
                        lastPlaythrough = playthrough
                    else:
                        customPrint('Missing sandbox access for ' + playthrough['fileConfig']['map'], infoType=InfoType.WARN)
                        objectives = []
                        objectives.append({'type': State.MANAGE_OBJECTIVES})
                else:
                    objectives = []
                    objectives.append({'type': State.EXIT})
            elif mode == Mode.VALIDATE_COSTS:
                oldTowers = copy.deepcopy(towers)
                changes = 0
                for monkeyType in costs['monkeys']:
                    if costs['monkeys'][monkeyType]['base'] and costs['monkeys'][monkeyType]['base'] != oldTowers['monkeys'][monkeyType]['base']:
                        print(f"{monkeyType} base cost: {oldTowers['monkeys'][monkeyType]['base']} -> {costs['monkeys'][monkeyType]['base']}")
                        towers['monkeys'][monkeyType]['base'] = costs['monkeys'][monkeyType]['base']
                        changes += 1
                    for iPath in range(0, 3):
                        for iUpgrade in range(0, 5):
                            if costs['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade] and costs['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade] != oldTowers['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade]:
                                print(f"{monkeyType} path {iPath + 1} upgrade {iUpgrade + 1} cost: {oldTowers['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade]} -> {costs['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade]}")
                                towers['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade] = costs['monkeys'][monkeyType]['upgrades'][iPath][iUpgrade]
                                changes += 1
                if 'heros' in costs:
                    for hero in costs['heros']:
                        if costs['heros'][hero]['base'] and costs['heros'][hero]['base'] != oldTowers['heros'][hero]['base']:
                            print(f"hero {hero} base cost: {oldTowers['heros'][hero]['base']} -> {costs['heros'][hero]['base']}")
                            towers['heros'][hero]['base'] = costs['heros'][hero]['base']
                            changes += 1

                if changes:
                    print(f"updating \"towers.json\" with {changes}!")
                    fp = open('towers_backup.json', "w")
                    fp.write(json.dumps(oldTowers, indent=4))
                    fp.close()
                    fp = open('towers.json', "w")
                    fp.write(json.dumps(towers, indent=4))
                    fp.close()
                else:
                    print(f"no price changes in comparison to \"towers.json\" detected!")
                
                return
            elif repeatObjectives or gamesPlayed == 0:
                if mode == Mode.SINGLE_MAP:
                    objectives = copy.deepcopy(originalObjectives)
                elif mode == Mode.RANDOM_MAP or mode == Mode.XP_FARMING or mode == Mode.MM_FARMING:
                    objectives = []
                    playthrough = random.choice(allAvailablePlaythroughsList)
                    customPrint('Random playthrough chosen: ' + playthrough['fileConfig']['map'] + ' on ' + playthrough['gamemode'] + ' (' + playthrough['filename'] + ')', infoType=InfoType.INFO)
                    mapConfig = parseBTD6InstructionsFile(playthrough['filename'], gamemode=playthrough['gamemode'])
                    objectives.append({'type': State.GOTO_HOME})
                    if 'hero' in mapConfig and lastHeroSelected != mapConfig['hero']:
                        objectives.append({'type': State.SELECT_HERO, 'mapConfig': mapConfig})
                        objectives.append({'type': State.GOTO_HOME})
                    objectives.append({'type': State.GOTO_INGAME, 'mapConfig': mapConfig})
                    objectives.append({'type': State.INGAME, 'mapConfig': mapConfig})
                    objectives.append({'type': State.MANAGE_OBJECTIVES})
                    lastPlaythrough = playthrough
                elif mode == Mode.CHASE_REWARDS:
                    objectives = []
                    if increasedRewardsPlaythrough:
                        playthrough = increasedRewardsPlaythrough
                        customPrint('Highest reward playthrough chosen: ' + playthrough['fileConfig']['map'] + ' on ' + playthrough['gamemode'] + ' (' + playthrough['filename'] + ')', infoType=InfoType.INFO)
                        mapConfig = parseBTD6InstructionsFile(playthrough['filename'], gamemode=playthrough['gamemode'])

                        objectives.append({'type': State.GOTO_HOME})
                        if 'hero' in mapConfig and lastHeroSelected != mapConfig['hero']:
                            objectives.append({'type': State.SELECT_HERO, 'mapConfig': mapConfig})
                            objectives.append({'type': State.GOTO_HOME})
                        objectives.append({'type': State.GOTO_INGAME, 'mapConfig': mapConfig})
                        objectives.append({'type': State.INGAME, 'mapConfig': mapConfig})
                        objectives.append({'type': State.MANAGE_OBJECTIVES})
                        increasedRewardsPlaythrough = None
                        lastPlaythrough = playthrough
                    else:
                        objectives.append({'type': State.GOTO_HOME})
                        objectives.append({'type': State.FIND_HARDEST_INCREASED_REWARDS_MAP})
                        objectives.append({'type': State.MANAGE_OBJECTIVES})
                else:
                    objectives = copy.deepcopy(originalObjectives)
            else:
                objectives = []
                objectives.append({'type': State.EXIT})

            state = objectives[0]['type']
            lastStateTransitionSuccessful = True
            objectiveFailed = False
        elif state == State.UNDEFINED:
            customPrint("Entered state management!", infoType=InfoType.INFO)
            if exitAfterGame:
                state = State.EXIT
            if objectiveFailed:
                customPrint("Objective failed on step " + objectives[0]['type'].name + "(screen " + lastScreen.name + ")!", infoType=InfoType.WARN)
                if repeatObjectives:
                    state = State.MANAGE_OBJECTIVES
                else:
                    state = State.EXIT
            elif not lastStateTransitionSuccessful:
                state = objectives[0]['type']
                if 'mapConfig' in objectives[0]:
                    mapConfig = objectives[0]['mapConfig']
                lastStateTransitionSuccessful = True
            elif lastStateTransitionSuccessful and len(objectives):
                objectives.pop(0)
                state = objectives[0]['type']
                if 'mapConfig' in objectives[0]:
                    mapConfig = objectives[0]['mapConfig']
            else:
                state = State.EXIT
        elif state == State.IDLE:
            pass
        elif state == State.EXIT:
            customPrint("Goal EXIT! Exiting!", infoType=InfoType.INFO)
            return
        elif state == State.GOTO_HOME:
            if screen == Screen.STARTMENU:
                customPrint("Goal GOTO_HOME fullfilled!", infoType=InfoType.INFO)
                state = State.UNDEFINED
            elif screen == Screen.UNKNOWN:
                if lastScreen == Screen.UNKNOWN and unknownScreenHasWaited:
                    unknownScreenHasWaited = False
                    ahk.send_event('{Esc}')
                else:
                    unknownScreenHasWaited = True
                    time.sleep(2)
            elif screen == Screen.INGAME:
                ahk.send_event('{Esc}')
            elif screen == Screen.INGAME_PAUSED:
                pyautogui.click(imageAreas["click"]["screen_ingame_paused_button_home"])
            elif screen == Screen.HERO_SELECTION:
                ahk.send_event('{Esc}')
            elif screen == Screen.GAMEMODE_SELECTION:
                ahk.send_event('{Esc}')
            elif screen == Screen.DIFFICULTY_SELECTION:
                ahk.send_event('{Esc}')
            elif screen == Screen.MAP_SELECTION:
                ahk.send_event('{Esc}')
            elif screen == Screen.DEFEAT:
                result = cv2.matchTemplate(screenshot, locateImages['button_home'], cv2.TM_SQDIFF_NORMED)
                pyautogui.click(cv2.minMaxLoc(result)[2])
            elif screen == Screen.VICTORY_SUMMARY:
                pyautogui.click(imageAreas["click"]["screen_victory_summary_button_next"])
            elif screen == Screen.VICTORY:
                pyautogui.click(imageAreas["click"]["screen_victory_button_home"])
            elif screen == Screen.OVERWRITE_SAVE:
                ahk.send_event('{Esc}')
            elif screen == Screen.LEVELUP:
                pyautogui.click(100, 100)
                time.sleep(menuChangeDelay)
                pyautogui.click(100, 100)
            elif screen == Screen.ROUND_100_INSTA:
                pyautogui.click(100, 100)
                time.sleep(menuChangeDelay)
            elif screen == Screen.COLLECTION_CLAIM_CHEST:
                pyautogui.click(imageAreas["click"]["collection_claim_chest"])
                time.sleep(menuChangeDelay * 2)
                while True:
                    newScreenshot = np.array(pyautogui.screenshot())[:, :, ::-1].copy()
                    result = [cv2.minMaxLoc(cv2.matchTemplate(newScreenshot, locateImages['unknown_insta'], cv2.TM_SQDIFF_NORMED, mask=locateImages['unknown_insta_mask']))[i] for i in [0,2]]
                    if result[0] < 0.01:
                        pyautogui.click(result[1])
                        time.sleep(menuChangeDelay)
                        pyautogui.click(result[1])
                        time.sleep(menuChangeDelay)
                    else:
                        break
                pyautogui.click(round(resolution[0] / 2), round(resolution[1] / 2))
                time.sleep(menuChangeDelay)
                ahk.send_event('{Esc}')
            elif screen == Screen.APOPALYPSE_HINT:
                pyautogui.click(imageAreas["click"]["gamemode_apopalypse_message_confirmation"])
        elif state == State.GOTO_INGAME:
            if screen == Screen.STARTMENU:
                pyautogui.click(imageAreas["click"]["screen_startmenu_button_play"])
                time.sleep(menuChangeDelay)
                if mapConfig['category'] == 'beginner':
                    pyautogui.click(imageAreas["click"]["map_categories"]['advanced'])
                    time.sleep(menuChangeDelay)
                    pyautogui.click(imageAreas["click"]["map_categories"][mapConfig['category']])
                    time.sleep(menuChangeDelay)
                else:
                    pyautogui.click(imageAreas["click"]["map_categories"]['beginner'])
                    time.sleep(menuChangeDelay)
                    pyautogui.click(imageAreas["click"]["map_categories"][mapConfig['category']])
                    time.sleep(menuChangeDelay)
                tmpClicks = mapConfig['page']
                while tmpClicks > 0:
                    pyautogui.click(imageAreas["click"]["map_categories"][mapConfig['category']])
                    tmpClicks -= 1
                    time.sleep(menuChangeDelay)
                pyautogui.click(imageAreas["click"]["map_positions"][mapConfig['pos']])
                time.sleep(menuChangeDelay)
                pyautogui.click(imageAreas["click"]["gamedifficulty_positions"][mapConfig['difficulty']])
                time.sleep(menuChangeDelay)
                pyautogui.click(getGamemodePosition(mapConfig['gamemode']))
            elif screen == Screen.OVERWRITE_SAVE:
                pyautogui.click(imageAreas["click"]["screen_overwrite_save_button_ok"])
            elif screen == Screen.APOPALYPSE_HINT:
                pyautogui.click(imageAreas["click"]["gamemode_apopalypse_message_confirmation"])
            elif screen == Screen.INGAME:
                customPrint("Goal GOTO_INGAME fullfilled!", infoType=InfoType.INFO)
                customPrint("Game: " + mapConfig['map'] + ' - ' + mapConfig['difficulty'], infoType=InfoType.INFO)
                iterationBalances = []
                if logStats:
                    lastPlaythroughStats = {'gamemode': mapConfig['gamemode'], 'time': [], 'result': PlaythroughResult.UNDEFINED}
                    lastPlaythroughStats['time'].append(('start', time.time()))
                lastIterationBalance = -1
                lastIterationCost = 0
                state = State.UNDEFINED
            elif screen == Screen.UNKNOWN:
                pass
            else:
                customPrint("Task GOTO_INGAME, but not in Start Menu!", infoType=InfoType.WARN)
                state = State.GOTO_HOME
                lastStateTransitionSuccessful = False
        elif state == State.SELECT_HERO:
            if screen == Screen.STARTMENU:
                pyautogui.click(imageAreas["click"]["screen_startmenu_button_hero_selection"])
                time.sleep(menuChangeDelay)
                pyautogui.click(imageAreas["click"]["hero_positions"][mapConfig['hero']])
                time.sleep(menuChangeDelay)
                pyautogui.click(imageAreas["click"]["screen_hero_selection_select_hero"])
                customPrint("Goal SELECT_HERO " + mapConfig['hero'] + " fullfilled!", infoType=InfoType.INFO)
                lastHeroSelected = mapConfig['hero']
                state = State.UNDEFINED
            elif screen == Screen.UNKNOWN:
                pass
            else:
                customPrint("Task SELECT_HERO, but not in startmenu!", infoType=InfoType.WARN)
                state = State.GOTO_HOME
                lastStateTransitionSuccessful = False
        elif state == State.FIND_HARDEST_INCREASED_REWARDS_MAP:
            if screen == Screen.STARTMENU:
                pyautogui.click(imageAreas["click"]["screen_startmenu_button_play"])
                time.sleep(menuChangeDelay)

                if categoryRestriction:
                    pyautogui.click(imageAreas["click"]["map_categories"][('advanced' if categoryRestriction == 'beginner' else 'beginner')])
                    time.sleep(menuChangeDelay)

                    mapname = None
                    for page in range(0, categoryPages[categoryRestriction]):
                        pyautogui.click(imageAreas["click"]["map_categories"][categoryRestriction])
                        time.sleep(menuChangeDelay)
                        newScreenshot = np.array(pyautogui.screenshot())[:, :, ::-1].copy()
                        result = findImageInImage(newScreenshot, locateImages['collection'][collectionEvent])
                        if result[0] < 0.05:
                            mapname = findMapForPxPos(categoryRestriction, page, result[1])
                            break
                    if not mapname:
                        customPrint('No maps with increased rewards found! Exiting!', infoType=InfoType.ERROR)
                        return
                    customPrint('Best map: ' + mapname, infoType=InfoType.INFO)
                    increasedRewardsPlaythrough = getHighestValuePlaythrough(allAvailablePlaythroughs, mapname, playthroughLog)
                    if not increasedRewardsPlaythrough:
                        customPrint('No playthroughs for map found! Exiting!', infoType=InfoType.ERROR)
                        return
                else:
                    iTmp = 0
                    for category in reversed(list(mapsByCategory.keys())):
                        if iTmp == 0:
                            pyautogui.click(imageAreas["click"]["map_categories"][('advanced' if category == 'beginner' else 'beginner')])
                            time.sleep(menuChangeDelay)

                        mapname = None
                        for page in range(0, categoryPages[category]):
                            pyautogui.click(imageAreas["click"]["map_categories"][category])
                            time.sleep(menuChangeDelay)
                            newScreenshot = np.array(pyautogui.screenshot())[:, :, ::-1].copy()
                            result = findImageInImage(newScreenshot, locateImages['collection'][collectionEvent])
                            if result[0] < 0.05:
                                mapname = findMapForPxPos(category, page, result[1])
                                break
                        if not mapname:
                            customPrint('No maps with increased rewards found! Exiting!', infoType=InfoType.ERROR)
                            return
                        customPrint('Best map in ' + category + ': ' + mapname, infoType=InfoType.INFO)
                        increasedRewardsPlaythrough = getHighestValuePlaythrough(allAvailablePlaythroughs, mapname, playthroughLog)
                        if increasedRewardsPlaythrough:
                            break
                        else:
                            customPrint('No playthroughs for map found! Searching lower map tiers!', infoType=InfoType.WARN)
                        iTmp += 1
                    
                    if not increasedRewardsPlaythrough:
                        customPrint('No available playthrough found! Exiting!', infoType=InfoType.ERROR)
                        return
                state = State.UNDEFINED
            elif screen == Screen.UNKNOWN:
                pass
            else:
                customPrint("Task FIND_HARDEST_INCREASED_REWARDS_MAP, but not in startmenu!", infoType=InfoType.WARN)
                state = State.GOTO_HOME
                lastStateTransitionSuccessful = False
        elif state == State.INGAME:
            if screen == Screen.INGAME_PAUSED:
                if lastScreen != screen and logStats:
                    lastPlaythroughStats['time'].append(('stop', time.time()))
                time.sleep(2)
                if ahk.get_active_window().title.decode() == 'BloonsTD6':
                    ahk.send_event('{Esc}')
            elif screen == Screen.UNKNOWN:
                if lastScreen == Screen.UNKNOWN and unknownScreenHasWaited:
                    unknownScreenHasWaited = False
                    ahk.send_event('{Esc}')
                else:
                    unknownScreenHasWaited = True
                    time.sleep(2)
            elif screen == Screen.LEVELUP:
                pyautogui.click(100, 100)
                time.sleep(menuChangeDelay)
                pyautogui.click(100, 100)
            elif screen == Screen.ROUND_100_INSTA:
                pyautogui.click(100, 100)
                time.sleep(menuChangeDelay)
            elif screen == Screen.VICTORY_SUMMARY:
                if logStats:
                    lastPlaythroughStats['time'].append(('stop', time.time()))
                    lastPlaythroughStats['result'] = PlaythroughResult.WIN
                    updateStatsFile(mapConfig['filename'], lastPlaythroughStats)
                gamesPlayed += 1
                if not mapConfig['filename'] in playthroughLog:
                    playthroughLog[mapConfig['filename']] = {}
                if not mapConfig['gamemode'] in playthroughLog[mapConfig['filename']]:
                    playthroughLog[mapConfig['filename']][mapConfig['gamemode']] = {'attempts': 0, 'wins': 0, 'defeats': 0}
                playthroughLog[mapConfig['filename']][mapConfig['gamemode']]['attempts'] += 1
                playthroughLog[mapConfig['filename']][mapConfig['gamemode']]['wins'] += 1

                if not isContinue:
                    updateMedalStatus(mapConfig['map'], mapConfig['gamemode'])
                
                state = State.UNDEFINED
            elif screen == Screen.DEFEAT:
                if logStats:
                    lastPlaythroughStats['time'].append(('stop', time.time()))
                    lastPlaythroughStats['result'] = PlaythroughResult.DEFEAT
                    updateStatsFile(mapConfig['filename'], lastPlaythroughStats)
                objectiveFailed = True
                gamesPlayed += 1
                if not mapConfig['filename'] in playthroughLog:
                    playthroughLog[mapConfig['filename']] = {}
                if not mapConfig['gamemode'] in playthroughLog[mapConfig['filename']]:
                    playthroughLog[mapConfig['filename']][mapConfig['gamemode']] = {'attempts': 0, 'wins': 0, 'defeats': 0}
                playthroughLog[mapConfig['filename']][mapConfig['gamemode']]['attempts'] += 1
                playthroughLog[mapConfig['filename']][mapConfig['gamemode']]['defeats'] += 1
                
                state = State.UNDEFINED
            elif screen == Screen.INGAME:
                if lastScreen != screen and logStats:
                    lastPlaythroughStats['time'].append(('start', time.time()))

                images = [
                    screenshot[segmentCoordinates[segment][1]:segmentCoordinates[segment][3], segmentCoordinates[segment][0]:segmentCoordinates[segment][2]] for segment in segmentCoordinates
                ]

                currentValues = {}
                thisIterationCost = 0
                thisIterationAction = None
                skippingIteration = False

                currentValues['money'] = custom_ocr(images[2])
                
                # to prevent random explosion particles that were recognized as digits from messing up the game
                # still possible: if it habens 2 times in a row
                # potential solution: when placing: check if pixel changed colour(or even is of correct colour) - potentially blocked by particles/projectiles
                # when upgrading: check if corresponding box turned green(for left and right menu)
                # remove obstacle: colour change?

                if len(mapConfig['steps']):
                    if mapConfig['steps'][0]['action'] == 'sell':
                        customPrint('Detected money: ' + str(currentValues['money']) + ', required: ' + str(getNextNonSellAction(mapConfig['steps'])['cost'] - sumAdjacentSells(mapConfig['steps'])) + ' (' + str(getNextNonSellAction(mapConfig['steps'])['cost']) + ' - ' + str(sumAdjacentSells(mapConfig['steps'])) + ')' + '          ', end = '', rewriteLine=True, infoType=InfoType.INFO)
                    else:
                        customPrint('Detected money: ' + str(currentValues['money']) + ', required: ' + str(mapConfig['steps'][0]['cost']) + '          ', end = '', rewriteLine=True, infoType=InfoType.INFO)

                if mode == Mode.VALIDATE_PLAYTHROUGHS:
                    if lastIterationBalance != -1 and currentValues['money'] != lastIterationBalance - lastIterationCost:
                        if currentValues['money'] == lastIterationBalance:
                            customPrint('Action: ' + str(lastIterationAction) + ' failed!', infoType=InfoType.WARN)
                            validationResult = False
                            mapConfig['steps'] = []
                        else:
                            customPrint('Pricing error! expected cost: ' + str(lastIterationCost) + ', detected cost: ' + str(lastIterationBalance - currentValues['money']) + '. Is monkey knowledge disabled?', infoType=InfoType.WARN)
                elif mode == Mode.VALIDATE_COSTS:
                    if lastIterationBalance != -1 and lastIterationAction:
                        if lastIterationAction['action'] == 'place':
                            costs[lastIterationAction['extra']['group']][lastIterationAction['extra']['type']]['base'] = lastIterationBalance - currentValues['money']
                        elif lastIterationAction['action'] == 'upgrade':
                            costs[lastIterationAction['extra']['group']][lastIterationAction['extra']['type']]['upgrades'][lastIterationAction['extra']['upgrade'][0]][lastIterationAction['extra']['upgrade'][1] - 1] = lastIterationBalance - currentValues['money']

                if currentValues['money'] == -1:
                    pass
                elif mode != Mode.VALIDATE_COSTS and lastIterationBalance - lastIterationCost > currentValues['money']:
                    customPrint('Potential recognition error: ' + str(lastIterationBalance) + ' - ' + str(lastIterationCost) + ' -> ' + str(currentValues['money']), infoType=InfoType.WARN)
                    # cv2.imwrite('tmp_images/' + time.strftime("%Y-%m-%d_%H-%M-%S") + '_' + str(lastIterationBalance) + '.png', lastIterationScreenshotAreas[2])
                    # cv2.imwrite('tmp_images/' + time.strftime("%Y-%m-%d_%H-%M-%S") + '_' + str(currentValues['money']) + '.png', images[2])
                    skippingIteration = True
                elif len(mapConfig['steps']) and ((mapConfig['steps'][0]['action'] != 'sell' and min(currentValues['money'], lastIterationBalance - lastIterationCost) >= mapConfig['steps'][0]['cost']) 
                or mapConfig['gamemode'] == 'deflation' 
                or (mapConfig['steps'][0]['action'] == 'sell' and min(currentValues['money'], lastIterationBalance - lastIterationCost) + sumAdjacentSells(mapConfig['steps']) >= getNextNonSellAction(mapConfig['steps'])['cost'])):
                    action = mapConfig['steps'].pop(0)
                    thisIterationAction = action
                    if action['action'] != 'sell':
                        thisIterationCost = action['cost']
                    customPrint('Performing action: ' + str(action), infoType=InfoType.ACTION)
                    if action['action'] == 'place':
                        pyautogui.moveTo(action['pos'])
                        time.sleep(actionDelay)
                        ahk.send_event(keyToAHK(action['key']))
                        time.sleep(actionDelay)
                        pyautogui.click()
                    elif action['action'] == 'upgrade' or action['action'] == 'retarget' or action['action'] == 'special':
                        # game hints potentially blocking monkeys
                        pyautogui.click(action['pos'])
                        time.sleep(actionDelay)
                        actionTmp = None
                        while action:
                            if 'to' in action:
                                pyautogui.moveTo(action['to'])
                                time.sleep(smallActionDelay)
                            if action['action'] == 'click':
                                time.sleep(actionDelay)
                                pyautogui.moveTo(action['pos'])
                                pyautogui.click()
                                time.sleep(actionDelay)
                            else:
                                ahk.send_event(keyToAHK(action['key']))
                            if 'to' in action and mapConfig['monkeys'][action['name']]['type'] == 'mortar':
                                pyautogui.click()
                            time.sleep(smallActionDelay)
                            actionTmp = action
                            if len(mapConfig['steps']) and 'name' in mapConfig['steps'][0] and mapConfig['steps'][0]['name'] == action['name'] and (mapConfig['steps'][0]['action'] == 'retarget' or mapConfig['steps'][0]['action'] == 'special' or mapConfig['steps'][0]['action'] == 'click'):
                                action = mapConfig['steps'].pop(0)
                                customPrint('+' + action['action'], infoType=InfoType.ACTION)
                            else:
                                action = None
                        action = actionTmp
                        ahk.send_event('{Esc}')
                    elif action['action'] == 'sell':
                        pyautogui.moveTo(action['pos'])
                        pyautogui.click()
                        time.sleep(actionDelay)
                        ahk.send_event(keyToAHK(action['key']))
                    elif action['action'] == 'remove':
                        customPrint('Removing obstacle at ' + tupleToStr(action['pos']) + ' for ' + str(action['cost']),infoType=InfoType.ACTION)
                        pyautogui.moveTo(action['pos'])
                        pyautogui.click()
                        time.sleep(menuChangeDelay)
                        result = cv2.matchTemplate(np.array(pyautogui.screenshot())[:, :, ::-1].copy(), locateImages['remove_obstacle_confirm_button'], cv2.TM_SQDIFF_NORMED)
                        pyautogui.click(cv2.minMaxLoc(result)[2])
                    elif action['action'] == 'click':
                        pyautogui.moveTo(action['pos'])
                        pyautogui.click()
                    elif action['action'] == 'press':
                        ahk.send_event(keyToAHK(action['key']))
                elif mode in [Mode.VALIDATE_PLAYTHROUGHS, Mode.VALIDATE_COSTS] and len(mapConfig['steps']) == 0 and lastIterationCost == 0:
                    state = State.UNDEFINED

                if (not doAllStepsBeforeStart and mapConfig['gamemode'] != 'deflation' and not skippingIteration) or len(mapConfig['steps']) == 0:
                    bestMatchDiff = None
                    gameState = None
                    for screenCfg in [
                        ('game_playing_fast', comparisonImages['game_state']['game_playing_fast'], imageAreas["compare"]["game_state"]),
                        ('game_playing_slow', comparisonImages['game_state']['game_playing_slow'], imageAreas["compare"]["game_state"]),
                        ('game_paused', comparisonImages['game_state']['game_paused'], imageAreas["compare"]["game_state"]),
                    ]:
                        diff = cv2.matchTemplate(cutImage(screenshot, screenCfg[2]), cutImage(screenCfg[1], screenCfg[2]), cv2.TM_SQDIFF_NORMED)[0][0]
                        if bestMatchDiff is None or diff < bestMatchDiff:
                            bestMatchDiff = diff
                            gameState = screenCfg[0]

                    if gameState == 'game_playing_fast':
                        pass
                    elif gameState == 'game_playing_slow':
                        ahk.send_event(keybinds['others']['play'])
                    elif gameState == 'game_paused':
                        ahk.send_event(keybinds['others']['play'])
                    
                lastIterationScreenshotAreas = images
                lastIterationBalance = currentValues['money']
                lastIterationCost = thisIterationCost
                lastIterationAction = thisIterationAction

                iterationBalances.append((currentValues['money'], thisIterationCost))
            else:
                customPrint("Task INGAME, but not in related screen!",infoType=InfoType.WARN)
                state = State.GOTO_HOME
                lastStateTransitionSuccessful = False
        else:
            state = State.UNDEFINED
            lastStateTransitionSuccessful = False

        if state != lastState:
            customPrint("New state " + state.name + "!",infoType=InfoType.INFO)

        lastScreen = screen
        lastState = state

        time.sleep(actionDelay if state == State.INGAME else menuChangeDelay)

if __name__ == "__main__":
    main()