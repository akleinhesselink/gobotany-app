#!/usr/bin/env python
"""Run the right commands to build the Go Botany database from scratch."""

import ConfigParser
import sys
import subprocess

# Actions that the user can perform; default is to do them all.

def schema():
    admin('syncdb --noinput')
    admin('migrate')

def csv():
    run('python -m gobotany.core.importer zipimport')

def images():
    run('python -m gobotany.core.importer taxon-images')

    # Now that the taxon images are loaded, we can rebuild various
    # "sample" image collections that are subsets of the full image
    # collection.

    run('python -m gobotany.core.rebuild sample_pile_group_images')
    run('python -m gobotany.core.rebuild sample_pile_images')

    # Finally come some slow image-import routines, that actually ask S3
    # to list the contents of several folders (a slow operation to begin
    # with), and that then use the Django ORM to actually create
    # database rows.

    run('python -m gobotany.core.importer character-images')
    run('python -m gobotany.core.importer character-value-images')
    run('python -m gobotany.core.importer glossary-images')
    run('python -m gobotany.core.importer home-page-images')

def dkey():
    run('bin/s3-init.sh')
    run('s3cmd get --skip-existing --no-progress '
        's3://newfs/data-dkey/110330_fone_test_05.xml')
    run('python -m gobotany.dkey.xml_import')
    run('python -m gobotany.dkey.sync')

def solr():
    admin('rebuild_index --noinput')

def test():
    config = ConfigParser.RawConfigParser()
    config.read('tox.ini')
    cmdline = config.get('testenv', 'commands')
    run(cmdline)

ACTIONS = schema, csv, images, dkey, solr, test

# Helpers.

def admin(cmd):
    run('django-admin.py {} --settings gobotany.settings'.format(cmd))

def run(cmdline):
    print
    print 'Command line:', cmdline
    print
    arguments = cmdline.split()
    try:
        subprocess.check_call(arguments)
    except OSError as e:
        print >>sys.stderr, (
            'Fatal error running command\n    Command: {}\n    Error: {}'
            .format(cmdline, e))
        sys.exit(1)

# Main.

def main():
    args = sys.argv[1:]

    if not args:
        actions = ACTIONS
    else:
        actions = [action for action in ACTIONS if action.__name__ in args]

    if len(args) and len(args) != len(actions):
        print >>sys.stderr, (
            'Error: command-line arguments must be actions from the'
            ' following list\n\n    {}\n'
            .format(' '.join(action.__name__ for action in ACTIONS))
            )
        sys.exit(2)
    print
    print 'Actions: {}'.format(' '.join(action.__name__ for action in actions))
    print
    for action in actions:
        print '==== Running {} ===='.format(action.__name__)
        print
        action()
        print
    print 'Done'
    print

if __name__ == '__main__':
    main()