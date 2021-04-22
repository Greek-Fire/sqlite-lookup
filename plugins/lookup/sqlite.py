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
            required: True
          select:
            description: select statement to use.
            default: 'SELECT * FROM table'
            required: True
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
from ansible.errors import AnsibleError, AnsibleParserError, AnsibleFileNotFound
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

import os
try:
    import sqlite3
except ImportError as e:
    raise AnsibleError("Please install sqlite3")
        
# function to check if file is sqlite db file and that string is select statement
def sqlite_check(path, select):
    qlist = select.split()
    select_test = qlist[0].upper()

    
    if select_test != 'SELECT':
        raise AnsibleError("Sorry, SELECT statements only")

    if not os.path.exists(path):
        raise AnsibleError("{} is not in the current path").format(path))
    test_file = open(path, "rb")
    file_header = test_file.read(16)

    if file_header != b'SQLite format 3\x00':
        raise AnsibleError("{} is not a sqlite db file".format(path))

class LookupModule(LookupBase):
    def run(self,terms,**kwargs):
        # get options
        self.set_options(direct=kwargs)

        # set variables
        path = self.get_option('path')
        select = self.get_option('select')

        # check for user error
        sqlite_check(path, select)

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


