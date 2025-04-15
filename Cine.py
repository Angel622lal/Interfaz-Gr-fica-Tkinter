import json
import os

clas_pers = "pers.json"
clas_reser = "reserva.json"
clas_fun = "funcion.json"
clas_pelicula = "pelicula.json"
clas_promo = "promo.json"

class Persona:

    pers = []

    def __init__(self, nombre, contacto, tipo,  rol=None):
        self.nombre = nombre
        self.contacto = contacto
        self.tipo = tipo
        self.rol = rol
    
    def registrar(self):
        Persona.pers.append(self)
        print(f"Se ha registrado el {self.tipo}")
    
    def actualizar_datos(self, nom, cambio):
        nom = nom.upper()
        if "NOMBRE" == nom:
            self.nombre = cambio

        if "CONTACTO" == nom.upper():
            self.contacto = cambio

        print(f"Se ha actualizado el campo {nom}")

    @classmethod
    def cargar_usuarios(cls):
        Persona.pers.clear()
        if os.path.exists(clas_pers):
            with open(clas_pers, "r") as file:
                data = json.load(file)
                for usuario_data in data:
                    Usuario(usuario_data["nombre"], usuario_data["rol"], usuario_data["password"])

    @classmethod
    def personas_registradas(cls):
        print("Personas registradas")
        for per in cls.pers:
            print(f"-{per.nombre} - {per.contacto} - {per.tipo}")

class Empleado(Persona):
    def __init__(self, nombre, contacto, tipo, rol):
        super().__init__(nombre, contacto, tipo, rol)
        self.rol = rol
        #Persona.pers.append(self)
    
    def agregar_funcion(self, funcion):
        funcion.registrar_funcion()

    def agregar_pelicula(self, pelicula):
        pelicula.registrar_pelicula()

    def agregar_promocion(self, promocion):
        promocion.registrar_promocion()
    
    @classmethod
    def guardar_empleado(cls):
        aux = []
        for persona in Persona.pers:
            aux.append({
                "nombre": persona.nombre,
                "contacto": persona.contacto,
                "tipo": persona.tipo,
                "rol": persona.rol
            })
        with open(clas_pers, "w") as file:
            json.dump(aux, file, indent=4)
       

class Usuario(Persona):
    def __init__(self, nombre, contacto, tipo):
        super().__init__(nombre, contacto, tipo)
        #Persona.pers.append(self)

    def confirmar_reserva(self, reserva):
        reserva.confirmar_reserva()
        
    def cancelar_reserva(self, reserva):
        reserva.cancelar_reserva()

    def acceder_promo(self, reserva, promocion):
        reserva.aplicar_promo(promocion)
    
    @classmethod
    def guardar_usuario(cls):
        aux = []
        for persona in Persona.pers:
            aux.append({
                "nombre": persona.nombre,
                "contacto": persona.contacto,
                "tipo": persona.tipo
            })
        with open(clas_pers, "w") as file:
            json.dump(aux, file, indent=4)


class Reservar:
    list_reserva = {}
    def __init__(self, usuario, funcion, asiento):
        self.usuario = usuario
        self.funcion = funcion
        self.asiento_selec = asiento

    def registrar_reserva(self):
        Reservar.list_reserva[self.funcion.pelicula.titulo] = {
            "usuario": self.usuario.nombre,
            "asiento": self.asiento_selec
        }
        print(f"Reserva confirmada para {self.usuario.nombre}, para la funciom {self.funcion.pelicula.titulo} con asientos: {self.asiento_selec}")
    
    def confirmar_reserva(self):
        if self.funcion not in Funcion.list_funciones:
            print(f"No se encontro la funcion {self.funcion}")
            return
        
        boletos_disponibles = set(self.funcion.list_boletos)
        boletos_elegidos = set(self.asiento_selec)

        if not boletos_elegidos.issubset(boletos_disponibles):
            print(f"Algunos de los asientos {self.asiento_selec} estan ocupados o no existen.")
            return
        
        for boletos in boletos_elegidos:
            self.funcion.list_boletos.remove(boletos)

        print("La reserva ha sido confirmada")

    def aplicar_promo(self, promocion):
        promocion.aplicar_promo()

    def cancelar_reserva(self):
        if self.asiento_selec == None:
            print(f"No existe reserva")
            return

        for asiento in self.asiento_selec:
            self.funcion.list_boletos.append(asiento)

        self.asiento_selec = None
        print("La reserva ha sido cancelada")

    @classmethod
    def guardar_reserva(cls):
        aux = []
        for funcion, datos in Reservar.list_reserva.items():
            aux.append({
                "usuario": datos["usuario"],
                "funcion": funcion,
                "asiento": datos["asiento"]
            })
        with open(clas_reser, "w") as file:
            json.dump(aux, file, indent=4)

class Pelicula:
    list_peliculas = []
    def __init__(self, titulo, genero, duracion, clasificacion):
        self.titulo = titulo
        self.genero = genero
        self.duracion = duracion
        self.clasificacion = clasificacion

    def registrar_pelicula(self):
        Pelicula.list_peliculas.append(self)
        print("Se ha registrado la pelicula en el catalogo")

    @classmethod
    def guardar_pelicula(cls):
        aux = []
        for datos in Pelicula.list_peliculas:
            aux.append({
                "hora": datos.titulo,
                "sala": datos.genero,
                "pelicula": datos.duracion,
                "boletos": datos.clasificacion
            })
        with open(clas_pelicula, "w") as file:
            json.dump(aux, file, indent=4)

    @classmethod
    def detalles_de_pelicula(cls):
        for pelicula in cls.list_peliculas:
            print(f"La pelicula {pelicula.titulo} es de clasificacion {pelicula.clasificacion}, es del genero {pelicula.genero}, y tiene una duracion de {pelicula.duracion}")

class Funcion:
    list_funciones = []
    def __init__(self, hora, sala, pelicula):
        self.hora = hora
        self.sala = sala
        self.pelicula = pelicula
        self.list_boletos = sala.list_asientos[:]

    def registrar_funcion(self):
        Funcion.list_funciones.append(self)
        print("La funcion ha sido programada ")

    def consultar_boletos(self):
        print("Asientos libres")
        for i in range(0, len(self.list_boletos), 10):
            print(*self.list_boletos[i:i+10], sep=" ")

    @classmethod
    def guardar_funcion(cls):
        aux = []
        for datos in Funcion.list_funciones:
            aux.append({
                "hora": datos.hora,
                "sala": datos.sala.identificador,
                "pelicula": datos.pelicula.titulo,
                "boletos": datos.sala.list_asientos[:]
            })
        with open(clas_fun, "w") as file:
            json.dump(aux, file, indent=4)


    @classmethod
    def funciones_del_dia(cls):
        for funcion in cls.list_funciones:
            print(f"{funcion.pelicula.titulo} en {funcion.sala.identificador} a las {funcion.hora}")


class Espacio:
    list_espacio = []
    def __init__(self,capacidad,identificador):
        self.capacidad=capacidad
        self.identificador=identificador

    def registrar(self):
        Espacio.list_espacio(self)
        print(f"Se ha registrado el {self.identificador}")
    
    def descripcion(self):
        print(f"El edificio tiene tamaño {self.capacidad} y tiene id {self.identificador}")
         
class Sala(Espacio):
    list_asientos = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", 
                    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", 
                    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", 
                    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", 
                    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", 
                    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]
    def __init__(self, capacidad, identificador, tipo):
        super().__init__(capacidad, identificador)
        self.tipo = tipo             
        self.disponibilidad = True
        
    def consultar_disponibilidad(self):
        if self.disponibilidad:  
            print("La sala esta disponible")
        else:
            print("La sala esta ocupada")

    @classmethod
    def consultar_boletos(self):
        print("Asientos libres")
        for i in range(0, len(Sala.list_asientos), 10):
            print(*Sala.list_asientos[i:i+10], sep=" ")

class Zona_de_comida:
    def __init__(self, capacidad, identificador):
        super().__init__(capacidad, identificador)       
     
class Promocion:
    list_descuentos = []
    def __init__(self, descuento, condicion, producto):
        self.descuento = descuento
        self.condicion = condicion
        self.producto = producto

    def registrar_promocion(self):
        Promocion.list_descuentos.append(self)
        print(f"Promocion registrada")

    def aplicar_promo(self):
        print(f"Se ha aplicado la promocion")

    @classmethod
    def guardar_promocion(cls):
        aux = []
        for datos in Promocion.list_descuentos:
            aux.append({
                "descuento": datos.descuento,
                "condicion": datos.condicion,
                "producto": datos.producto
            })
        with open(clas_promo, "w") as file:
            json.dump(aux, file, indent=4)

    @classmethod
    def mostrar_promociones(cls):
        for oferta in Promocion.list_descuentos:
            print(f"Promocion: {oferta.descuento}% de descuento en {oferta.producto}, Condiciones: {oferta.condicion}")

'''
#Peliculas
Peli1 = Pelicula("Matrix", "Ciencia Ficción", "1 hora con 30 min", "Clasificacion A")
Peli2 = Pelicula("Titanic", "Drama/Romance", "2 horas con 30 min", "Clasificacion B")

#Salas
Sal1 = Sala(60,"Sala 1","3DX")
Sal2 = Sala(60,"Sala 2","Tradicional")

#Funciones
funcion1 = Funcion("18:00", Sal1, Peli1)
funcion2 = Funcion("20:00", Sal2, Peli2)

#Promociones
Prom1 = Promocion(20, "Canjear antes del 14 de Febrero", "Boletos")
Prom2 = Promocion(40, "Canjear antes del 3 de Octubre", "Palomitas")

#Usuarios
print("\n--- Registrando Usuarios ---")
Us1 = Usuario("Angel Camacho", "angel@email.com", "Usuario") 
Us1.registrar()
Us2 = Usuario("Ricardo Salinas", "ricardo@email.com", "Usuario") 
Us2.registrar()
Us3 = Usuario("Mario Almada", "mario@email.com", "Usuario") 
Us3.registrar()
#Usuario.guardar_usuario()
#Empleados
print("\n--- Registrando Empleados ---")
Emp1 = Empleado("Leonel Torres", "leonel@email.com", "Empleado", "Administrador")
Emp1.registrar()
Emp2 = Empleado("Manuel Santos", "manuel@email.com", "Empleado", "Taquillero") 
Emp2.registrar()
Emp3 = Empleado("Carlos Hernandez", "carlos@email.com", "Empleado", "Limpieza") 
Emp3.registrar()
Empleado.guardar_empleado()

#Registrar pelicula
print("\n--- Acciones de Empleado Administrador ---")
Emp1.agregar_pelicula(Peli1)
Emp1.agregar_pelicula(Peli2)
#Pelicula.guardar_pelicula()

#Registrar funciones
Emp1.agregar_funcion(funcion1)
Emp1.agregar_funcion(funcion2)
#Funcion.guardar_funcion()

#Registrar promocion
Emp1.agregar_promocion(Prom1)
Emp1.agregar_promocion(Prom2)
#Promocion.guardar_promocion()

#Registrar Reserva
Reserva1 = Reservar(Us2, funcion1, ["A3", "B4", "D7"])
Reserva1.registrar_reserva()
#Reservar.guardar_reserva()

print("\n--- Asientos Disponibles en la funcion ---")
funcion1.consultar_boletos()

print("\n--- Acceder a promociones ---")
Us1.acceder_promo(Reserva1, Prom1)

print("\n--- Acciones del Usuario ---")
Us1.confirmar_reserva(Reserva1)

print("\n--- Asientos Disponibles despues de reservar ---")
funcion1.consultar_boletos()
'''
Us1.cancelar_reserva(Reserva1)

print("\n--- Asientos Disponibles despues de cancelar reserva ---")
funcion1.consultar_boletos()
'''

