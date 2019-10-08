from redminelib import Redmine


def issueUpdater(id, key, notes):
    redmine = Redmine('http://redmine.chuangle.com', key=key)

    author = redmine.issue.get(id).author
    projectID = redmine.issue.get(id).project.id
    nextVersion = redmine.project.get(projectID).versions.filter(name="Next version")
    nextVersionID = nextVersion[0].id if nextVersion else None
    
    redmine.issue.update(
        id,
        status_id=4,
        assigned_to_id=author.id,
        fixed_version_id=nextVersionID,
        notes=notes
    )


if __name__ == "__main__":
    issueUpdater(
        328,
        key="2054640b19d6a26f3d87047e342ea5e946908ad9",
        notes="this is update via bot"
    )
