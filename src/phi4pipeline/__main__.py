# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

"""Run the PHI-base cleaning pipeline as a shell script."""

import sys

from phi4pipeline import cli


def main(args):
    cli.run(args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
