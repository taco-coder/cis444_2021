global cart

cart = []

def get_cart():
  return cart

def add_to_cart(book_data):
  cart.append(book_data)
  
def clear_cart():
  cart.clear()
  