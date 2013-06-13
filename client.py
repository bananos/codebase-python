import requests


API_USERNAME = ''
API_KEY = ''


class CodebaseClient(object):

    BASE_URL = 'https://api3.codebasehq.com'

    def __init__(self, username, key, project):
        self.username = username
        self.key = key
        self.auth = (username, key)
        self.project = project

    def activity(self):
        return requests.get(
            '%s/%s/activity.json' % (self.BASE_URL, self.project),
            auth=self.auth).json()

    def _request_by_id(self, url, key, _id='id', params={}):
        response = requests.get(
            '%s/%s/%s' % (self.BASE_URL, self.project, url),
            params=params,
            auth=self.auth).json()
        return dict([(x[key][_id], x[key]) for x in response])

    def statuses(self):
        return self._request_by_id('tickets/statuses.json', 'ticketing_status')

    def priorities(self):
        return self._request_by_id('tickets/priorities.json', 'ticketing_priority')

    def categories(self):
        return self._request_by_id('tickets/categories.json', 'ticketing_category')

    def milestones(self):
        return self._request_by_id('milestones.json', 'ticketing_milestone')

    def tickets(self):
        return self._request_by_id('tickets.json', 'ticket', 'ticket_id')

    def group_tickets_by_status(self, tickets, statuses=None):
        if statuses is None:
            statuses = self.statuses()

        grouped_tickets = dict([(s['ticketing_status']['id'], []) for s in statuses.keys()])

        for ticket in tickets:
            status_id = ticket['ticket']['status_id']
            if not status_id in grouped_tickets:
                grouped_tickets[status_id] = []
            grouped_tickets[status_id].append(ticket)

        return grouped_tickets


def main():
    client = CodebaseClient(API_USERNAME, API_KEY, 'projectname')
    return


if __name__ == '__main__':
    main()
