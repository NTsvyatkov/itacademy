import unittest
from mock import patch
from business_logic import order_manager
from models.order_dao import Order, OrderProduct


class OrderTest(unittest.TestCase):

    def setUp(self):
        self.json = {'value': 1, 'status': 3}
        self.userId = 4
        self.productId = 11
        self.dimension_id = 2

    @patch('business_logic.order_manager.Order.getAllOrders')
    def testGetListOrders(self, getAllOrders):
        order_manager.getListOrder()
        self.assertEqual(getAllOrders.call_count, 1)

    @patch('business_logic.order_manager.OrderStatus.get_all_order_status')
    def testStatusList(self, getListStatus):
        order_manager.list_status()
        self.assertEqual(getListStatus.call_count, 1)

    @patch('business_logic.order_manager.DeliveryType.get_delivery_all')
    def testDeliveryList(self, getDeliveryList):
        order_manager.list_delivery()
        self.assertEqual(getDeliveryList.call_count, 1)

    @patch('business_logic.order_manager.Order.getOrderByStatus')
    @patch('business_logic.order_manager.OrderProduct.get_order_product')
    @patch('business_logic.order_manager.OrderProduct.updateSumQuantity')
    @patch('business_logic.order_manager.OrderProduct.add_order_product')
    def testAddProductToCartStatus(self, orderStatus, orderProduct, updateSum, addOrder):
        order_manager.addProductToCartStatus(self.userId,self.productId, self.json)
        self.assertEqual(orderStatus.call_count, 0)
        self.assertEqual(orderProduct.call_count, 1)
        self.assertEqual(updateSum.call_count, 1)
        self.assertEqual(addOrder.call_count, 1)

if __name__ == '__main__':
    unittest.main()