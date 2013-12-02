import unittest
from mock import Mock, MagicMock
from business_logic.order_manager import addProductToCartStatus, addOrderWithStatusCart
from models.order_dao import Order, OrderProduct


class OrderTest(unittest.TestCase):

    def setUp(self):
        self.json = {'value': 1, 'status': 3}
        self.userId = 4
        self.productId = 11
        self.dimension_id = 2

    def testAddOrderWithStatusCart(self):
        mock = Mock()
        mock.testMethod( Order.getOrderByStatus(self.userId).id , key="4" )
        mock.mockCheckCall(self, 0, 'testMethod', "hello", key="some value" )
        #real.method(key='4')
        #order = Order.getOrderByStatus(self.userId)
        #self.assertEqual(self.userId,order.user_id)

    def testAddProductToCartStatus(self):
        addProductToCartStatus(self.userId, self.productId, self.json)
        order = Order.getOrderByStatus(self.userId)
        product = OrderProduct.get_order_product(order.id,self.productId, self.dimension_id)
        self.assertEqual(self.productId, product.product_id)

if __name__ == '__main__':
    unittest.main()