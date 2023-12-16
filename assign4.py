# Name: Aric Aggarwal
# Student Id: 251350481
# The file includes classes: InventoryProduct, product, inventory, shopping cart and a product catalog
# includes functions: populate_catalog, populate_inventory

class Product:
    def __init__(self, name, price, category):
        # Initialize product attributes
        self._name = name
        self._price = int(price)
        self._category = category

    # Define how products are classified
    def __eq__(self, other):
        if isinstance(other, Product):
            if (self._name == other._name and self._price == other._price) and (self._category == other._category):
                return True
            else:
                return False
        else:
            return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        rep = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return rep


# represents a product in an inventory store
class InventoryProduct:

    def __init__(self, productName, productPrice, productQuantity):
        self.name = productName
        self.price = productPrice
        self.quantity = productQuantity

    def get_name(self):
        return self.name

    def get_price(self):
        return int(self.price)

    def get_quantity(self):
        return int(self.quantity)

    def set_name(self, productName):
        self.name = productName

    def set_price(self, productPrice):
        self.price = str(productPrice)

    def set_quantity(self, productQuantity):
        self.quantity = str(productQuantity)


# provides data structures and methods for Inventory management
class Inventory:
    def __init__(self):
        self.inventory_store = {}

    # adds a new product to  inventory
    def add_to_productInventory(self, productName, productPrice, productQuantity):
        product = InventoryProduct(productName, productPrice, productQuantity)

        self.inventory_store[productName] = product

    # adds quantity of a product
    def add_productQuantity(self, nameProduct, addQuantity):
        quantity = self.inventory_store[nameProduct].get_quantity() + addQuantity

        self.inventory_store[nameProduct].set_quantity(quantity)

    # removes product quantity
    def remove_productQuantity(self, nameProduct, removeQuantity):
        quantity = self.inventory_store[nameProduct].get_quantity() - removeQuantity

        self.inventory_store[nameProduct].set_quantity(quantity)

    # gets product price
    def get_productPrice(self, nameProduct):
        return self.inventory_store[nameProduct].get_price()

    # gets product quantity
    def get_productQuantity(self, nameProduct):
        return self.inventory_store[nameProduct].get_quantity()

    # print inventory
    def display_Inventory(self):
        # print the inventory items
        for name, product in self.inventory_store.items():
            print("%s, %d, %d" % (product.get_name(), product.get_price(), product.get_quantity()))


# class that provides the data structures and methods for a shopping cart
class ShoppingCart:

    # initialize class members
    def __init__(self, buyerName, inventory):

        self.shopping_cart = {}
        self.buyer = buyerName
        self.inventory = inventory

    # adds an item to cart
    def add_to_cart(self, nameProduct, requestedQuantity):

        # checks product quantity inventory
        if self.inventory.get_productQuantity(nameProduct) >= requestedQuantity:

            # if a product already in cart
            if nameProduct in self.shopping_cart:

                quantity = self.shopping_cart[nameProduct] + requestedQuantity

                self.shopping_cart[nameProduct] = quantity

            else:
                # set quantity of an item in cart
                self.shopping_cart[nameProduct] = requestedQuantity

                # inventory update
            self.inventory.remove_productQuantity(nameProduct, requestedQuantity)

            return "Filled the order"
        else:
            return "Can not fill the order"

    # removes a product from cart
    def remove_from_cart(self, nameProduct, requestedQuantity):

        # check if the product in the shopping cart
        if nameProduct in self.shopping_cart:

            # check  the quantity of a product in cart
            if requestedQuantity <= self.shopping_cart[nameProduct]:

                quantity = self.shopping_cart[nameProduct] - requestedQuantity

                # remove the requestedQuantity
                self.shopping_cart[nameProduct] = quantity

                # update the inventory
                self.inventory.add_productQuantity(nameProduct, requestedQuantity)

                return "Successful"
            else:
                return "The requested quantity to be removed from cart exceeds what is in the cart"
        else:
            # return string message
            return "Product not in the cart"

    # prints the cart
    def view_cart(self):

        cart_total = 0

        for name, quantity in self.shopping_cart.items():
            print("%s %d" % (name, quantity))

            # sum the price of products
            cart_total += (self.inventory.get_productPrice(name) * quantity)

        # print the more information
        print("Total: %d" % cart_total)
        print("Buyer Name: %s" % self.buyer)


# provides data structures and methods for Catalog
class ProductCatalog:

    # initialize class members
    def __init__(self):
        self.products = {
            "low_price_product": [],
            "medium_price_product": [],
            "high_price_product": [],
            "all": []
        }

    # adds a product
    def addProduct(self, product):
        # add product to the products list
        self.products["all"].append(product)

    # categorizes product
    def price_category(self):

        for product in self.products["all"]:

            if product.get_price() <= 99:
                self.products["low_price_product"].append(product)
            elif product.get_price() >= 100 and product.get_price() <= 499:
                self.products["medium_price_product"].append(product)

            else:
                self.products["high_price_product"].append(product)

        # print analyses data
        print("Number of low price items: %d" % len(self.products["low_price_product"]))
        print("Number of medium price items: %d" % len(self.products["medium_price_product"]))
        print("Number of high price items: %d" % len(self.products["high_price_product"]))

    # prints the catalog
    def display_catalog(self):
        # loop through the product
        for product in self.products["all"]:
            print("Product: %s Price: %d Category: %s" % (
                product.get_name(), product.get_price(), product.get_category().replace("\n", "")))


# reads a CSV file and populates the data to inventory object
def populate_inventory(filename):
    inventory = Inventory()
    try:

        # opens the file
        file = open(filename, "r")
        line = file.readline()
        while not line == "":

            split = line.split(",")
            # add items
            inventory.add_to_productInventory(split[0], split[1], split[2])
            line = file.readline()

    except IOError:
        print("Could not read file: %s" % filename)
        return

    return inventory


# read a CSV populates data to catalog
def populate_catalog(filename):
    catalog = ProductCatalog()

    try:
        # open the file
        file = open(filename, "r")
        line = file.readline()
        while not line == "":

            split = line.split(",")

            product = Product(split[0], split[1], split[3])
            # add items
            catalog.addProduct(product)
            line = file.readline()
    except IOError:
        print("Could not read file: %s" % filename)
        return

    return catalog
