#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if sys.argv[1]=='runserver':
        if os.fork():
            sys.exit(0)
        os.setpgrp()
        os.umask(0)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smserver.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
