
def make_product_public(product):
    product.status = 'public'
    product.save()