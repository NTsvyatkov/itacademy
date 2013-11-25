import unittest
from business_logic.user_manager import *


class UserManagerTest(unittest.TestCase):

    def setUp(self):
        self.login = 'Alex'
        self.firstName = 'Alexander'
        self.lastName = 'Ivanov'
        self.password = 'password'
        self.email = 'alex.ivanov@gmail.ru'
        self.roleId = 1
        self.userId = 1

    def testCorrectLogin(self):
        self.assertNotEqual(validationLogin(self.login), BaseException)

    def testCorrectFirstName(self):
        self.assertNotEqual(validationFirstName(self.firstName), BaseException)

    def testCorrectLastName(self):
        self.assertNotEqual(validationLastName(self.lastName), BaseException)

    def testCorrectRoleId(self):
        self.assertNotEqual(validationRoleID(self.roleId), BaseException)

    def testCorrectUserById(self):
        self.assertIsNotNone(getUserByID(self.userId))

    def testCorrectPassword(self):
        self.assertNotEqual(validationPassword(self.password), BaseException)

    def testCorrectEmail(self):
        self.assertNotEqual(validationEmail(self.email), BaseException)

if __name__ == '__main__':
    unittest.main()

