class product():

    id =0
    name = ''
    price = ''
    quantity = ''

    def __init__(self, name='', price=0,quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

p=product()

print(p.__class__.__name__)