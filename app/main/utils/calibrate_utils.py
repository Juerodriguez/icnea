import json

async def updateCalibrateStatus(newStatus):
    with open('/code/./app/main/calibrateFile.json', 'r') as f:
        calibrateFile = json.load(f)
    calibrateFile['calibrateStatus'] = newStatus
    with open('/code/./app/main/calibrateFile.json', 'w') as f:
        json.dump(calibrateFile, f)


async def readCalibrateStatus():
    with open('/code/./app/main/calibrateFile.json', 'r') as f:
        calibrateFile = json.load(f)
    return calibrateFile['calibrateStatus']