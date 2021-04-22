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
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

import os
try:
    import sqlite3
except AnsibleParserError():
    raise AnsibleError("Please install sqlite3")
        
class LookupModule(LookupBase):
    def run(self,terms, **kwargs, variables=None):
        ret = []

        self.set_options(var_options=variables, direct=kwargs)

        # populate options
        paramvals = self.get_options()

        for term in terms:
            print(term)
            kv = parse_kv(term)
            print(kv)

            if '_raw_params' not in kv:
                raise AnsibleError('Search key is required but was not found')

            key = kv['_raw_params']

            # parameters override per term using k/v
            try:
                for name, value in kv.items():
                    if name == '_raw_params':
                        continue
                    if name not in paramvals:
                        raise AnsibleAssertionError('%s is not a valid option' % name)

                    self._deprecate_inline_kv()
                    paramvals[name] = value

            except (ValueError, AssertionError) as e:
                raise AnsibleError(e)
                
        self.set_options(direct=kwargs, var_options=variables)
        

        # set variables
        path = self.get_option('path')
        select = self.get_option('select')
        
        # Find file in search path
        lookup = self.find_file_in_search_path(variables, 'files', path)
        display.vvv(u"File lookup using %s as file" % lookup)
        try:
                if lookup:
                        print('bob')
                        
                else:
                        raise AnsibleParserError()

        except AnsibleParserError():                 
                raise AnsibleError("Could not locate file in path: %s" % path)

                 
        


        # setup connection
        curse = sqlite3.connect(path).cursor()

        # grab data
        values = curse.execute(select)

        # setup keys from column headers
        keys = [description[0] for description in values.description]

        # create a list of json objects from the results of the select statement
        rel = []
        for v in values:
          json_object = dict(zip(keys,v))
          rel.append(json_object)
        return rel,kv,term


