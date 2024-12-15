import tkinter as tk
from tkinter import messagebox
import mysql.connector

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Conexión establecida a la base de datos")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            messagebox.showerror("Error de conexión", f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

class ReservaManager:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def insertar_reserva(self, cliente, telefono, fecha, estado):
        if not cliente or not telefono or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.db_connector.connect()
            self.db_connector.cursor.callproc("insertar_reserva", [cliente, telefono, fecha, estado])
            self.db_connector.connection.commit()
            messagebox.showinfo("Éxito", "Reserva insertada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar reserva: {e}")
        finally:
            self.db_connector.disconnect()

    def buscar_reserva(self, id_reserva):
        try:
            self.db_connector.connect()
            self.db_connector.cursor.callproc("buscar_reserva", [id_reserva])
            resultados = list(self.db_connector.cursor.stored_results())[0]
            return resultados
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar reserva: {e}")
            return []
        finally:
            self.db_connector.disconnect()

    def actualizar_reserva(self, id_reserva, cliente, telefono, estado):
        if not cliente or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.db_connector.connect()
            self.db_connector.cursor.callproc("actualizar_reserva", [id_reserva, cliente, telefono, estado])
            self.db_connector.connection.commit()
            messagebox.showinfo("Éxito", "Reserva actualizada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar reserva: {e}")
        finally:
            self.db_connector.disconnect()

    def eliminar_reserva(self, id_reserva):
        try:
            self.db_connector.connect()
            self.db_connector.cursor.callproc("eliminar_reserva", [id_reserva])
            self.db_connector.connection.commit()
            messagebox.showinfo("Éxito", "Reserva eliminada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar reserva: {e}")
        finally:
            self.db_connector.disconnect()

class ReservaApp:
    def __init__(self, root, reserva_manager):
        self.root = root
        self.reserva_manager = reserva_manager
        self.create_widgets()

    def create_widgets(self):

        tk.Label(self.root, text="ID Reserva").grid(row=0, column=0)
        self.entry_id_reserva = tk.Entry(self.root)
        self.entry_id_reserva.grid(row=0, column=1)

        tk.Label(self.root, text="Cliente").grid(row=1, column=0)
        self.entry_cliente = tk.Entry(self.root)
        self.entry_cliente.grid(row=1, column=1)

        tk.Label(self.root, text="Teléfono").grid(row=2, column=0)
        self.entry_telefono = tk.Entry(self.root)
        self.entry_telefono.grid(row=2, column=1)

        tk.Label(self.root, text="Fecha").grid(row=3, column=0)
        self.entry_fecha = tk.Entry(self.root)
        self.entry_fecha.grid(row=3, column=1)

        tk.Label(self.root, text="Estado").grid(row=4, column=0)
        self.combo_estado = tk.StringVar(self.root)
        self.combo_estado.set("pendiente")  # Valor por defecto
        estado_menu = tk.OptionMenu(self.root, self.combo_estado, "pendiente", "confirmada", "cancelada")
        estado_menu.grid(row=4, column=1)

        tk.Button(self.root, text="Insertar Reserva", command=self.insertar_reserva).grid(row=5, column=0)
        tk.Button(self.root, text="Actualizar Reserva", command=self.actualizar_reserva).grid(row=6, column=0)
        tk.Button(self.root, text="Eliminar Reserva", command=self.eliminar_reserva).grid(row=6, column=1)

    def insertar_reserva(self):
        cliente = self.entry_cliente.get()
        telefono = self.entry_telefono.get()
        fecha = self.entry_fecha.get()
        estado = self.combo_estado.get()
        self.reserva_manager.insertar_reserva(cliente, telefono, fecha, estado)
        self.limpiar_campos()

    def actualizar_reserva(self):
        id_reserva = self.entry_id_reserva.get()
        cliente = self.entry_cliente.get()
        telefono = self.entry_telefono.get()
        estado = self.combo_estado.get()
        self.reserva_manager.actualizar_reserva(id_reserva, cliente, telefono, estado)
        self.limpiar_campos()

    def eliminar_reserva(self):
        id_reserva = self.entry_id_reserva.get()
        self.reserva_manager.eliminar_reserva(id_reserva)
        self.limpiar_campos()

    def limpiar_campos(self):
        self.entry_id_reserva.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.combo_estado.set("")

def main():
    db_connector = DatabaseConnector(host="localhost", user="root", password="", database="sistema_reservas")
    reserva_manager = ReservaManager(db_connector)

    root = tk.Tk()
    root.title("Sistema de Reservas")

    app = ReservaApp(root, reserva_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
