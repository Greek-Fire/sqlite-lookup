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

import os
try:
    import sqlite3
except AnsibleParserError():
    raise AnsibleError("Please install sqlite3")
        
class LookupModule(LookupBase):
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

import os
try:
    import sqlite3
except ImportError:
    pass

    def sqlite_check(self, path, select):
        file_check = os.path.isfile(path)
        qlist = select.split()
        select_test = qlist[0].upper()

        if select_test != 'SELECT':
            raise Exception("Sorry, SELECT statements only")
        
        if file_check != True:
            raise Exception("{} is not in the current path".format(path))
        
        file_header = open(path,'rb').read(16)

        if file_header != b'SQLite format 3\x00':
            raise Exception("{} is not a sqlite db file".format(path))

    def run(self,terms,**kwargs):
        # get options
        self.set_options(direct=kwargs)

        # set variables
        path = self.get_option('path')
        
        # setup select statement
        select = self.get_option('select')
        
        # check for user error
        self.sqlite_check(path, select)

        # create a list of json objects from the results of the select statement
        curse = sqlite3.connect(path).cursor()
        values = curse.execute(select)
        data = values.fetchone()
        rel = []
        if data > 0;
            keys = [description[0] for description in values.description]
            for v in values:
                json_object = dict(zip(keys,v))
                rel.append(json_object)
            return rel
        else:
            return rel
