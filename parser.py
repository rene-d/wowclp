import sys
import csv
import logging
import itertools


events = {
    #
    "PARTY_KILL": 0,  # source: killer, dest: killed
    "UNIT_DIED": 0,  # source: nil
    "UNIT_DESTROYED": 0,  # source: nil
    #
    "ENVIRONMENTAL_DAMAGE": 27,
    "SPELL_DAMAGE": 29,
    "SPELL_PERIODIC_DAMAGE": 29,
    "SWING_DAMAGE": 26,
    "RANGE_DAMAGE": 29,
    #
    "SPELL_HEAL": 24,
    "SPELL_PERIODIC_HEAL": 24,
    #
    "SPELL_MISSED": [5, 6, 7],
    "SWING_MISSED": [2, 3, 4],
    "RANGE_MISSED": [5, 6, 7],
    #
    "SPELL_AURA_APPLIED": 4,
    "SPELL_AURA_REMOVED": 4,
    "SPELL_AURA_BROKEN": 4,
    "SPELL_AURA_BROKEN_SPELL": 7,
    "SPELL_AURA_APPLIED_DOSE": 5,
    "SPELL_AURA_REMOVED_DOSE": 5,
    "SPELL_AURA_REFRESH": 4,
    #
    "SPELL_CAST_START": 3,
    "SPELL_CAST_SUCCESS": 19,
    "SPELL_CAST_FAILED": 4,
    #
    "SPELL_ABSORBED": [9, 12],
    "SPELL_INTERRUPT": [6],
    "SPELL_DISPEL": 7,
    "SPELL_ENERGIZE": [23],
    "SPELL_PERIODIC_ENERGIZE": [23],
    "SPELL_PERIODIC_MISSED": [6, 7],
    "SPELL_PERIODIC_LEECH": 23,
    "SPELL_EXTRA_ATTACKS": 4,
    "DAMAGE_SHIELD": 29,
    "SPELL_DRAIN": 23,
    "SPELL_PERIODIC_DRAIN": 23,
    "SPELL_RESURRECT": 3,
    "SPELL_INSTAKILL": 3,
    "SPELL_SUMMON": 3,
    #
    "DAMAGE_SHIELD_MISSED": [5, 6],
    "SWING_DAMAGE_LANDED": 26,
    "SPELL_CREATE": 3,
}

# https://wow.gamepedia.com/COMBAT_LOG_EVENT
prefixes = {
    "SWING": [],
    "RANGE": ["spellId", "spellName", "spellSchool"],
    "SPELL": ["spellId", "spellName", "spellSchool"],
    "SPELL_PERIODIC": ["spellId", "spellName", "spellSchool"],
    "SPELL_BUILDING": ["spellId", "spellName", "spellSchool"],
    "ENVIRONMENTAL": ["environmentalType"],
}

suffixes = {
    "_DAMAGE": [
        "amount",
        "overkill",
        "school",
        "resisted",
        "blocked",
        "absorbed",
        "critical",
        "glancing",
        "crushing",
        "isOffHand",
    ],
    "_MISSED": ["missType", "isOffHand", "amountMissed"],
    "_HEAL": ["amount", "overhealing", "absorbed", "critical"],
    "_ENERGIZE": ["amount", "overEnergize", "powerType", "alternatePowerType"],
    "_DRAIN": ["amount", "powerType", "extraAmount"],
    "_LEECH": ["amount", "powerType", "extraAmount"],
    "_INTERRUPT": ["extraSpellId", "extraSpellName", "extraSchool"],
    "_DISPEL": ["extraSpellId", "extraSpellName", "extraSchool", "auraType"],
    "_DISPEL_FAILED": ["extraSpellId", "extraSpellName", "extraSchool"],
    "_STOLEN": ["extraSpellId", "extraSpellName", "extraSchool", "auraType"],
    "_EXTRA_ATTACKS": ["amount"],
    "_AURA_APPLIED": ["auraType", "amount"],
    "_AURA_REMOVED": ["auraType", "amount"],
    "_AURA_APPLIED_DOSE": ["auraType", "amount"],
    "_AURA_REMOVED_DOSE": ["auraType", "amount"],
    "_AURA_REFRESH": ["auraType", "amount"],
    "_AURA_BROKEN": ["auraType"],
    "_AURA_BROKEN_SPELL": ["extraSpellId", "extraSpellName", "extraSchool", "auraType"],
    "_CAST_START": [],
    "_CAST_SUCCESS": [],
    "_CAST_FAILED": ["failedType"],
    "_INSTAKILL": [],
    "_DURABILITY_DAMAGE": [],
    "_DURABILITY_DAMAGE_ALL": [],
    "_CREATE": [],
    "_SUMMON": [],
    "_RESURRECT": [],
    # "_ABSORBED": ["amount"],
}

advanced_fields = [
    "unitGUID",
    "ownerGUID",
    "currHp",
    "maxHp",
    "attackPower",
    "spellPower",
    "armor",
    "resourceType",
    "currResource",
    "maxResource",
    "resourceCost",
    "coord",
    "coord",
    "UiMapID",
    "facing",
    "itemLevel/level",
]

specials = {
    "SPELL_ABSORBED": [
        [
            # magical damage absorb
            "damageSpellId",
            "damageSpellName",
            "damageSpellSchool",
            "originGuid",
            "originName",
            "originFlags",
            "originRaidFlags",
            "spellId",
            "spellName",
            "spellSchool",
            "amount",
            "amount2",
        ],
        [
            # physical damage absorb
            "originGuid",
            "originName",
            "originFlags",
            "originRaidFlags",
            "spellId",
            "spellName",
            "spellSchool",
            "amount",
            "amount2",
        ],
    ],
    #
    "DAMAGE_SHIELD": "SPELL_DAMAGE",
    "DAMAGE_SPLIT": "SPELL_DAMAGE",
    "DAMAGE_SHIELD_MISSED": "SPELL_MISSED",
    "SWING_DAMAGE_LANDED": "SWING_DAMAGE",
    "SPELL_CREATE": "SPELL_SUMMON",
    #
    "ENCHANT_APPLIED": ["spellName", "itemID", "itemName"],
    "ENCHANT_REMOVED": ["spellName", "itemID", "itemName"],
    #
    "PARTY_KILL": [],
    "UNIT_DIED": [[], ["recapID", "unconsciousOnDeath"]],
    "UNIT_DESTROYED": [[], ["recapID", "unconsciousOnDeath"]],
    "UNIT_DISSIPATES": ["recapID", "unconsciousOnDeath"],
}

# Type
COMBATLOG_OBJECT_TYPE_MASK = 0x0000FC00
COMBATLOG_OBJECT_TYPE_OBJECT = 0x00004000
COMBATLOG_OBJECT_TYPE_GUARDIAN = 0x00002000
COMBATLOG_OBJECT_TYPE_PET = 0x00001000
COMBATLOG_OBJECT_TYPE_NPC = 0x00000800
COMBATLOG_OBJECT_TYPE_PLAYER = 0x00000400
# Controller
COMBATLOG_OBJECT_CONTROL_MASK = 0x00000300
COMBATLOG_OBJECT_CONTROL_NPC = 0x00000200
COMBATLOG_OBJECT_CONTROL_PLAYER = 0x00000100
# Reaction
COMBATLOG_OBJECT_REACTION_MASK = 0x000000F0
COMBATLOG_OBJECT_REACTION_HOSTILE = 0x00000040
COMBATLOG_OBJECT_REACTION_NEUTRAL = 0x00000020
COMBATLOG_OBJECT_REACTION_FRIENDLY = 0x00000010
# Controller affiliation
COMBATLOG_OBJECT_AFFILIATION_MASK = 0x0000000F
COMBATLOG_OBJECT_AFFILIATION_OUTSIDER = 0x00000008
COMBATLOG_OBJECT_AFFILIATION_RAID = 0x00000004
COMBATLOG_OBJECT_AFFILIATION_PARTY = 0x00000002
COMBATLOG_OBJECT_AFFILIATION_MINE = 0x00000001
# Special cases (non-exclusive)
COMBATLOG_OBJECT_SPECIAL_MASK = 0xFFFF0000
COMBATLOG_OBJECT_NONE = 0x80000000
COMBATLOG_OBJECT_MAINASSIST = 0x00080000
COMBATLOG_OBJECT_MAINTANK = 0x00040000
COMBATLOG_OBJECT_FOCUS = 0x00020000
COMBATLOG_OBJECT_TARGET = 0x00010000



def find_event(event, field_count):

    if event in specials:
        if isinstance(specials[event], str):
            return find_event(specials[event], field_count)
        else:
            a = specials[event]
            if len(a) == 0 or isinstance(a[0], str):
                a = [a]

            for i in a:
                if len(i) == field_count:
                    return i, "="
            return None, None

    prefix = ""
    prefix_length = 0
    prefix_fields = None
    for k, v in prefixes.items():
        if event.startswith(k) and len(k) > prefix_length:
            prefix_length = len(k)
            prefix = k
            prefix_fields = v

    suffix = ""
    suffix_length = 0
    suffix_fields = None
    for k, v in suffixes.items():
        if event.endswith(k) and len(k) > suffix_length:
            suffix_length = len(k)
            suffix = k
            suffix_fields = v

    if event == prefix + suffix:
        fields = prefix_fields + suffix_fields
        nb = len(fields)
        fields_adv = prefix_fields + advanced_fields + suffix_fields
        nb_adv = len(fields_adv)

        if field_count == nb:
            return fields, "="

        if field_count == nb_adv:
            return fields_adv, "="

        if field_count - nb == 1:
            fields.append("unknown")
            return fields, ">"

        if field_count - nb == -1:
            return fields[:-1], "<"

        if field_count - nb_adv == 1:
            fields_adv.append("unknown")
            return fields_adv, ">"

        if field_count - nb_adv == -1:
            return fields_adv[:-1], "<"

        logging.critical(f"bad event {event}. fields: {field_count}, expected: {nb} or {nb_adv}")
    else:
        logging.critical(f"unknown event {event}")

    return None, None


signalled = set()

def check_event(event, row):
    global signalled

    fields, state = find_event(event, len(row[9:]))

    if fields is None:
        logging.error(event)
        # logging.error(source)
        # logging.error(dest)
        logging.error(" | ".join(row[9:]))
        exit(2)

    if state != "=":
        if event + state not in signalled:
            signalled.add(event + state)

            if state == ">":
                logging.info(f"{event} 1 extra field")
            else:
                logging.info(f"{event} 1 missing field")

            logging.debug("{} {} {} {} {}".format(event, row[2], row[6], ",".join(map(str, row[9:])), state))
            for field, value in zip(fields, row[9:]):
                logging.debug(f"{field:>25}: {str(value)}")

    return fields, state




class Entity:
    def __init__(self, id, name, flags, raid_flags):
        self.guid = id  # https://wow.gamepedia.com/GUID
        self.name = name
        self.flags = int(flags, 16)  # https://wow.gamepedia.com/UnitFlag
        self.raid_flags = int(raid_flags, 16)  # https://wow.gamepedia.com/RaidFlag

    def __str__(self):
        return "{:40} {:32} 0x{:x} 0x{:x}".format(self.guid, self.name, self.flags, self.raid_flags)


class LogInfo:
    def __init__(self):
        self.event_filter_include = set()
        self.event_filter_exclude = set()

    def Parse(self, filename):
        # parsing a new file, reset some of the instance variables
        self.encounters = []
        self.total_line_count = 0
        self.parsed_line_count = 0
        entities = {}

        version = ""

        reader = csv.reader(open(filename))
        for row in reader:
            # print(row)

            # bump line counter
            self.total_line_count += 1

            # two spaces are used to split the date/time field from the actual combat data
            timestamp, event = row[0].split("  ")

            if event == "COMBAT_LOG_VERSION":
                version = f"version={row[1]} adv={row[3]} game={row[5]}/{row[7]}"
                continue

            source = Entity(*row[1:5])
            dest = Entity(*row[5:9])

            def test(e):
                if e.guid not in entities:
                    entities[e.guid] = e
                else:
                    pass
                    # if e.name != entities[e.guid].name and entities[e.guid].name != 'Unknown':
                    #     if e.name not in signalled:
                    #         signalled.add(e.name)
                    #         print()
                    #         print(e)
                    #         print(entities[e.guid])

            test(source)
            test(dest)

            if event in events:
                e = events[event]

                if isinstance(e, int):
                    fields = [e]
                elif isinstance(e, list):
                    fields = e
                else:
                    logging.critical("bad events table")
                    exit(2)

                for i in fields:
                    if len(row) == 1 + 4 + 4 + i:
                        break
                else:
                    logging.error("event %s: bad number of fields: %d excepted: %r", event, len(row) - 9, fields)
                    print(",".join(map(str, row)))
                    exit(2)
            else:
                logging.critical("unknown event %s", event)
                print(",".join(map(str, row)))
                print(len(row) - 9)
                exit(2)

            ########################
            if self.event_filter_include:
                if event not in self.event_filter_include:
                    continue
            elif self.event_filter_exclude:
                if event in self.event_filter_exclude:
                    continue

            ########################
            fields, state = check_event(event, row)

            data = {}
            for i, field in enumerate(fields, 9):
                data[field] = row[i]

                # print(f"{field:>25}: {row[i]}")

            # if data["critical"] != "0":
            #     print("ok")
            #     exit(0)

        # for i in entities.values():
        #     print(i)

        return []
