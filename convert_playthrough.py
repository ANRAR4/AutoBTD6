from helper import *

if len(sys.argv) < 3 or not re.search(r"\d+x\d+", sys.argv[2]):
    print("Usage: py", sys.argv[0], "<filename> <resolution(e. g. 1920x1080)>")
    exit()

if convertBTD6InstructionsFile(sys.argv[1], [int(x) for x in sys.argv[2].split("x")]):
    print(sys.argv[1], "converted successfully!")
else:
    print("invalid filename or file not existing!")
