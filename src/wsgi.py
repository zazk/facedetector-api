import os
import sys

from os.path import dirname, realpath
from site import addsitedir

BASE_DIR = dirname(realpath(__file__))

WORKON_HOME = os.environ['WORKON_HOME']
VENV = 'cv'

addsitedir('{0}/{1}/lib/python2.7/site-packages'.format(WORKON_HOME, VENV))

sys.path = [BASE_DIR] + sys.path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')

# activamos el entorno virtual
activate_this = os.path.expanduser(
    '{0}/{1}/bin/activate_this.py'.format(WORKON_HOME, VENV))
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()