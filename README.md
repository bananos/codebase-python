Codebase Python API
=======================

This project is just a wrapper for [CodebaseHQ API](http://support.codebasehq.com/kb).
Some notes:

* The project is just an alpha version.
* Doesn't cover all the endpoints yet, and it's read only for now.

# Instalation

You can install this library through PyPI using `pip` or `easy_install`::

    pip install codebase-api

or directly from the current master branch from GitHub::

    pip install https://github.com/pyriku/codebase-python/zipball/master

# Documentation

The library is really easy to use::

```python

    from codebase import CodebaseClient
    client = CodebaseClient(API_USERNAME, API_KEY)  # from your Codebase account page

    projects = client.all_projects()
    milestones = client.milestones('my-project')
    users = client.users()
    tickets = client.tickets('my-project', {'query': 'milestone:"Sprint 1"')
    notes = client.notes('my-project', 204)

```

Supported operations:

* Global and per-project activity
* Projects, project groups and project users
* Repositories
* Tickets
* Statuses, milestones, categories and priorities

Only read-only support right now.

More documentation to be added soon.

# License

Copyright (c) 2013, Pablo Recio
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
