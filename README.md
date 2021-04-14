# sqlite-lookup
Allows users to query sqlite database.
```
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
```


### EXAMPLES
```
- name: "check local database"
  ansible.builtin.debug:
    msg: "{{ lookup('sqlite', 'path=foo/bar', 'select=select * from tablesA') }}"
- name: "use vars as values"
  ansible.builtin.debug: 
    msg: "{{ lookup('sqlite',path=path, select=select)}}"
  vars:
    path: 'foo/var'
    select: 'select * FROM tableA'
```
