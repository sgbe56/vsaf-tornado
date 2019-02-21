import unittest

from app.tests import TestMainHandler, TestLogOutHandler, TestProfileHandler
from app.tests import TestRegHandler, TestRepositoriesHandler, TestUsersJSONHandler

mainTestSuite = unittest.TestSuite()
mainTestSuite.addTests([unittest.makeSuite(TestMainHandler.TestMainHandler),
                        unittest.makeSuite(TestRegHandler.TestRegHandler),
                        unittest.makeSuite(TestProfileHandler.TestProfileHandler),
                        unittest.makeSuite(TestUsersJSONHandler.TestUsersJSONHandler),
                        unittest.makeSuite(TestRepositoriesHandler.TestRepositoriesHandler),
                        unittest.makeSuite(TestLogOutHandler.TestLogOutHandler)])

runner = unittest.TextTestRunner(verbosity=2)
runner.run(mainTestSuite)
