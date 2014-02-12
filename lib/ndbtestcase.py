from google.appengine.ext import testbed
import unittest


class NdbTestCase(unittest.TestCase):
    """ Setup and teardown common to tests involving ndb entities """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        super(NdbTestCase, self).setUp()

    def tearDown(self):
        self.testbed.deactivate()
        super(NdbTestCase, self).tearDown()


if __name__ == '__main__':
    unittest.main()
