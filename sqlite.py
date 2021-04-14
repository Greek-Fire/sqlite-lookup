#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
        lookup: sqlite
        author: Louis Tiches <ltiches@redhat.com>
        version_added: "0.1"  # for collections, use the collection version, not the Ansible version
        short_description: read file contents
        description:
          - This lookup returns the contents from a query to a sqlite database
        options:
          path:
            description: path of sqlite database
            default: 'change me' 
          select:
            description: select statement to use.
            default: 'SELECT * FROM table' 
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

try:
    import sqlite3
except ImportError:
    pass

class LookupModule(LookupBase):
    def run(self, terms, **kwargs):
       # get options
        self.set_options(direct=kwargs)

        # setup connection
        path = self.get_option('path')
        curse = sqlite3.connect(path).cursor()

        # setup select statement
        select = self.get_option('select')
        values = curse.execute(select)

        # setup keys from column headers
        keys = [description[0] for description in description.title]

        # create a list of json objects from the results of the select statement
        rel = []
        for v in values:
          json_object = dict(zip(keys,v))
          rel.append(json_object)
        return rel
