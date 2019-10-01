class RedmineWebhookParser():
    def __init__(self, data):
        self.data = data

    @property
    def payload(self):
        if ('payload' in self.data):
            return self.data['payload']

    @property
    def action(self):
        if ('action' in self.payload):
            return self.payload['action']

    @property
    def issue(self):
        if ('issue' in self.payload):
            return self.payload['issue']

    @property
    def assignee(self):
        if ('assignee' in self.issue):
            return self.issue['assignee']

    @property
    def assignee_name(self):
        if ('login' in self.assignee):
            return self.assignee['login']

    @property
    def issue_id(self):
        if ('id' in self.issue):
            return self.issue['id']

    @property
    def subject(self):
        if ('subject' in self.issue):
            return self.issue['subject']

    @property
    def status(self):
        if ('status' in self.issue):
            return self.issue['status']

    @property
    def status_name(self):
        if ('name' in self.status):
            return self.status['name']
