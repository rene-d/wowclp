version = 12

events = {
    "SPELL_ABSORBED": [9, 12],
    "SPELL_AURA_APPLIED": [4, 5],
    "SPELL_AURA_APPLIED_DOSE": 5,
    "SPELL_AURA_REFRESH": [4, 5],
    "SPELL_AURA_REMOVED": [4, 5],
    "SPELL_AURA_REMOVED_DOSE": 5,
    "SPELL_CAST_FAILED": 4,
    "SPELL_CAST_START": 3,
    "SPELL_CAST_SUCCESS": 20,
    "SPELL_DAMAGE": 30,
    "SPELL_ENERGIZE": 24,
    "SPELL_EXTRA_ATTACKS": 4,
    "SPELL_HEAL": 25,
    "SPELL_MISSED": [5, 7],
    "SPELL_PERIODIC_MISSED": 7,
    "SPELL_SUMMON": 3,
    "SWING_DAMAGE": 27,
    "SWING_DAMAGE_LANDED": 27,
    "SWING_MISSED": [2, 4],
    "PARTY_KILL": 1,
    "UNIT_DIED": 1,
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
    "unknown", # ?
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
    "PARTY_KILL": ["?"],
    "UNIT_DIED": [[], ["?"], ["recapID", "unconsciousOnDeath"]],
    "UNIT_DESTROYED": [[], ["recapID", "unconsciousOnDeath"]],
    "UNIT_DISSIPATES": ["recapID", "unconsciousOnDeath"],
}
