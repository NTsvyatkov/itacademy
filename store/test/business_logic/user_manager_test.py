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
        self.assertRaises(ValidationException,validationLogin(self.login))

    def testCorrectFirstName(self):
        self.assertRaises(ValidationException, validationFirstName(self.firstName))

    def testCorrectLastName(self):
        self.assertRaises(ValidationException, validationLastName(self.lastName))

    def testCorrectRoleId(self):
        self.assertRaises(ValidationException, validationRoleID(self.roleId))

    def testCorrectUserById(self):
        self.assertIsNotNone(getUserByID(self.userId))

    def testCorrectPassword(self):
        self.assertRaises(ValidationException, validationPassword(self.password))

    def testCorrectEmail(self):
        self.assertRaises(ValidationException, validationEmail(self.email))

if __name__ == '__main__':
    unittest.main()

