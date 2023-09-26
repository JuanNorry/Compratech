class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, componente):
        id = str(componente.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "componente_id": componente.id,
                "producto": componente.producto,
                "categoria": componente.categoria,
                "acumulado": componente.precio,
                "stock": componente.stock,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += componente.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, componente):
        id = str(componente.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, componente):
        id = str(componente.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= componente.precio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(componente)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True