import sys
import csv
import logging
import collections
import itertools
import combatlog9
import combatlog12


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



class Entity:
    """
    game entity (player, creature, pet, ...)
    """

    def __init__(self, id, name, flags, raid_flags):
        self.guid = id  # https://wow.gamepedia.com/GUID
        self.name = name
        self.flags = int(flags, 16)  # https://wow.gamepedia.com/UnitFlag
        self.raid_flags = int(raid_flags, 16)  # https://wow.gamepedia.com/RaidFlag

    def __str__(self):
        return "{:40} {:32} 0x{:x} 0x{:x}".format(
            self.guid, self.name, self.flags, self.raid_flags
        )


class LogParser:
    """
    class to parse WoWCombatLog.txt file
    """

    def __init__(self):
        self.event_filter_include = set()
        self.event_filter_exclude = set()
        self.flag_print = False
        self.combatlog = None
        self.signalled = set()
        self.with_adv = set()
        self.without_adv = set()
        self.flag_count = False
        self.fields_count = dict()

    def set_print(self, flag):
        self.flag_print = flag

    def set_count(self, flag):
        self.flag_count = flag

    def parse(self, filename):
        """ parse a combatlog file """
        self.encounters = []
        self.total_line_count = 0
        self.parsed_line_count = 0

        self.version = ""
        self.entities = {}

        try:
            reader = csv.reader(open(filename))
            for row in reader:
                # print(row)

                # bump line counter
                self.total_line_count += 1

                self.parse_row(row)

        except csv.Error as e:
            logging.error(f"CSV ERROR {e}")

        if self.flag_count:
            for k, v in sorted(self.fields_count.items()):
                print(f"{k:32} {' '.join(map(str, v))}")

            def rev_key(a):
                return a
                # return "".join(reversed(a))

            t = dict()
            for k in sorted(self.fields_count.keys(), key=rev_key):
                s = self.fields_count[k]
                if len(s) == 1:
                    t[k] = s.pop()
                else:
                    t[k] = list(s)
            print(t)

            return

        # print(self.without_adv)
        # print(self.with_adv)
        # print(self.without_adv.intersection(self.with_adv))


    def parse_row(self, row):

        # two spaces are used to split the date/time field from the actual combat data
        timestamp, event = row[0].split("  ")


        if event == "COMBAT_LOG_VERSION":
            self.version = f"version={row[1]} adv={row[3]} game={{build: {row[5]}/project: {row[7]}}}"
            logging.info("{} {} {}".format(timestamp, event, self.version))
            if row[1] == "9":
                self.combatlog = combatlog9
            elif row[1] == "12":
                self.combatlog = combatlog12
            else:
                logging.error(f"unknown version: {row[1]}")
                self.combatlog = None
            return

        if event == "ENCOUNTER_START":
            logging.info("{} {} {}".format(timestamp, event, ",".join(row[1:])))
            return

        if event == "ENCOUNTER_END":
            logging.info("{} {} {}".format(timestamp, event, ",".join(row[1:])))
            return

        if event == "COMBATANT_INFO":
            return

        if event == "ZONE_CHANGE":
            logging.info("{} {} {}".format(timestamp, event, ",".join(row[1:])))
            return

        if self.flag_count:
            n = len(row) - 9
            c = self.fields_count.get(event, set())
            if n not in c:
                c.add(n)
                self.fields_count[event] = c
            return

        cl = self.combatlog
        if cl is None:
            return

        ########################
        if self.event_filter_include:
            if event not in self.event_filter_include:
                return
        elif self.event_filter_exclude:
            if event in self.event_filter_exclude:
                return

        try:
            source = Entity(*row[1:5])
            dest = Entity(*row[5:9])
            # if source.guid not in entities:
            #     entities[source.guid] = source
            # if dest.guid not in entities:
            #     entities[dest.guid] = source
        except TypeError:
            logging.error(f"{row}")
            exit()

        ########################
        if event in cl.events:
            e = cl.events[event]

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
                logging.error(
                    "event %s: bad number of fields: %d excepted: %r",
                    event,
                    len(row) - 9,
                    fields,
                )
                print(",".join(map(str, row)))
                exit(2)
        else:
            logging.critical("unknown event %s", event)
            logging.critical("%s %d", ",".join(map(str, row)), len(row) - 9)
            exit(2)

        ########################

        fields, state = self.check_event(event, row)

        if self.flag_print:
            print(",".join(row))
            print(f"\033[34m{'event':>25}: {event}\033[0m")
            print(f"\033[34m{'timestamp':>25}: {timestamp}\033[0m")
            print(f"\033[32m{'source':>25}: {source}\033[0m")
            print(f"\033[95m{'dest':>25}: {dest}\033[0m")

            for i, field in enumerate(fields, 9):
                print(f"\033[33m{field:>25}: {row[i]}\033[0m")

        # data = {}
        # for i, field in enumerate(fields, 9):
        #     data[field] = row[i]



    def find_event(self, event, value_count):
        """
        find the event fields
        """

        prefixes = self.combatlog.prefixes
        suffixes = self.combatlog.suffixes
        specials = self.combatlog.specials
        advanced_fields = self.combatlog.advanced_fields

        if event in specials:
            if isinstance(specials[event], str):
                return self.find_event(specials[event], value_count)
            else:
                a = specials[event]
                if len(a) == 0 or isinstance(a[0], str):
                    a = [a]

                for i in a:
                    if len(i) == value_count:
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

            if value_count == nb:
                self.without_adv.add(event)
                return fields, "="

            if value_count == nb_adv:
                self.with_adv.add(event)
                return fields_adv, "="

            if value_count - nb == 1:
                self.without_adv.add(event)
                fields.append("unknown")
                return fields, ">"

            if value_count - nb == -1:
                self.without_adv.add(event)
                return fields[:-1], "<"

            if value_count - nb_adv == 1:
                self.with_adv.add(event)
                fields_adv.append("unknown")
                return fields_adv, ">"

            if value_count - nb_adv == -1:
                self.with_adv.add(event)
                return fields_adv[:-1], "<"

            logging.critical(
                f"bad event {event}. fields: {value_count}, expected: {nb} or {nb_adv}"
            )
        else:
            logging.critical(f"unknown event {event}")

        return None, None


    def check_event(self, event, row):
        """
        decode and check an event
        """

        fields, state = self.find_event(event, len(row[9:]))

        if fields is None:
            logging.error(event)
            # logging.error(source)
            # logging.error(dest)
            logging.error(" | ".join(row[9:]))
            exit(2)

        if state != "=":
            if event + state not in self.signalled:
                self.signalled.add(event + state)

                if state == ">":
                    # logging.info(f"{event} 1 extra field")
                    pass
                else:
                    # logging.info(f"{event} 1 missing field")
                    pass

                logging.debug(
                    "{},{},{},{},{}".format(
                        event, row[2], row[6], ",".join(map(str, row[9:])), state
                    )
                )
                for field, value in zip(fields, row[9:]):
                    logging.debug(f"{field:>25}: {str(value)}")

        return fields, state