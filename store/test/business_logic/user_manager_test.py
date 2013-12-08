import unittest
from business_logic import user_manager
from business_logic.user_manager import *
from mock import patch

class UserManagerTest(unittest.TestCase):

    def setUp(self):
        self.login = 'Alex'
        self.firstName = 'Alexander'
        self.lastName = 'Ivanov'
        self.password = 'password'
        self.email = 'alex.ivanov@gmail.ru'
        self.roleId = 1
        self.regionId = 1
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

    @patch('business_logic.user_manager.UserDao.getAllUsers')
    def testGetListUser(self,getAllUsers):
        user_manager.getListUser()
        self.assertEqual(getAllUsers.call_count, 1)

    @patch('business_logic.user_manager.UserDao.updateUser')
    def testUpdateUser(self, updateUser):
        user_manager.updateUser(self.userId,self.login, self.firstName, self.lastName, self.password, self.email,
                                self.roleId, self.regionId)
        self.assertEqual(updateUser.call_count, 1)

    @patch('business_logic.user_manager.UserDao.deleteRecord')
    def testDeleteUser(self,deleteUser):
        user_manager.deleteUser(self.userId)
        self.assertEqual(deleteUser.call_count, 1)

    @patch('business_logic.user_manager.UserDao.getUserByID')
    def testGetUser(self, getUser):
        user_manager.getUserByID(self.userId)
        self.assertEqual(getUser.call_count, 2)


if __name__ == '__main__':
    unittest.main()

