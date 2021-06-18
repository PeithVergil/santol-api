#!/usr/bin/env python
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from sqlalchemy import create_engine
from santol.alchemy import BaseModel
from santol.settings import DATABASES
from santol.authen.chems import *
from santol.profile.chems import *


def main():
    BaseModel.metadata.create_all(create_engine(DATABASES['default']))
    BaseModel.metadata.create_all(create_engine(DATABASES['testing']))


if __name__ == '__main__':
    main()
