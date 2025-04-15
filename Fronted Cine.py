from Cine import Persona, Empleado, Usuario, Reservar, Pelicula, Funcion, Sala, Promocion 
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

clas_pers = "pers.json"
clas_reser = "reserva.json"
clas_fun = "funcion.json"
clas_pelicula = "pelicula.json"
clas_promo = "promo.json"

class CineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Cine")
        self.root.geometry("800x600")
        

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        

        self.tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text='Usuarios')
        self.setup_usuarios_tab()
        

        self.tab_peliculas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_peliculas, text='Películas')
        self.setup_peliculas_tab()
        

        self.tab_funciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_funciones, text='Funciones')
        self.setup_funciones_tab()
        

        self.tab_reservas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reservas, text='Reservas')
        self.setup_reservas_tab()
        

        self.tab_promociones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_promociones, text='Promociones')
        self.setup_promociones_tab()
        
        #self.cargar_datos()
    

    # Carga de Datos del Json

    def cargar_datos(self):
        if os.path.exists(clas_pers):
            try:
                with open(clas_pers, "r") as f:
                    personas_data = json.load(f)
                    for p in personas_data:
                        if p["tipo"] == "Empleado":
                            Empleado(p["nombre"], p["contacto"], p["tipo"], p.get("rol", "N/A")).registrar()
                        else:
                            Usuario(p["nombre"], p["contacto"], p["tipo"]).registrar()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar personas: {str(e)}")
        

        if os.path.exists(clas_pelicula):
            try:
                with open(clas_pelicula, "r") as f:
                    peliculas_data = json.load(f)
                    for peli in peliculas_data:
                        pelicula = Pelicula(peli["hora"], peli["sala"], peli["pelicula"], peli["boletos"])
                        pelicula.registrar_pelicula()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar películas: {str(e)}")
        

        if os.path.exists(clas_fun):
            try:
                with open(clas_fun, "r") as f:
                    funciones_data = json.load(f)
                    for func in funciones_data:
                        sala = Sala(60, func["sala"], "General")
                        pelicula = Pelicula(func["pelicula"], "Desconocido", "Desconocido", "Desconocido")
                        funcion = Funcion(func["hora"], sala, pelicula)
                        funcion.list_boletos = func.get("boletos", sala.list_asientos[:])
                        funcion.registrar_funcion()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar funciones: {str(e)}")
        
        
        if os.path.exists(clas_reser):
            try:
                with open(clas_reser, "r") as f:
                    reservas_data = json.load(f)
                    Reservar.list_reserva = {res["funcion"]: res for res in reservas_data}
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar reservas: {str(e)}")
        
        
        if os.path.exists(clas_promo):
            try:
                with open(clas_promo, "r") as f:
                    promos_data = json.load(f)
                    for promo in promos_data:
                        p = Promocion(promo["descuento"], promo["condicion"], promo["producto"])
                        p.registrar_promocion()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar promociones: {str(e)}")
        
        self.actualizar_lista_usuarios()
        self.actualizar_lista_peliculas()
        self.actualizar_lista_funciones()
        self.actualizar_lista_reservas()
        self.actualizar_lista_promociones()
    
    def guardar_datos(self):
        try:
            if Persona.pers:
                Usuario.guardar_usuario()

            if Pelicula.list_peliculas:
                Pelicula.guardar_pelicula()

            if Funcion.list_funciones:
                Funcion.guardar_funcion()

            if Reservar.list_reserva:
                Reservar.guardar_reserva()

            if Promocion.list_descuentos:
                Promocion.guardar_promocion()
                
            messagebox.showinfo("Guardar Datos", "Datos guardados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos: {str(e)}")
    

    #Pestañas

    def setup_usuarios_tab(self):
        frame_registro = ttk.LabelFrame(self.tab_usuarios, text="Registrar Usuario/Empleado")
        frame_registro.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(frame_registro, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ttk.Entry(frame_registro)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_registro, text="Contacto:").grid(row=1, column=0, padx=5, pady=5)
        self.contacto_entry = ttk.Entry(frame_registro)
        self.contacto_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_registro, text="Tipo:").grid(row=2, column=0, padx=5, pady=5)
        self.tipo_combobox = ttk.Combobox(frame_registro, values=["Usuario", "Empleado"])
        self.tipo_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame_registro, text="Rol (solo empleado):").grid(row=3, column=0, padx=5, pady=5)
        self.rol_entry = ttk.Entry(frame_registro)
        self.rol_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(frame_registro, text="Registrar", command=self.registrar_persona).grid(row=4, column=0, columnspan=2, pady=10)
        

        frame_lista = ttk.LabelFrame(self.tab_usuarios, text="Usuarios Registrados")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ("Nombre", "Contacto", "Tipo", "Rol")
        self.tree_usuarios = ttk.Treeview(frame_lista, columns=columns, show='headings')
        
        for col in columns:
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=150)
        
        self.tree_usuarios.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista", command=self.actualizar_lista_usuarios).pack(pady=5)
    
    def setup_peliculas_tab(self):
        frame_registro = ttk.LabelFrame(self.tab_peliculas, text="Registrar Película")
        frame_registro.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(frame_registro, text="Título:").grid(row=0, column=0, padx=5, pady=5)
        self.titulo_entry = ttk.Entry(frame_registro)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_registro, text="Género:").grid(row=1, column=0, padx=5, pady=5)
        self.genero_entry = ttk.Entry(frame_registro)
        self.genero_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_registro, text="Duración:").grid(row=2, column=0, padx=5, pady=5)
        self.duracion_entry = ttk.Entry(frame_registro)
        self.duracion_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame_registro, text="Clasificación:").grid(row=3, column=0, padx=5, pady=5)
        self.clasificacion_entry = ttk.Entry(frame_registro)
        self.clasificacion_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(frame_registro, text="Registrar Película", command=self.registrar_pelicula).grid(row=4, column=0, columnspan=2, pady=10)
        

        frame_lista = ttk.LabelFrame(self.tab_peliculas, text="Películas Registradas")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ("Título", "Género", "Duración", "Clasificación")
        self.tree_peliculas = ttk.Treeview(frame_lista, columns=columns, show='headings')
        
        for col in columns:
            self.tree_peliculas.heading(col, text=col)
            self.tree_peliculas.column(col, width=150)
        
        self.tree_peliculas.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista", command=self.actualizar_lista_peliculas).pack(pady=5)
    
    def setup_funciones_tab(self):
        frame_reg = ttk.LabelFrame(self.tab_funciones, text="Registrar Función")
        frame_reg.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(frame_reg, text="Hora:").grid(row=0, column=0, padx=5, pady=5)
        self.hora_entry = ttk.Entry(frame_reg)
        self.hora_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_reg, text="Sala (ID):").grid(row=1, column=0, padx=5, pady=5)
        self.sala_entry = ttk.Entry(frame_reg)
        self.sala_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_reg, text="Película (Título):").grid(row=2, column=0, padx=5, pady=5)
        self.peli_entry = ttk.Entry(frame_reg)
        self.peli_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(frame_reg, text="Registrar Función", command=self.registrar_funcion).grid(row=3, column=0, columnspan=2, pady=10)
        

        frame_lista = ttk.LabelFrame(self.tab_funciones, text="Funciones Registradas")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ("Hora", "Sala", "Película", "Asientos Disponibles")
        self.tree_funciones = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_funciones.heading(col, text=col)
            self.tree_funciones.column(col, width=150)
        self.tree_funciones.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista", command=self.actualizar_lista_funciones).pack(pady=5)
    
    def setup_reservas_tab(self):

        frame_reg = ttk.LabelFrame(self.tab_reservas, text="Registrar Reserva")
        frame_reg.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(frame_reg, text="Usuario (Nombre):").grid(row=0, column=0, padx=5, pady=5)
        self.reserva_usuario_entry = ttk.Entry(frame_reg)
        self.reserva_usuario_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_reg, text="Función (Película):").grid(row=1, column=0, padx=5, pady=5)
        self.reserva_funcion_entry = ttk.Entry(frame_reg)
        self.reserva_funcion_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_reg, text="Asientos (separados por coma):").grid(row=2, column=0, padx=5, pady=5)
        self.reserva_asientos_entry = ttk.Entry(frame_reg)
        self.reserva_asientos_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(frame_reg, text="Registrar Reserva", command=self.registrar_reserva).grid(row=3, column=0, columnspan=2, pady=10)
        

        frame_lista = ttk.LabelFrame(self.tab_reservas, text="Reservas Registradas")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ("Usuario", "Función", "Asientos")
        self.tree_reservas = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=150)
        self.tree_reservas.pack(fill='both', expand=True)
        

        ttk.Button(frame_lista, text="Actualizar Lista", command=self.actualizar_lista_reservas).pack(pady=5)
        ttk.Button(frame_lista, text="Cancelar Reserva", command=self.cancelar_reserva).pack(pady=5)

    def cancelar_reserva(self):
        selected_items = self.tree_reservas.selection()
        if not selected_items:
            messagebox.showerror("Error", "Seleccione una reserva para cancelar")
            return

        for item in selected_items:
            values = self.tree_reservas.item(item, "values")
            usuario = values[0]
            funcion_titulo = values[1]
            confirm = messagebox.askokcancel("Confirmar cancelación",
                                              f"¿Está seguro de cancelar la reserva del usuario '{usuario}' para la función '{funcion_titulo}'?")
            if confirm:
                if funcion_titulo in Reservar.list_reserva:
                    del Reservar.list_reserva[funcion_titulo]
                    messagebox.showinfo("Cancelación exitosa", "Reserva cancelada correctamente")
                else:
                    messagebox.showerror("Error", "Reserva no encontrada")
        self.actualizar_lista_reservas()
    
    def setup_promociones_tab(self):
        frame_reg = ttk.LabelFrame(self.tab_promociones, text="Registrar Promoción")
        frame_reg.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(frame_reg, text="Descuento (%):").grid(row=0, column=0, padx=5, pady=5)
        self.promo_descuento_entry = ttk.Entry(frame_reg)
        self.promo_descuento_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_reg, text="Condición:").grid(row=1, column=0, padx=5, pady=5)
        self.promo_condicion_entry = ttk.Entry(frame_reg)
        self.promo_condicion_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_reg, text="Producto:").grid(row=2, column=0, padx=5, pady=5)
        self.promo_producto_entry = ttk.Entry(frame_reg)
        self.promo_producto_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(frame_reg, text="Registrar Promoción", command=self.registrar_promocion).grid(row=3, column=0, columnspan=2, pady=10)
        
        frame_lista = ttk.LabelFrame(self.tab_promociones, text="Promociones Registradas")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ("Descuento", "Condición", "Producto")
        self.tree_promociones = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_promociones.heading(col, text=col)
            self.tree_promociones.column(col, width=150)
        self.tree_promociones.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista", command=self.actualizar_lista_promociones).pack(pady=5)
    
    # Registro y actualización de mis datos
    
    def registrar_persona(self):
        nombre = self.nombre_entry.get()
        contacto = self.contacto_entry.get()
        tipo = self.tipo_combobox.get()
        rol = self.rol_entry.get()
        
        if not nombre or not contacto or not tipo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if tipo == "Empleado" and not rol:
            messagebox.showerror("Error", "El rol es obligatorio para empleados")
            return
        
        if tipo == "Usuario":
            usuario = Usuario(nombre, contacto, tipo)
            usuario.registrar()
            Usuario.guardar_usuario()  
        else:
            empleado = Empleado(nombre, contacto, tipo, rol)
            empleado.registrar()
            Empleado.guardar_empleado()
        
        messagebox.showinfo("Éxito", f"{tipo} registrado correctamente")
        self.actualizar_lista_usuarios()
        self.limpiar_campos()
    
    def registrar_pelicula(self):
        titulo = self.titulo_entry.get()
        genero = self.genero_entry.get()
        duracion = self.duracion_entry.get()
        clasificacion = self.clasificacion_entry.get()
        
        if not titulo or not genero or not duracion or not clasificacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        pelicula = Pelicula(titulo, genero, duracion, clasificacion)
        pelicula.registrar_pelicula()
        Pelicula.guardar_pelicula()
        
        messagebox.showinfo("Éxito", "Película registrada correctamente")
        self.actualizar_lista_peliculas()
        self.limpiar_campos_pelicula()
    
    def registrar_funcion(self):
        hora = self.hora_entry.get()
        sala_id = self.sala_entry.get()
        titulo_peli = self.peli_entry.get()
        
        if not hora or not sala_id or not titulo_peli:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        sala = Sala(60, sala_id, "General")
        pelicula = None
        for p in Pelicula.list_peliculas:
            if p.titulo.lower() == titulo_peli.lower():
                pelicula = p
                break
        if pelicula is None:
            pelicula = Pelicula(titulo_peli, "Desconocido", "Desconocido", "Desconocido")
            pelicula.registrar_pelicula()
        
        funcion = Funcion(hora, sala, pelicula)
        funcion.registrar_funcion()
        messagebox.showinfo("Función registrada", "La función ha sido registrada con éxito")
        self.actualizar_lista_funciones()
        self.hora_entry.delete(0, tk.END)
        self.sala_entry.delete(0, tk.END)
        self.peli_entry.delete(0, tk.END)
    
    def registrar_reserva(self):
        usuario_nombre = self.reserva_usuario_entry.get()
        funcion_peli = self.reserva_funcion_entry.get()
        asientos_str = self.reserva_asientos_entry.get()
        
        if not usuario_nombre or not funcion_peli or not asientos_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        usuario = None
        for per in Persona.pers:
            if per.nombre.lower() == usuario_nombre.lower():
                usuario = per
                break
        if usuario is None:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        funcion = None
        for func in Funcion.list_funciones:
            if func.pelicula.titulo.lower() == funcion_peli.lower():
                funcion = func
                break
        if funcion is None:
            messagebox.showerror("Error", "Función no encontrada")
            return
        
        asientos = [a.strip() for a in asientos_str.split(",") if a.strip()]
        reserva = Reservar(usuario, funcion, asientos)
        reserva.registrar_reserva()
        messagebox.showinfo("Reserva registrada", "Reserva registrada correctamente")
        self.actualizar_lista_reservas()
        self.reserva_usuario_entry.delete(0, tk.END)
        self.reserva_funcion_entry.delete(0, tk.END)
        self.reserva_asientos_entry.delete(0, tk.END)
    
    def registrar_promocion(self):
        descuento = self.promo_descuento_entry.get()
        condicion = self.promo_condicion_entry.get()
        producto = self.promo_producto_entry.get()
        
        if not descuento or not condicion or not producto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            descuento_val = float(descuento)
        except ValueError:
            messagebox.showerror("Error", "El descuento debe ser un valor numérico")
            return
        
        promo = Promocion(descuento_val, condicion, producto)
        promo.registrar_promocion()
        messagebox.showinfo("Promoción registrada", "Promoción registrada correctamente")
        self.actualizar_lista_promociones()
        self.promo_descuento_entry.delete(0, tk.END)
        self.promo_condicion_entry.delete(0, tk.END)
        self.promo_producto_entry.delete(0, tk.END)
    
    
    #Actualizar mis listas en las pestaña
    
    def actualizar_lista_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        for persona in Persona.pers:
            self.tree_usuarios.insert("", "end", values=(
                persona.nombre, 
                persona.contacto, 
                persona.tipo,
                getattr(persona, 'rol', 'N/A')
            ))
    
    def actualizar_lista_peliculas(self):
        for item in self.tree_peliculas.get_children():
            self.tree_peliculas.delete(item)
        for pelicula in Pelicula.list_peliculas:
            self.tree_peliculas.insert("", "end", values=(
                pelicula.titulo, 
                pelicula.genero, 
                pelicula.duracion,
                pelicula.clasificacion
            ))
    
    def actualizar_lista_funciones(self):
        for item in self.tree_funciones.get_children():
            self.tree_funciones.delete(item)
        for func in Funcion.list_funciones:
            self.tree_funciones.insert("", "end", values=(
                func.hora, 
                func.sala.identificador, 
                func.pelicula.titulo,
                str(func.list_boletos)
            ))
    
    def actualizar_lista_reservas(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        for func_title, data in Reservar.list_reserva.items():
            self.tree_reservas.insert("", "end", values=(
                data["usuario"],
                func_title,
                str(data["asiento"])
            ))
    
    def actualizar_lista_promociones(self):
        for item in self.tree_promociones.get_children():
            self.tree_promociones.delete(item)
        for promo in Promocion.list_descuentos:
            self.tree_promociones.insert("", "end", values=(
                promo.descuento,
                promo.condicion,
                promo.producto
            ))
    
    # Limpia mis campos de entrada

    def limpiar_campos(self):
        self.nombre_entry.delete(0, 'end')
        self.contacto_entry.delete(0, 'end')
        self.tipo_combobox.set('')
        self.rol_entry.delete(0, 'end')
    
    def limpiar_campos_pelicula(self):
        self.titulo_entry.delete(0, 'end')
        self.genero_entry.delete(0, 'end')
        self.duracion_entry.delete(0, 'end')
        self.clasificacion_entry.delete(0, 'end')

# Inicio
def main():
    root = tk.Tk()
    app = CineApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
