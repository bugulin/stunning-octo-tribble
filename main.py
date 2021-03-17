#!/usr/bin/env python3

import os
import sys


# Změna pracovního adresáře

path = os.path.abspath(__file__)
os.chdir(os.path.dirname(path))


# Spuštění aplikace

from application import OctoTribble

app = OctoTribble()
app.run(sys.argv)
