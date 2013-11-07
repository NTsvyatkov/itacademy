from models.product_dao import Product, Dimension
from models.region_dao import RegionDao
from models.role_dao import RoleDao
from models.user_dao import UserDao
from models.order_dao import Order, OrderProduct, OrderStatus,DeliveryType
from datetime import date

# This file can fill you DB store_db
# just run this file

Dimension.add_dimension("item")
Dimension.add_dimension("box")
Dimension.add_dimension("package")

Product.add_product('apple', 'sweet apple', 1.5, 1)
Product.add_product('potato', 'ukrainian potato', 5.5, 2)
Product.add_product('apple', 'red apple', 10.0, 3)
Product.add_product('orange', 'tasty orange', 1.2, 1)
Product.add_product('banana', 'yellow banana', 7.0, 2)
Product.add_product('lemon', 'yellow lemon', 11.0, 3)
Product.add_product('tomato', 'red tomato', 2.5, 1)
Product.add_product('mango', 'ugly mango', 1.8, 1)
Product.add_product('apple', 'russian apple', 0.5, 1)
Product.add_product('orange', 'italian orange', 15.0, 3)
Product.add_product('apple', 'sweet apple', 11.3, 3)
Product.add_product('banana', 'brazilian banana', 12.1, 3)
Product.add_product('tomato', 'ukrainian tomato', 5.8, 2)
Product.add_product('mango', 'fresh mango', 7.5, 2)
Product.add_product('lemon', 'indian lemon', 4.4, 2)


RoleDao.createNewRole("Admin")
RegionDao.createNewRegion("Crimea")

UserDao.createNewUser('Max', '111','Maxim','Sidorov', 'max.sidorov@gmail.ru', 1,1)
UserDao.createNewUser('Vanya', '111','Ivan','Ivanov', 'vanya@gmail.com', 1,1)
UserDao.createNewUser('Andrew', '111','Andrew','Petrov', 'andrew@mail.ru', 1,1)
UserDao.createNewUser('Katya', '111','Ekaterina','Ivanova', 'ekaterina@rambler.com', 1,1)


DeliveryType.add_delivery('Courier')
DeliveryType.add_delivery('Express-mail')
DeliveryType.add_delivery('Himself')

OrderStatus.add_status('In Stock')
OrderStatus.add_status('Delivery process')
OrderStatus.add_status('Delivered')

Order.add_order(1,date.today(),2,2)
Order.add_order(3,date.today(),1,1)
Order.add_order(2,date.today(),1,2)
Order.add_order(4,date.today(),3,2)
Order.add_order(2,date.today(),3,3)
Order.add_order(1,date.today(),2,3)

OrderProduct.add_order_product(2,4,5)
OrderProduct.add_order_product(4,11,1)
OrderProduct.add_order_product(1,7,3)
OrderProduct.add_order_product(3,3,2)
OrderProduct.add_order_product(5,1,1)
OrderProduct.add_order_product(6,3,4)



