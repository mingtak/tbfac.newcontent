import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import tbfac.newcontent

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['tbfac.newcontent'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              tbfac.newcontent)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='tbfac.newcontent',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='tbfac.newcontent.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='tbfac.newcontent',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for Profile
        ztc.ZopeDocFileSuite(
            'Profile.txt',
            package='tbfac.newcontent',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ArtAndLife
        ztc.ZopeDocFileSuite(
            'ArtAndLife.txt',
            package='tbfac.newcontent',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for NewNews
        ztc.ZopeDocFileSuite(
            'NewNews.txt',
            package='tbfac.newcontent',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
