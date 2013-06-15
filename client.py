import requests


API_USERNAME = ''
API_KEY = ''


class CodebaseClient(object):

    BASE_URL = 'https://api3.codebasehq.com'

    def __init__(self, username, key):
        self.username = username
        self.key = key
        self.auth = (username, key)

    def _plain_request(self, endpoint, project=None, params={}):
        if project:
            url = '%s/%s/%s' % (self.BASE_URL, project, endpoint)
        else:
            url = '%s/%s' % (self.BASE_URL, endpoint)
        return requests.get(
            url,
            params=params,
            auth=self.auth
        ).json()

    def _group_by_id(self, items, key, _id="id"):
        return dict([(x[key][_id], x[key]) for x in items])

    def _request_by_id(self, endpoint, project, key, _id='id', params={}):
        response = self._plain_request(endpoint, project, params)
        return self._group_by_id(response, key, _id)

    def global_activity(self):
        return self._plain_request(endpoint='activity.json')

    def activity(self, project):
        return self._plain_request(endpoint='activity.json', project=project)

    def statuses(self, project):
        return self._request_by_id(
            endpoint='tickets/statuses.json',
            project=project,
            key='ticketing_status')

    def priorities(self, project):
        return self._request_by_id(
            endpoint='tickets/priorities.json',
            project=project,
            key='ticketing_priority')

    def categories(self, project):
        return self._request_by_id(
            endpoint='tickets/categories.json',
            project=project,
            key='ticketing_category')

    def milestones(self, project):
        return self._request_by_id(
            endpoint='milestones.json',
            project=project,
            key='ticketing_milestone')

    def tickets(self, project, params={}):
        """
        Paginated to 20 items
        """
        return self._request_by_id(
            endpoint='tickets.json',
            project=project,
            params=params,
            key='ticket',
            _id='ticket_id'
        )

    def all_tickets(self, project, params={}):
        result = self.tickets(project, params)
        if result:
            _params = params.copy()
            page = _params.get("page", 0)
            _params["page"] = page + 1
            result.update(self.all_tickets(project, _params))
        return result

    def tickets_by_milestones(self, project, milestone):
        return self.tickets(
            project=project,
            params={"query": 'milestone:"%s"' % milestone}
        )

    def group_tickets_by_status(self, tickets, project, statuses=None):
        if statuses is None:
            statuses = self.statuses(project)

        grouped_tickets = dict([(statuses[s]['id'], []) for s in statuses.keys()])

        for ticket in tickets.values():
            status_id = ticket['status_id']
            if not status_id in grouped_tickets:
                grouped_tickets[status_id] = []
            grouped_tickets[status_id].append(ticket)

        return grouped_tickets


def main():
    client = CodebaseClient(API_USERNAME, API_KEY)
    return


if __name__ == '__main__':
    main()
