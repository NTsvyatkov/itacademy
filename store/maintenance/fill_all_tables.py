from models.product_dao import Product, Dimension
from models.product_stock_dao import ProductStock
from models.region_dao import RegionDao
from models.role_dao import RoleDao
from models.user_dao import UserDao, UserLevel
from models.order_dao import Order, OrderProduct, OrderStatus,DeliveryType
from models.product_stock_dao import ProductStock

from datetime import date

# This file can fill you DB store_db
# just run this file

Dimension.add_dimension("Items", 1)
Dimension.add_dimension("Box", 5)
Dimension.add_dimension("Package", 10)

Product.add_product('apple', 'sweet apple', 1.5)
Product.add_product('potato', 'ukrainian potato', 5.5)
Product.add_product('apple', 'red apple', 10.0)
Product.add_product('orange', 'tasty orange', 1.2)
Product.add_product('banana', 'yellow banana', 7.0)
Product.add_product('lemon', 'yellow lemon', 11.0)
Product.add_product('tomato', 'red tomato', 2.5)
Product.add_product('mango', 'ugly mango', 1.8)
Product.add_product('apple', 'russian apple', 0.5)
Product.add_product('orange', 'italian orange', 15.0)
Product.add_product('apple', 'sweet apple', 11.3)
Product.add_product('banana', 'brazilian banana', 12.1)
Product.add_product('tomato', 'ukrainian tomato', 5.8)
Product.add_product('mango', 'fresh mango', 7.5)
Product.add_product('lemon', 'indian lemon', 4.4)

ProductStock.add_new_record(1,1,15)
ProductStock.add_new_record(2,1,10)
ProductStock.add_new_record(3,3,15)
ProductStock.add_new_record(4,1,18)
ProductStock.add_new_record(5,2,15)
ProductStock.add_new_record(6,1,25)
ProductStock.add_new_record(11,1,15)
ProductStock.add_new_record(11,2,15)
ProductStock.add_new_record(1,2,10)
ProductStock.add_new_record(3,1,15)

RoleDao.createNewRole("Administrator")
RoleDao.createNewRole("Merchandiser")
RoleDao.createNewRole("Supervisor")
RoleDao.createNewRole("Customer")

RegionDao.createNewRegion("North")
RegionDao.createNewRegion("West")
RegionDao.createNewRegion("South")
RegionDao.createNewRegion("East")

UserDao.createNewUser('Max', '111','Maxim','Sidorov', 'max.sidorov@gmail.ru',1,2)
UserDao.createNewUser('Nikol', '111','Nikolay','Lobanov', 'giman89@gmail.ru', 4,1)
UserDao.createNewUser('Vanya', '111','Ivan','Ivanov', 'vanya@gmail.com', 2,1)
UserDao.createNewUser('Andrew', '111','Andrew','Petrov', 'andrew@mail.ru', 3,4)
UserDao.createNewUser('Katya', '111','Ekaterina','Ivanova', 'ekaterina@rambler.com', 4,3)
UserDao.createNewUser('Roma', '111','Roman','Melnishin', 'roma90@gmail.com', 2,1)
UserDao.createNewUser('Den', '111','Dennis','Popov', 'popov@mail.ru', 3,1)
UserDao.createNewUser('Max90', '111','Maxim','Smirnov', 'smirnov@gmail.ru', 4,4)
UserDao.createNewUser('Yaroslav', '111','Yaroslav','Lobanov', 'lobanov95@gmail.ru', 4,2)
UserDao.createNewUser('Seriy', '111','Sergey','Lobanov', 'global85@gmail.ru', 1,2)
UserDao.createNewUser('Dona', '111','Donna','Popova', 'popova@mail.ru', 3,1)



DeliveryType.add_delivery('Courier')
DeliveryType.add_delivery('Express-mail')
DeliveryType.add_delivery('Himself')

OrderStatus.add_status('Ordered')
OrderStatus.add_status('Delivered')
OrderStatus.add_status('Created')
OrderStatus.add_status('Pending')


Order.add_order(1,date.today(),2,2,12,2)
Order.add_order(3,date.today(),1,1,43,1)
Order.add_order(2,date.today(),1,2,31,2)
Order.add_order(4,date.today(),3,2,53,1)
Order.add_order(2,date.today(),2,3,42,2)
Order.add_order(2,date.today(),2,3,42,2)

Order.add_order(5,date.today(),1,2,40,1,13/11/2013,15/11/2013)
Order.add_order(5,date.today(),2,2,40,2,13/11/2013,15/11/2013)
Order.add_order(5,date.today(),3,2,40,2,13/11/2013,15/11/2013)
Order.add_order(5,date.today(),4,2,40,4,13/11/2013,15/11/2013)

Order.add_order(1,date.today(),2,3)

OrderProduct.add_order_product(2,4,1,5)
OrderProduct.add_order_product(4,11,2,1)
OrderProduct.add_order_product(1,7,3,3)
OrderProduct.add_order_product(4,3,3,2)
OrderProduct.add_order_product(5,1,2,1)
OrderProduct.add_order_product(6,3,1,4)
OrderProduct.add_order_product(4,2,1,2)
OrderProduct.add_order_product(4,5,2,5)
OrderProduct.add_order_product(4,6,1,4)
OrderProduct.add_order_product(4,7,3,2)
OrderProduct.add_order_product(4,11,1,1)

UserLevel.add_user_level('Standard', 0, 0)
UserLevel.add_user_level('Silver', 1000, 5)
UserLevel.add_user_level('Gold', 3000, 10)
UserLevel.add_user_level('Platinum', 10000, 15)
