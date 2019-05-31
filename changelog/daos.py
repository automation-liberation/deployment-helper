from dataclasses import dataclass
from typing import List

import yaml

from changelog.constants import ChangelogEntryEnum
from changelog.exceptions import ParseException
from changelog.utils import send_changelog_entry


class ChangelogEntryDAO:
    entry_type: ChangelogEntryEnum
    message: str

    def __init__(self, entry_type, message):
        self.entry_type = entry_type
        self.message = message


@dataclass
class ChangelogDAO:
    service: str
    version: str
    entries: List[ChangelogEntryDAO]

    @classmethod
    def parse_yaml(cls, file_path):
        with open(file_path) as file:
            changelog_dict = yaml.safe_load(file)
            image = changelog_dict.get('image')

            changelog = changelog_dict.get('changelog')
            changelog_entries = []

            if changelog:
                for enum in ChangelogEntryEnum:
                    entries = changelog.get(enum.value)
                    if entries:
                        for entry in entries:
                            changelog_entries.append(ChangelogEntryDAO(enum, entry))

            if image:
                dao = cls(image.get('package'), image.get('tag'), changelog_entries)
                return dao
            else:
                raise ParseException

    def send_entries(self):
        for entry in self.get_entry_dicts():
            send_changelog_entry(entry)

    def get_entry_dicts(self):
        return [self.get_entry_dict(entry) for entry in self.entries]

    def get_entry_dict(self, entry: ChangelogEntryDAO):
        return {"service": self.service, "version": self.version, "header": entry.entry_type.value, "body":entry.message}
