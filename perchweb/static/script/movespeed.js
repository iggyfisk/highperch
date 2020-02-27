const heroSpeeds = {
    "Hamg": { "name": "Archmage", "ms": 320 },
    "Hblm": { "name": "Blood Mage", "ms": 300 },
    "Hmkg": { "name": "Mountain King", "ms": 290 },
    "Hpal": { "name": "Paladin", "ms": 290 },
    "Obla": { "name": "Blademaster", "ms": 320 },
    "Ofar": { "name": "Far Seer", "ms": 320 },
    "Oshd": { "name": "Shadow Hunter", "ms": 320 },
    "Otch": { "name": "Tauren Chieftain", "ms": 290 },
    "Edem": { "name": "Demon Hunter", "ms": 320 },
    "Ekee": { "name": "Keeper of the Grove", "ms": 320 },
    "Emoo": { "name": "Priestess of the Moon", "ms": 320 },
    "Ewar": { "name": "Warden", "ms": 320 },
    "Ucrl": { "name": "Crypt Lord", "ms": 290 },
    "Udea": { "name": "Death Knight", "ms": 320 },
    "Udre": { "name": "Dreadlord", "ms": 290 },
    "Ulic": { "name": "Lich", "ms": 290 },
    "Nngs": { "name": "Naga Sea Witch", "ms": 290 },
    "Nbrn": { "name": "Dark Ranger", "ms": 320 },
    "Npbm": { "name": "Pandaren Brewmaster", "ms": 290 },
    "Nfir": { "name": "Firelord", "ms": 320 },
    "Nplh": { "name": "Pit Lord", "ms": 300 },
    "Nbst": { "name": "Beastmaster", "ms": 320 },
    "Ntin": { "name": "Tinker", "ms": 290 },
    "Nalc": { "name": "Goblin Alchemist", "ms": 290 },
};

const pctBuffValues = {
    "enduranceaura1": 10,
    "enduranceaura2": 20,
    "enduranceaura3": 30,
    "unholyaura1": 10,
    "unholyaura2": 20,
    "unholyaura3": 30,
    "windwalk1": 10,
    "windwalk2": 40,
    "windwalk3": 70,
    "engineering1": 10,
    "engineering2": 20,
    "engineering3": 30,
    "bloodlust": 25
};

const setBuffValues = {
    "scrollofspeed": 400,
    "chemicalrage": 406
};

const flatBuffValues = {
    "bootsofspeed": 60
};

const breakLimitBuffs = [
    "windwalk1",
    "windwalk2",
    "windwalk3",
    "chemicalrage"
];

const requiredHero = {
    "windwalk1": "Obla",
    "windwalk2": "Obla",
    "windwalk3": "Obla",
    "engineering1": "Ntin",
    "engineering2": "Ntin",
    "engineering3": "Ntin",
    "chemicalrage": "Nalc"
};

const speedName = moveSpeed => {    // returns [Plaintext, classname]
    if (moveSpeed <= 175) {
        return ['Very slow', 'veryslow'];
    } else if (moveSpeed > 175 && moveSpeed <= 220) {
        return ['Slow', 'slow'];
    } else if (moveSpeed > 220 && moveSpeed <= 280) {
        return ['Normal', 'normal'];
    } else if (moveSpeed > 280 && moveSpeed <= 350) {
        return ['Fast', 'fast'];
    } else if (moveSpeed > 350) {
        return ['Very Fast', 'veryfast'];
    }
}

let baseSpeed = 0;
let pctBuffs = [];
let setBuffs = [];
let flatBuffs = [];

const calcSpeed = () => {
    let moveSpeed = baseSpeed;
    let theoreticalSpeed = 0;
    let breakLimit = false;

    setBuffs.forEach(buff => {
        if (moveSpeed < setBuffValues[buff]) {
            moveSpeed = setBuffValues[buff];
        }
        if (breakLimitBuffs.includes(buff)) {
            breakLimit = true;
        }
    });

    flatBuffs.forEach(buff => {
        moveSpeed += flatBuffValues[buff];
    })

    let totalPercentBuff = 0;
    pctBuffs.forEach(buff => {
        totalPercentBuff += pctBuffValues[buff] / 100;
        if (breakLimitBuffs.includes(buff)) {
            breakLimit = true;
        }
    });
    moveSpeed *= (1 + totalPercentBuff);

    if (!breakLimit && moveSpeed > 400) {
        theoreticalSpeed = moveSpeed;
        moveSpeed = 400;
    } else if (breakLimit && moveSpeed > 522) {
        theoreticalSpeed = moveSpeed;
        moveSpeed = 522;
    }
    return [Math.round(moveSpeed), Math.round(theoreticalSpeed)];
}

const grayOutBuffs = selectedHero => {
    document.querySelectorAll('.buff').forEach(elem => {
        const buffName = elem.dataset.buff;
        if (buffName in requiredHero) {
            if (requiredHero[buffName] !== selectedHero) {
                elem.classList.add('grayedout');
            } else {
                elem.classList.remove('grayedout');
            }
        }
    });
}

const toggleBuffButton = selectedBuff => {
    const buffButton = document.querySelectorAll("[data-buff=" + selectedBuff + "]")[0]
    buffButton.classList.toggle('selected');
}

const handleGroupBuff = (selectedBuff, buffGroup) => {
    allPctBuffs = document.querySelectorAll('.pctbuff');
    allPctBuffs.forEach(elem => {
        if (!elem.dataset.buffgroup === buffGroup) {
            return;
        } else if (elem.dataset.buff === selectedBuff) {
            return;
        } else if (elem.dataset.buffgroup === buffGroup) {
            pctBuffs = pctBuffs.filter(e => e !== elem.dataset.buff);
            elem.classList.remove('selected');
            deleteBuffFromDisplayList(elem.dataset.buff);
            toggleBuffButton(selectedBuff);
        }
    });
}

const toggleBuff = (selectedBuff, selectedBuffGroup, selectedBuffType, displayDiv) => {
    if (selectedBuffType === 'setbuff') {
        if (setBuffs.includes(selectedBuff)) {
            setBuffs = setBuffs.filter(e => e !== selectedBuff)
            deleteBuffFromDisplayList(selectedBuff);
        } else {
            setBuffs.push(selectedBuff);
            addBuffToDisplayList(selectedBuff, displayDiv, 'set');
        }
    } else if (selectedBuffType === 'pctbuff') {
        if (pctBuffs.includes(selectedBuff)) {
            pctBuffs = pctBuffs.filter(e => e !== selectedBuff);
            deleteBuffFromDisplayList(selectedBuff);
        } else {
            handleGroupBuff(selectedBuff, selectedBuffGroup);
            pctBuffs.push(selectedBuff);
            addBuffToDisplayList(selectedBuff, displayDiv, 'pct');
        }
    } else if (selectedBuffType === 'flatbuff') {
        if (flatBuffs.includes(selectedBuff)) {
            flatBuffs = flatBuffs.filter(e => e !== selectedBuff);
            deleteBuffFromDisplayList(selectedBuff);
        } else {
            flatBuffs.push(selectedBuff);
            addBuffToDisplayList(selectedBuff, displayDiv, 'flat');
        }
    }
    toggleBuffButton(selectedBuff);
}

const resetHeroRequiredBuffs = () => {
    document.querySelectorAll('.grayedout').forEach(elem => {
        if (elem.classList.contains('selected')) {
            toggleBuff(elem.dataset.buff, elem.dataset.buffgroup);
            setBuffs.forEach(buff => {
                if (elem.dataset.buff === buff) {
                    setBuffs = setBuffs.filter(e => e !== buff);
                    deleteBuffFromDisplayList(buff);
                }
            });
            pctBuffs.forEach(buff => {
                if (elem.dataset.buff === buff) {
                    pctBuffs = pctBuffs.filter(e => e !== buff);
                    deleteBuffFromDisplayList(buff);
                }
            });
        }
    });
}

const writeSpeed = () => {
    if (baseSpeed === 0) {
        return;
    }
    const moveSpeed = calcSpeed()[0];
    const theoreticalSpeed = calcSpeed()[1];
    const speedReadout = document.getElementById('movespeed');
    const speedClass = document.getElementById('speedclass');
    const theoreticalReadout = document.getElementById('theoretical');
    speedReadout.value = moveSpeed;
    speedClass.innerHTML = speedName(moveSpeed)[0];
    speedClass.className = speedName(moveSpeed)[1];
    if (theoreticalSpeed > moveSpeed) {
        theoreticalReadout.className = '';
        theoreticalReadout.innerHTML = '(Speed cap hit - theoretical speed ' + theoreticalSpeed + ')';
    } else {
        theoreticalReadout.className = 'hidden';
        theoreticalReadout.innerHTML = '&nbsp;';
    }
}

const addBuffToDisplayList = (selectedBuff, displayDiv, buffType) => {
    const buffDiv = document.createElement("div");
    buffDiv.id = selectedBuff + '-display';
    buffDiv.className = 'listbuff';
    const buffImg = new Image();
    buffImg.src = '/static/images/game/speedbuffs/' + selectedBuff + '.png'
    buffText = document.createElement("span");
    buffText.className = 'listbufftext';
    if (buffType === 'set') {
        buffText.append(document.createTextNode('Base movespeed set to ' + setBuffValues[selectedBuff]));
    } else if (buffType === 'pct') {
        buffText.append(document.createTextNode('+' + pctBuffValues[selectedBuff] + '%'));
    } else if (buffType === 'flat') {
        buffText.append(document.createTextNode('+' + flatBuffValues[selectedBuff]));
    }
    buffDiv.appendChild(buffImg);
    buffDiv.append(buffText);
    displayDiv.appendChild(buffDiv);
}

const deleteBuffFromDisplayList = (selectedBuff) => {
    const buffDiv = document.getElementById(selectedBuff + '-display');
    if (buffDiv) {
        buffDiv.parentNode.removeChild(buffDiv);
    }
}

(() => {
    document.addEventListener("DOMContentLoaded", () => {
        const heroIconDiv = document.getElementById('heroicon');
        const heroNameDiv = document.getElementById('heroname');
        const currentBuffsDiv = document.getElementById('currentbuffs');
        let selectedHero = null;
        grayOutBuffs(selectedHero);
        heroNameDiv.innerHTML = 'Pick a hero!';
        const selectedHeroImg = new Image();
        selectedHeroImg.src = '/static/images/question.png';
        heroIconDiv.appendChild(selectedHeroImg);

        document.querySelectorAll('.hero').forEach(elem => {
            elem.addEventListener('click', event => {
                selectedHero = elem.dataset.unit;
                baseSpeed = heroSpeeds[selectedHero].ms;
                selectedHeroImg.src = elem.src;
                heroNameDiv.innerHTML = heroSpeeds[selectedHero].name;
                grayOutBuffs(selectedHero);
                resetHeroRequiredBuffs();
                writeSpeed();
            });
        });

        document.querySelectorAll('.setbuff').forEach(elem => {
            elem.addEventListener('click', event => {
                if (!elem.classList.contains('grayedout') && selectedHero) {
                    toggleBuff(elem.dataset.buff, elem.dataset.buffgroup, 'setbuff', currentBuffsDiv);
                    writeSpeed();
                }
            });
        });

        document.querySelectorAll('.pctbuff').forEach(elem => {
            elem.addEventListener('click', event => {
                if (!elem.classList.contains('grayedout') && selectedHero) {
                    toggleBuff(elem.dataset.buff, elem.dataset.buffgroup, 'pctbuff', currentBuffsDiv);
                    writeSpeed();
                }
            });
        });

        document.querySelectorAll('.flatbuff').forEach(elem => {
            elem.addEventListener('click', event => {
                if (!elem.classList.contains('grayedout') && selectedHero) {
                    toggleBuff(elem.dataset.buff, elem.dataset.buffgroup, 'flatbuff', currentBuffsDiv);
                    writeSpeed();
                }
            });
        });
    });
})();
