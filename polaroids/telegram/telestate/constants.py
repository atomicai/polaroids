#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging

__author__ = "luckydonald"

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logging.add_colored_handler(level=logging.DEBUG)
# end if


class IKEEP_PREVIOUS:
    pass


# end class


KEEP_PREVIOUS: IKEEP_PREVIOUS = IKEEP_PREVIOUS()  # now it's a singleton yo.
