version = 9

events = {
    "DAMAGE_SHIELD": 29,
    "DAMAGE_SHIELD_MISSED": [5, 6],
    "DAMAGE_SPLIT": 29,
    "ENVIRONMENTAL_DAMAGE": 27,
    "RANGE_DAMAGE": 29,
    "RANGE_MISSED": [5, 6, 7],
    "SPELL_ABSORBED": [9, 12],
    "SPELL_AURA_APPLIED": 4,
    "SPELL_AURA_APPLIED_DOSE": 5,
    "SPELL_AURA_BROKEN": 4,
    "SPELL_AURA_BROKEN_SPELL": 7,
    "SPELL_AURA_REFRESH": 4,
    "SPELL_AURA_REMOVED": 4,
    "SPELL_AURA_REMOVED_DOSE": 5,
    "SPELL_CAST_FAILED": 4,
    "SPELL_CAST_START": 3,
    "SPELL_CAST_SUCCESS": 19,
    "SPELL_CREATE": 3,
    "SPELL_DAMAGE": 29,
    "SPELL_DISPEL": 7,
    "SPELL_DRAIN": 23,
    "SPELL_ENERGIZE": 23,
    "SPELL_EXTRA_ATTACKS": 4,
    "SPELL_HEAL": 24,
    "SPELL_INSTAKILL": 3,
    "SPELL_INTERRUPT": 6,
    "SPELL_MISSED": [5, 6, 7],
    "SPELL_PERIODIC_DAMAGE": 29,
    "SPELL_PERIODIC_DRAIN": 23,
    "SPELL_PERIODIC_ENERGIZE": 23,
    "SPELL_PERIODIC_HEAL": 24,
    "SPELL_PERIODIC_LEECH": 23,
    "SPELL_PERIODIC_MISSED": [5, 7],
    "SPELL_RESURRECT": 3,
    "SPELL_SUMMON": 3,
    "SWING_DAMAGE": 26,
    "SWING_DAMAGE_LANDED": 26,
    "SWING_MISSED": [2, 3, 4],
    "PARTY_KILL": 0,
    "UNIT_DESTROYED": 0,
    "UNIT_DIED": 0,
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
