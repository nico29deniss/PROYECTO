# models/model_login.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from conexion.conexion import get_db_connection, cerrar_conexion
from mysql.connector import Error
 


# ------------------ USUARIO ------------------

class Usuario(UserMixin):
    def __init__(self, id_usuario, Nombre, email, password, session_token=None):
        self.id_usuario = id_usuario
        self.Nombre = Nombre
        self.email = email
        self.password = password
        self.session_token = session_token

    def get_id(self):
        return str(self.id_usuario)

    @staticmethod
    def obtener_todos():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        cursor.close()
        cerrar_conexion(conn)
        return [
            Usuario(r["id_usuario"], r["Nombre"], r["email"], r["password"], r.get("session_token"))
            for r in rows
        ]

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (id_usuario,))
        row = cursor.fetchone()
        cursor.close()
        cerrar_conexion(conn)
        if row:
            return Usuario(
                row["id_usuario"], row["Nombre"], row["email"], row["password"], row.get("session_token")
            )
        return None

    @staticmethod
    def obtener_por_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        row = cursor.fetchone()
        cursor.close()
        cerrar_conexion(conn)
        if row:
            return Usuario(
                row["id_usuario"], row["Nombre"], row["email"], row["password"], row.get("session_token")
            )
        return None

    @staticmethod
    def crear(Nombre, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (Nombre, email, password) VALUES (%s, %s, %s)",
            (Nombre, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        cerrar_conexion(conn)

    @staticmethod
    def actualizar_token(id_usuario, token):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET session_token=%s WHERE id_usuario=%s",
            (token, id_usuario)
        )
        conn.commit()
        cursor.close()
        cerrar_conexion(conn)

# ------------------ PRODUCTO ------------------
class Producto:
    def __init__(self, id_productos, nombre_producto, id_categoria, precio, stock):
        self.id_productos = id_productos
        self.nombre_producto = nombre_producto
        self.id_categoria = id_categoria
        self.precio = precio
        self.stock = stock

    @staticmethod
    def obtener_todos():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        cursor.close()
        cerrar_conexion(conn)
        return [Producto(r["id_productos"], r["nombre_producto"], r["id_categoria"], r["precio"], r["stock"]) for r in rows]

    @staticmethod
    def obtener_por_id(id_producto):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id_productos=%s", (id_producto,))
        row = cursor.fetchone()
        cursor.close()
        cerrar_conexion(conn)
        if row:
            return Producto(row["id_productos"], row["nombre_producto"], row["id_categoria"], row["precio"], row["stock"])
        return None

    @staticmethod
    def crear(nombre_producto, id_categoria, precio, stock):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre_producto, id_categoria, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre_producto, id_categoria, precio, stock)
        )
        conn.commit()
        cursor.close()
        cerrar_conexion(conn)

    @staticmethod
    def actualizar(id_productos, nombre_producto, id_categoria, precio, stock):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre_producto=%s, id_categoria=%s, precio=%s, stock=%s WHERE id_productos=%s",
            (nombre_producto, id_categoria, precio, stock, id_productos)
        )
        conn.commit()
        cursor.close()
        cerrar_conexion(conn)

    @staticmethod
    def eliminar(id_productos):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_productos=%s", (id_productos,))
        conn.commit()
        cursor.close()
        cerrar_conexion(conn)

# ------------------ CLIENTE ------------------
class Cliente:
    def __init__(self, id_cliente, nombre, direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion

    @staticmethod
    def obtener_todos():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        cursor.close()
        cerrar_conexion(conn)
        return [Cliente(r["id_cliente"], r["nombre"], r["direccion"]) for r in rows]

    @staticmethod
    def crear(nombre, direccion):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO clientes (nombre, direccion) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, direccion))
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        cerrar_conexion(conn)
        return nuevo_id

# ------------------ CATEGORIA ------------------
class Categoria:
    def __init__(self, id_categoria, nombre_categoria):
        self.id_categoria = id_categoria
        self.nombre_categoria = nombre_categoria

    @staticmethod
    def obtener_todas():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias")
        rows = cursor.fetchall()
        cursor.close()
        cerrar_conexion(conn)
        return [Categoria(r["id_categoria"], r["nombre_categoria"]) for r in rows]

# ------------------ VENTA ------------------
class Venta:
    def __init__(self, id_ventas, id_usuario, id_cliente, id_productos, cantidad, fecha, precio):
        self.id_ventas = id_ventas
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente
        self.id_productos = id_productos
        self.cantidad = cantidad
        self.fecha = fecha
        self.precio = precio

    @staticmethod
    def registrar(id_usuario, id_cliente, id_productos, cantidad, fecha):
        producto = Producto.obtener_por_id(id_productos)
        if not producto:
            raise ValueError("Producto no encontrado")
        precio_total = producto.precio * cantidad

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ventas (id_usuario, id_cliente, id_productos, cantidad, precio, fecha) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_usuario, id_cliente, id_productos, cantidad, precio_total, fecha)
        )
        conn.commit()
        cursor.close()
        cerrar_conexion(conn)

    @staticmethod
    def obtener_todas():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.id_ventas, v.id_usuario, v.id_cliente, v.id_productos, p.nombre_producto, v.cantidad, v.fecha, v.precio
            FROM ventas v
            JOIN productos p ON v.id_productos = p.id_productos
            ORDER BY v.fecha DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        cerrar_conexion(conn)
        return rows
