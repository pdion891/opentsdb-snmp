# This file is part of opentsdb-snmp.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.
import logging


class IfName:
    def __init__(self, cache=None):
        self.cache = cache

    def get_ifnames(self, snmp):
        data = snmp.walk('.1.3.6.1.2.1.31.1.1.1.1', expect_str=True)
        if not data:
            raise Exception("SNMP walk failed")
        return data

    def get_ifname(self, snmp, key):
        data = snmp.get('.1.3.6.1.2.1.31.1.1.1.1.{}'.format(key))
        return data

    def get_ifaliases(self, snmp):
        data = snmp.walk('.1.3.6.1.2.1.31.1.1.1.18', expect_str=True)
        if not data:
            raise Exception("SNMP walk failed")
        return data

    def get_ifalias(self, snmp, key):
        data = snmp.get('.1.3.6.1.2.1.31.1.1.1.18.{}'.format(key))
        return data

    def resolve(self, index, device=None):
        snmp = device.snmp
        hostname = device.hostname
        c_key = "IfName_" + hostname
        a_key = "IfName_" + hostname
        if c_key not in self.cache:
            self.cache[c_key] = self.get_ifnames(snmp)
            self.cache[a_key] = self.get_ifaliases(snmp)

        if not index:
            return None

        if index not in self.cache[c_key]:
            name = self.get_ifname(snmp, index)
            alias = self.get_ifalias(snmp, index)
            if (name):
                self.cache[c_key][index] = name
                self.cache[a_key][index] = alias
            else:
                logging.warning(
                    "Failed fetch ifname for {} index {}"
                    .format(hostname, index)
                )
                return None

        return {"interface": self.cache[c_key][index], "description": self.cache[a_key][index]}