#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_pivot.tests.test_project.settings'

def test():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["django_pivot.tests"])
    sys.exit(bool(failures))


def main():
    from django.core.management import execute_from_command_line
    if len(sys.argv) == 1:
        test()
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
