#!/bin/bash

# First groks packs so we are sure we are update
/opt/shinken.io/bin/grokpacks.py

# Then compute some stats
/opt/shinken.io/bin/compute-github-stats.py
/opt/shinken.io/bin/compute-packages-stats.py
/opt/shinken.io/bin/compute-wiki-stats.py
/opt/shinken.io/bin/compute-achievements.py
