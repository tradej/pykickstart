#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import unittest
from tests.baseclass import *

from pykickstart.errors import *

class FC3_TestCase(CommandTest):
    command = "timezone"

    def runTest(self):
        # pass
        self.assert_parse("timezone Eastern", "timezone  Eastern\n")

        # On FC6 and later, we write out --isUtc regardless of what the input was.
        if self.__class__.__name__ == "FC3_TestCase":
            self.assert_parse("timezone --utc Eastern", "timezone --utc Eastern\n")
        else:
            self.assert_parse("timezone --utc Eastern", "timezone --isUtc Eastern\n")

        # fail
        self.assert_parse_error("timezone", KickstartValueError)
        self.assert_parse_error("timezone Eastern Central", KickstartValueError)
        self.assert_parse_error("timezone --blah Eastern")
        self.assert_parse_error("timezone --utc", KickstartValueError)

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("timezone --isUtc Eastern", "timezone --isUtc Eastern\n")

        # fail
        self.assert_parse_error("timezone --isUtc", KickstartValueError)

class F18_TestCase(FC6_TestCase):
    def runTest(self):
        # pass
        self.assert_parse("timezone --utc Europe/Prague")
        self.assert_parse("timezone --isUtc Europe/Prague\n")
        self.assert_parse("timezone --isUtc Eastern", "timezone Eastern --isUtc\n")
        self.assert_parse("timezone Europe/Prague")
        self.assert_parse("timezone Europe/Prague --nontp",
                          "timezone Europe/Prague --nontp\n")
        self.assert_parse("timezone Europe/Prague "\
                          "--ntpservers=ntp.cesnet.cz,tik.nic.cz")
        self.assert_parse("timezone Europe/Prague --ntpservers=ntp.cesnet.cz,",
                          "timezone Europe/Prague --ntpservers=ntp.cesnet.cz\n")

        # fail
        self.assert_parse_error("timezone", KickstartValueError)
        self.assert_parse_error("timezone Eastern Central", KickstartValueError)
        self.assert_parse_error("timezone --blah Eastern")
        self.assert_parse_error("timezone --utc", KickstartValueError)
        self.assert_parse_error("timezone --isUtc", KickstartValueError)
        self.assert_parse_error("timezone Europe/Prague --nontp "\
                                "--ntpservers=ntp.cesnet.cz",
                                KickstartParseError)
        self.assert_parse_error("timezone Europe/Prague --ntpservers="\
                                "ntp.cesnet.cz, tik.nic.cz",
                                KickstartValueError)

if __name__ == "__main__":
    unittest.main()
