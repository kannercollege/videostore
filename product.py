class Product:
    def __init__(self, id: int, name: str, price: float, image_filename: str):
        self.id = id
        self.name = name
        self.price = round(price, 2)
        self.image_filename = image_filename
