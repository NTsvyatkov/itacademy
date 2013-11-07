from models.product_dao import Product, Dimension

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

# You can check, that all products and dimensions was added. You should comment text above, and uncomment below and run
# this script one more time.

#d = Dimension.get_all_dimensions()
#for i in d:
#    print i
#
#p = Product.get_all_products()
#for i in p:
#    print i