import unittest
from models.user_dao import UserDao
from mock import MagicMock, Mock


class UserManagerTest(unittest.TestCase):

    def setUp(self):
        self.id = 1
        self.login = 'Alex'
        self.firstName = 'Alexander'
        self.lastName = 'Ivanov'
        self.password = 'password'
        self.email = 'alex.ivasnov@gmail.ru'
        self.roleId = 1
        self.regionId = 1

    def testAddUser(self):
        real = UserDao.createNewUser
        real.method = Mock()
        real.method(self.login,self.password, self.firstName, self.lastName,self.email, self.roleId,
                              self.regionId)
        real.method.assert_called_with(self.login,self.password, self.firstName, self.lastName,self.email, self.roleId,
                              self.regionId)

    def testIsUserExist(self):
        self.assertEqual(UserDao.isUserExists(self.login, self.password), False)

    def testGetUserById(self):
        self.assertNotEqual(UserDao.getUserByID(1), None)

    def tearDown(self):
        user = UserDao.getUserByLogin(self.login, self.password)
        if user:
            UserDao.deleteRecord(user.id)

if __name__ == '__main__':
    unittest.main()

