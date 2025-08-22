from flask import Flask, request, render_template
from time import time
from random import randint, seed
from math import floor

randomTitles = [
    ":ta:",
    "emoji ta",
    "*paws at you*",
    "powered by femboys",
    ":3"
]

def rollDice(dice: str):
    spliced = dice.split("d")
    amount = int(spliced[0])
    side = int(spliced[1])
    total = 0
    for _ in range(amount):
        total += randint(1, side)
    return total

def getRandomTitle():
    return randomTitles[randint(0, len(randomTitles)-1)]

app = Flask(__name__)

@app.route('/')
def home():
    title = getRandomTitle()
    return render_template("index.html", resultData=None, title=title)
    
@app.route("/attack")
def attack_page():
    title = getRandomTitle()
    return render_template("attack.html", resultData=None, title=title)

@app.route("/attack", methods=["POST"])
def attack_post():
    title = getRandomTitle()

    attackDamage = request.form["attackDamage"]
    flatBonusDamage = request.form["flatBonusDamage"]
    attackAmount = request.form["attackAmount"]

    armorClass = request.form.get("armorClass")
    flatBonusArmor = request.form.get("flatBonusArmor")
    armorClassAdvantage = request.form.get("armorClassAdvantage")

    # currentSeed = floor(time)
    # seed(currentSeed)
    
    attackDamages = attackDamage.split(" ")

    flatBonusDamage = int(flatBonusDamage)
    attackAmount = int(attackAmount)

    attackRolls = []
    attackRawRolls = []
    armorRolls = []
    armorRawRolls = []

    # Roll attack dice
    for _ in range(attackAmount):
        for dice in attackDamages:
            attackRawRolls.append(rollDice(dice) + flatBonusDamage) 

    # if armor class
    if armorClass and flatBonusArmor and armorClassAdvantage:
        armorClass = int(armorClass)
        flatBonusArmor = int(flatBonusArmor)
        armorClassAdvantage = int(armorClassAdvantage)

        for i in range(attackAmount):
            armorRawRolls.append([])
            for _ in range(1 + abs(armorClassAdvantage)):
                armorRawRolls[i].append(rollDice("1d20") + flatBonusArmor)
        
        # pick based on advantage  
        for rolls in armorRawRolls:
            armorRolls.append(min(rolls) if armorClassAdvantage < 0 else max(rolls))
        
        # filter out the attack rolls to final rolls
        for index in range(len(armorRolls)):
            roll = armorRolls[index]
            if roll > armorClass:
                attackRolls.append(attackRawRolls[index])
            else:
                attackRolls.append(0)
                
    else:
        attackRolls = attackRawRolls
    
    resultData = []
    resultData.append("=====================================")
    resultData.append(f"Attack Damage: {attackDamage}")
    resultData.append(f"Flat Bonus Damage: {flatBonusDamage}")
    resultData.append(f"Attack Amount: {attackAmount}")
    resultData.append("=====================================")
    resultData.append(f"Armor Class Check: {armorClass != None}")
    if armorClass != None and flatBonusArmor != None and armorClassAdvantage != None:
        resultData.append(f"Armor Class: {armorClass}")
        resultData.append(f"Flat Bonus Armor: {flatBonusDamage}")
        resultData.append(f"Advantage: {"+" if armorClassAdvantage > 0 else "-" if armorClassAdvantage < 0 else ""}{armorClassAdvantage}")
        resultData.append(f"Raw Rolls: {armorRawRolls}")
        resultData.append(f"Advantaged rolls: {armorRolls}")
    resultData.append("=====================================")
    resultData.append(f"Raw Attack Rolls: {attackRawRolls}")
    resultData.append(f"Attack Rolls: {attackRolls}")
    resultData.append(f"Total damage: {sum(attackRolls)}")
    resultData.append("=====================================")

    return render_template("attack.html", resultData=resultData, title=title)

@app.route("/check")
def check_page():
    title = getRandomTitle()
    return render_template("check.html", resultData=None, title=title)

@app.route("/check", methods=["POST"])
def check_post():
    title = getRandomTitle()

    advantageRoll = request.form["advantageRoll"]
    flatBonus = request.form["flatBonus"]

    advantageRoll = int(advantageRoll)
    flatBonus = int(flatBonus)

    checkRoll = 0
    checkRawRolls = []

    for _ in range(1 + abs(advantageRoll)):
        checkRawRolls.append(rollDice("1d20") + flatBonus)
    
    # pick based on advantage  
    checkRoll = min(checkRawRolls) if advantageRoll < 0 else max(checkRawRolls)

    resultData = []
    resultData.append("=====================================")
    resultData.append(f"Advantage: {"+" if advantageRoll > 0 else "-" if advantageRoll < 0 else ""}{advantageRoll}")
    resultData.append(f"Flat Bonus: {flatBonus}")
    resultData.append("=====================================")
    resultData.append(f"Raw check rolls: {checkRawRolls}")
    resultData.append(f"Check roll: {checkRoll}")
    resultData.append("=====================================")

    return render_template("check.html", resultData=resultData, title=title)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)