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

    #def testIsUserExist(self):
        #my_mock = Mock()
        #my_mock.some_method.return_value = False
        #self.assertEqual(True, my_mock.UserDao.isUserExists(self.login, self.password))
        #self.assertEqual(UserDao.isUserExists(self.login, self.password), True)

    def testGetUserById(self):
        mock = MagicMock()
        #result = mock('Alex', 'Alexander', 'Ivanov', 'password', 'alex.ivasnov@gmail.ru', 1,1)
        #mock.method_calls = UserDao.getUserByID(self.id)



    #def tearDown(self):
    #    user = UserDao.getUserByLogin(self.login, self.password)
    #    UserDao.deleteRecord(user.id)

if __name__ == '__main__':
    unittest.main()

