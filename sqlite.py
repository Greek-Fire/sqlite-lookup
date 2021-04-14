#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
        lookup: file
        author: Daniel Hokka Zakrisson <daniel@hozac.com>
        version_added: "0.9"  # for collections, use the collection version, not the Ansible version
        short_description: read file contents
        description:
            - This lookup returns the contents from a file on the Ansible controller's file system.
        options:
          _terms:
            description: path(s) of files to read
            required: True
        notes:
          - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
          - this lookup does not understand globing --- use the fileglob lookup instead.
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
    def run(self, ents, **kwargs):
        data = []
        db,sel = (ents[0], ents[1])
        curse = sqlite3.connect(db).cursor()
        values = curse.execute(sel)
        keys = [description[0] for description in values.description]
        for x in values:
          entry = dict(zip(keys,x))
          data.append(entry)
        return data
