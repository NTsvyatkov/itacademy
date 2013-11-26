import unittest
from business_logic.order_manager import addProductToCartStatus, addOrderWithStatusCart
from models.order_dao import Order, OrderProduct


class OrderTest(unittest.TestCase):

    def setUp(self):
        self.json = {'value': 1}
        self.userId = 4
        self.productId = 3

    def testAddOrderWithStatusCart(self):
        addOrderWithStatusCart(self.userId)
        order = Order.getOrderByStatus(self.userId)
        self.assertEqual(self.userId,order.user_id)

    def testAddProductToCartStatus(self):
        addProductToCartStatus(self.userId, self.productId, self.json)
        order = Order.getOrderByStatus(self.userId)
        product = OrderProduct.get_order_product(order.id,self.productId)
        self.assertEqual(self.productId,product.product_id)

if __name__ == '__main__':
    unittest.main()