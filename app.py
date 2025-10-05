from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from conexion.conexion import get_db_connection, cerrar_conexion
from datetime import datetime
from modelo import Usuario, Producto, Categoria, Venta, Cliente

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------ CONFIGURAR LOGIN ------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.obtener_por_id(id_usuario)


# ------------------ RUTA PRINCIPAL ------------------
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('panel.html')
    return render_template('index.html')  # Página de bienvenida para no autenticados

# ------------------ RUTA PANEL ------------------
@app.route('/panel')
@login_required
def panel_usuario():
    return render_template('panel.html')

# ------------------ RUTA Usuario------------------
@property
def id(self):
    return self.id_usuario
# ------------------ RUTA NUEVA V------------------
@app.route('/nueva_venta')
@login_required
def nueva_venta():
    productos = Producto.obtener_todos()  # devuelve lista de productos
    clientes = Cliente.obtener_todos()    # devuelve lista de clientes
    return render_template("nueva_venta.html", productos=productos, clientes=clientes)

# ------------------ PRODUCTOS (CRUD) ------------------
@app.route('/productos')
@login_required
def ver_productos():
    productos = Producto.obtener_todos()
    return render_template('producto.html', productos=productos)

    # Crear producto
@app.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == "POST":
        nombre_producto = request.form['nombre_producto']
        id_categoria = request.form['id_categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        Producto.crear(nombre_producto, id_categoria, precio, stock)
        flash("Producto creado correctamente ✅", "success")
        return redirect(url_for('ver_productos'))
    return render_template('producto.html', accion="Crear")

# Editar producto
@app.route('/producto/<int:id_productos>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(id_productos):
    producto = Producto.obtener_por_id(id_productos)
    if not producto:
        flash("Producto no encontrado ❌", "danger")
        return redirect(url_for('ver_productos'))
    if request.method == "POST":
        nombre_producto = request.form['nombre_producto']
        id_categoria = request.form['id_categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        Producto.actualizar(id_productos, nombre_producto, id_categoria, precio, stock)
        flash("Producto actualizado correctamente ✅", "success")
        return redirect(url_for('ver_productos'))
    return render_template('producto.html', producto=producto, accion="Editar")

# Eliminar producto
@app.route('/producto/<int:id_productos>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(id_productos):
    Producto.eliminar(id_productos)
    flash("Producto eliminado ✅", "success")
    return redirect(url_for('ver_productos'))


# ------------------ VENTAS ------------------
@app.route('/ventas')
@login_required
def ver_ventas():
    ventas = Venta.obtener_todas()
    return render_template('ventas.html', ventas=ventas)


@app.route('/crear_venta', methods=['GET', 'POST'])
@login_required
def crear_venta():
    if request.method == 'POST':
        try:
            id_producto = request.form['id_productos']
            id_cliente = request.form['id_cliente']
            cantidad = int(request.form['cantidad'])
            fecha = datetime.now().strftime("%Y-%m-%d")
            id_usuario = current_user.id_usuario

            # Registrar la venta
            Venta.registrar(id_usuario, id_cliente, id_producto, cantidad, fecha)
            flash("Venta registrada correctamente ✅", "success")

        except KeyError as e:
            flash(f"Falta el campo {e.args[0]} en el formulario ❌", "danger")
        except Exception as e:
            flash(f"Error al registrar la venta: {e}", "danger")

        return redirect(url_for('crear_venta'))

    productos = Producto.obtener_todos()
    clientes = Cliente.obtener_todos()
    return render_template("nueva_venta.html", productos=productos, clientes=clientes)

@app.route('/ventas')
def mostrar_ventas():
    ventas = Venta.obtener_todas()  # Asegúrate que trae los últimos registros
    return render_template('ventas.html', ventas=ventas)

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        usuarios = Usuario.obtener_todos()

        for u in usuarios:
            if u.email == email and u.password == password:
                login_user(u)
                flash("¡Sesión iniciada correctamente! 🎉", "success")
                return redirect(url_for('index'))
                
        
        flash("Credenciales incorrectas ❌", "danger")
        return redirect(url_for('login'))

    return render_template("logini.html")

# ------------------ REGISTRO ------------------
@app.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == "POST":
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash("❌ Las contraseñas no coinciden", "danger")
            return redirect(url_for('registrar_usuario'))

        if Usuario.obtener_por_email(email):
            flash("⚠️ Este correo ya está registrado", "warning")
            return redirect(url_for('registrar_usuario'))

        Usuario.crear(nombre, email, password)
        flash("✅ Usuario registrado. Ahora inicia sesión.", "success")
        return redirect(url_for('login'))

    return render_template("registro.html")

# ------------------ Clientes ------------------
@app.route('/crear_cliente', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']

        # Guardar cliente en BD
        Cliente.crear(nombre, direccion)

        # Redirige a ventas después de registrar
        return redirect(url_for('crear_venta'))

    return render_template('crear_cliente.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 Sesión cerrada", "info")
    return redirect(url_for("index"))


# ------------------ MAIN ------------------
if __name__ == '__main__':
    app.run(debug=True)
