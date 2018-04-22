#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if sys.argv[1] not in ['own', 'test', 'prd']:
        print('请输入正确的环境参数')
        sys.exit(1)
    env = sys.argv.pop(1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings_%s" % env)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
