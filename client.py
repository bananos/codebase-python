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

    def _plain_request(self, endpoint, params={}):
        return requests.get(
            '%s/%s/%s' % (self.BASE_URL, self.project, endpoint),
            params=params,
            auth=self.auth
        ).json()

    def _group_by_id(self, items, key, _id="id"):
        return dict([(x[key][_id], x[key]) for x in items])

    def _request_by_id(self, url, key, _id='id', params={}):
        response = self._plain_request(url, params)
        return self._group_by_id(response, key, _id)

    def activity(self):
        return self._plain_request('activity.json')

    def statuses(self):
        return self._request_by_id('tickets/statuses.json', 'ticketing_status')

    def priorities(self):
        return self._request_by_id('tickets/priorities.json', 'ticketing_priority')

    def categories(self):
        return self._request_by_id('tickets/categories.json', 'ticketing_category')

    def milestones(self):
        return self._request_by_id('milestones.json', 'ticketing_milestone')

    def tickets(self, params={}):
        response = self._plain_request('tickets.json', params)
        result = self._group_by_id(response, 'ticket', 'ticket_id')
        if result:
            _params = params.copy()
            page = _params.get("page", 0)
            _params["page"] = page + 1
            result.update(self.tickets(_params))
        return result

    def tickets_by_milestones(self, milestone):
        return self.tickets({"query": 'milestone:"%s"' % milestone})

    def group_tickets_by_status(self, tickets, statuses=None):
        if statuses is None:
            statuses = self.statuses()

        grouped_tickets = dict([(statuses[s]['id'], []) for s in statuses.keys()])

        for ticket in tickets.values():
            status_id = ticket['status_id']
            if not status_id in grouped_tickets:
                grouped_tickets[status_id] = []
            grouped_tickets[status_id].append(ticket)

        return grouped_tickets


def main():
    client = CodebaseClient(API_USERNAME, API_KEY, 'projectname')
    return


if __name__ == '__main__':
    main()
