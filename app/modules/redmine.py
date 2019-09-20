from redminelib import Redmine


def issueUpdater(id, key, notes):
    redmine = Redmine('http://redmine.chuangle.com', key=key)

    author = redmine.issue.get(id).author

    redmine.issue.update(
        id,
        status_id=4,
        assigned_to_id=author.id,
        notes=notes
    )
    # import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    issueUpdater(
        139,
        key="2054640b19d6a26f3d87047e342ea5e946908ad9",
        notes="this is update via bot"
    )
