from changelog.daos import ChangelogDAO


def parse_build_params(path):
    dao = ChangelogDAO.parse_yaml(path)
    dao.send_entries()
