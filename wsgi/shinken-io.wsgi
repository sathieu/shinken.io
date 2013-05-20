import sys
import os
import ConfigParser

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__)+"/..")
sys.path.append(os.path.dirname(__file__)+"/..")

from shinkenio.shinkenio import ShinkenIO
from webgears import bottle

cfg_file = os.path.join(os.path.dirname(__file__), '../config.ini')

app = ShinkenIO(cfg_file)
app.load_pages()

# Now go for it!
application = bottle.default_app()
