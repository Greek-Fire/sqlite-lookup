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

EXAMPLES = '''
- name: "check local database"
  ansible.builtin.debug:
    msg: "{{ lookup('theredgreek.sqlite.sqlite', 'path=foo/bar', 'select=select * from tablesA') }}"
- name: "use vars as values"
  ansible.builtin.debug: 
    msg: "{{ lookup('theredgreek.sqlite.sqlite',path=path, select=select)}}"
  vars:
    path: 'foo/var'
    select: 'select * FROM tableA'
'''

RETURN = '''
    _raw:
        description:
            - list of key value pair.
            - column headers are the keys.
        type: list
        elements: string
'''
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

import os
try:
    import sqlite3
except ImportError:
    pass

# function to check if file exist
def file_check(path):
    assert(os.path.isfile(path)), "{} is not in the current path".format(path)

# function to check if file is sqlite db file
def sqlite_check(path):
    sqlite_header = b'SQLite format 3\x00'
    test_file = open(path, "rb")
    file_header = test_file.read(16)
    assert (file_header == sqlite_header), "{} is not a sqlite db file".format(path)


class LookupModule(LookupBase):
    def run(self,terms,**kwargs):
        # get options
        self.set_options(direct=kwargs)

        # check for proper sqlite db file
        path = self.get_option('path')
        file_check(path)
        sqlite_check(path)

        # setup connection
        curse = sqlite3.connect(path).cursor()

        # setup select statement
        select = self.get_option('select')
        values = curse.execute(select)

        # setup keys from column headers
        keys = [description[0] for description in values.description]

        # create a list of json objects from the results of the select statement
        rel = []
        for v in values:
          json_object = dict(zip(keys,v))
          rel.append(json_object)
        return rel
