import unittest
from models.user_dao import UserDao


class UserManagerTest(unittest.TestCase):

    def setUp(self):
        self.login = 'Alex'
        self.firstName = 'Alexander'
        self.lastName = 'Ivanov'
        self.password = 'password'
        self.email = 'alex.ivanov@gmail.ru'
        self.roleId = 1
        self.regionId = 1

    def testAddUser(self):
        UserDao.createNewUser(self.login,self.password, self.firstName, self.lastName,self.email, self.roleId,
                              self.regionId)
        self.assertIsNotNone(UserDao.getUserByLogin(self.login, self.password))

    def testGetUser(self):
        self.assertIsNotNone(UserDao.getUserByLogin(self.login, self.password))

    #def tearDown(self):
    #    user = UserDao.getUserByLogin(self.login, self.password)
    #    UserDao.deleteRecord(user.id)

if __name__ == '__main__':
    unittest.main()

