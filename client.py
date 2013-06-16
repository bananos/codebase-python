import requests


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
        build = lambda item: (item[key][_id], item[key])
        return dict(map(build, items))

    def _request_by_id(self, endpoint, key, _id='id', project=None, params={}):
        response = self._plain_request(endpoint, project, params)
        return self._group_by_id(response, key, _id)

    def global_activity(self, page=1):
        return self._request_by_id(
            endpoint="activity.json",
            key="event",
            params={"page": page}
        )

    def activity(self, project, page=1):
        return self._request_by_id(
            endpoint='activity.json',
            project=project,
            key="event",
            params={"page": page}
        )

    def all_projects(self):
        return self._request_by_id(
            endpoint='projects.json',
            key='project',
            _id='permalink'
        )

    def project(self, project):
        return self._plain_request(endpoint='%s.json' % project)['project']

    def project_groups(self):
        return self._request_by_id(
            endpoint='project_groups.json',
            key='project_group'
        )

    def assignments(self, project):
        return self._request_by_id(
            endpoint='assignments.json',
            project=project,
            key='user',
            _id='username'
        )

    def repositories(self, project):
        return self._request_by_id(
            endpoint='repositories.json',
            project=project,
            key='repository',
            _id='permalink'
        )

    def repository(self, project, repository):
        return self._plain_request(
            endpoint='%s.json' % repository,
            project=project
        )['repository']

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
