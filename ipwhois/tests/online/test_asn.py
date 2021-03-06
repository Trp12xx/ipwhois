import json
import io
from os import path
import logging
from ipwhois.tests import TestCommon
from ipwhois.exceptions import (WhoisLookupError, HTTPLookupError,
                                ASNRegistryError)
from ipwhois.net import Net
from ipwhois.asn import (IPASN, ASNOrigin)

LOG_FORMAT = ('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s] '
              '[%(funcName)s()] %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
log = logging.getLogger(__name__)


class TestIPASN(TestCommon):

    def test__TestIPASNLookup(self):

        net = Net('74.125.225.229')
        ipasn = IPASN(net)

        try:
            self.assertIsInstance(ipasn.lookup(inc_raw=True), dict)
        except (HTTPLookupError, ASNRegistryError):
            pass
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        net = Net(address='74.125.225.229', timeout=0,
                  allow_permutations=False)
        ipasn = IPASN(net)
        self.assertRaises(ASNRegistryError, ipasn.lookup)

        net = Net(address='74.125.225.229', timeout=0,
                  allow_permutations=True)
        ipasn = IPASN(net)
        self.assertRaises(HTTPLookupError, ipasn.lookup, **dict(
            asn_alts=['http']))


class TestASNOrigin(TestCommon):

    def test__TestASNOriginLookup(self):

        data_dir = path.abspath(path.join(path.dirname(__file__), '..'))

        with io.open(str(data_dir) + '/asn.json', 'r') as \
                data_file:
            data = json.load(data_file)

        # IP doesn't matter here
        net = Net('74.125.225.229')

        for key, val in data.items():

            log.debug('Testing: {0} - {1}'.format(key, val['asn']))

            obj = ASNOrigin(net)
            try:

                self.assertIsInstance(
                    obj.lookup(
                        asn=val['asn']
                    ),
                    dict
                )

            except WhoisLookupError:

                pass

            except AssertionError as e:

                raise e

            except Exception as e:

                self.fail('Unexpected exception raised: {0}'.format(e))

        net = Net(address='74.125.225.229', timeout=0,
                  allow_permutations=True)
        asnorigin = ASNOrigin(net)
        self.assertRaises(HTTPLookupError, asnorigin.lookup, **dict(
            asn='15169',
            asn_alts=['http']))

