class CarritoDeCompras:
    def __init__(self, request):
        # Inicializamos el carrito de compras
        self.session = request.session
        # Obtenemos el carrito de la sesión, si no existe lo inicializamos como un diccionario vacío

        if 'carrito' not in self.session:
            self.session['carrito'] = {}
        self.carrito = self.session['carrito']

    def agregar_plato(self, plato_id):
        # Agregamos un plato al carrito
        if str(plato_id) not in self.carrito:
            # Si el plato no está en el carrito, lo agregamos y establecemos la cantidad en 1
            self.carrito[plato_id] = {'cantidad': 1}
        else:
            # Si el plato ya está en el carrito, incrementamos la cantidad en 1
            self.carrito[plato_id]['cantidad'] += 1
        self.guardar_carrito()

    def quitar_plato(self, plato_id):
        plato_id = str(plato_id)
        if self.carrito[plato_id]['cantidad'] <= 1:
            self.eliminar_plato(plato_id)
        else:
            self.carrito[plato_id]['cantidad'] -= 1
        self.guardar_carrito()

    def eliminar_plato(self, plato_id):
        # Eliminamos un plato del carrito
        if str(plato_id) in self.carrito:
            # Si el plato está en el carrito, lo eliminamos
            del self.carrito[plato_id]
            self.guardar_carrito()

    def guardar_carrito(self):
        # Guardamos el carrito en la sesión
        self.session['carrito'] = self.carrito
        # Marcamos la sesión como modificada para asegurarnos de que se guarde
        self.session.modified = True

    def obtener_carrito(self):
        # Obtenemos el carrito actual
        return self.carrito

    def borrar_carrito(self):
        self.session['carrito'] = {}
        self.session.modified = True