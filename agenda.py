import streamlit as st

class Contacto:
    def __init__(self, nombre, telefono, imagen=None):
        self.nombre = nombre
        self.telefono = telefono
        self.imagen = imagen

    def __str__(self):
        return f"{self.nombre}: {self.telefono}"

class HashMap:
    def __init__(self, tamaño=10):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    def funcion_hash(self, clave):
        return sum(ord(c) for c in clave) % self.tamaño

    def agregar_contacto(self, nombre, telefono, imagen=None):
        indice = self.funcion_hash(nombre)
        for contacto in self.tabla[indice]:
            if contacto.nombre == nombre:
                contacto.telefono = telefono
                if imagen:
                    contacto.imagen = imagen
                return f"✏️ Contacto actualizado: {nombre}"
        self.tabla[indice].append(Contacto(nombre, telefono, imagen))
        return f"✅ Contacto agregado: {nombre}"

    def buscar_contacto(self, nombre):
        indice = self.funcion_hash(nombre)
        for contacto in self.tabla[indice]:
            if contacto.nombre == nombre:
                return contacto
        return None

    def eliminar_contacto(self, nombre):
        indice = self.funcion_hash(nombre)
        for i, contacto in enumerate(self.tabla[indice]):
            if contacto.nombre == nombre:
                del self.tabla[indice][i]
                return f"🗑️ Contacto eliminado: {nombre}"
        return f"⚠️ Contacto no encontrado: {nombre}"

    def obtener_todos(self):
        todos = []
        for i, lista in enumerate(self.tabla):
            for contacto in lista:
                todos.append((i, contacto))
        return todos

CODIGOS_VALIDOS = {
    '+51': 'Perú',
    '+52': 'México',
    '+54': 'Argentina',
    '+55': 'Brasil',
    '+56': 'Chile',
    '+57': 'Colombia',
    '+58': 'Venezuela',
    '+591': 'Bolivia',
    '+593': 'Ecuador',
    '+595': 'Paraguay',
    '+598': 'Uruguay'
}

def es_telefono_valido(telefono: str) -> tuple[bool, str]:
    if telefono.isdigit() and telefono.startswith("9") and len(telefono) == 9:
        return True, "Teléfono nacional válido (Perú)"
    if telefono.startswith("+") and len(telefono) >= 10:
        for codigo in CODIGOS_VALIDOS:
            if telefono.startswith(codigo):
                return True, f"Teléfono internacional válido ({CODIGOS_VALIDOS[codigo]})"
        return False, "⚠️ Código de país no permitido"
    return False, "⚠️ Número inválido: debe ser nacional (9 dígitos desde 9) o internacional válido (+código país)"


st.set_page_config(page_title="Agenda de Contactos", layout="centered", page_icon="📞")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f7fa;
    }

    .title {
        font-size: 42px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    .contact-card {
        background-color: #f0f6ff;
        border-left: 6px solid #1f77b4;
        padding: 12px 18px;
        margin-bottom: 10px;
        border-radius: 6px;
    }

    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 20px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #155b8d;
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📒 Agenda de Contactos </div>', unsafe_allow_html=True)

if "agenda" not in st.session_state:
    st.session_state.agenda = HashMap()

tab1, tab2, tab3, tab4 = st.tabs(["➕ Agregar", "🔍 Buscar", "🗑️ Eliminar", "📋 Ver Todo"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Agrega o actualiza un contacto")

    nombre = st.text_input("👤 Nombre del contacto")
    telefono = st.text_input("📱 Teléfono (ej: 987654321 o +51xxxxxxxxx)")
    imagen_subida = st.file_uploader("🖼️ Sube una imagen (opcional)", type=["png", "jpg", "jpeg"])

    if st.button("Guardar contacto"):
        if not nombre or not telefono:
            st.error("❗Por favor completa todos los campos.")
        else:
            valido, mensaje = es_telefono_valido(telefono)
            if not valido:
                st.error(mensaje)
            else:
                imagen_bytes = imagen_subida.read() if imagen_subida else None
                resultado = st.session_state.agenda.agregar_contacto(nombre, telefono, imagen_bytes)
                st.success(f"{resultado}\n✅ {mensaje}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Buscar un contacto")
    nombre_buscar = st.text_input("🔎 Nombre a buscar", key="buscar")
    if st.button("Buscar"):
        c = st.session_state.agenda.buscar_contacto(nombre_buscar)
        if c:
            st.success(f"👤 {c.nombre} → 📱 {c.telefono}")
            if c.imagen:
                st.image(c.imagen, width=150, caption="📸 Imagen del contacto")
        else:
            st.warning("No se encontró ese contacto.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🗑️ Eliminar un contacto")
    nombre_eliminar = st.text_input("✂️ Nombre a eliminar", key="eliminar")
    if st.button("Eliminar"):
        resultado = st.session_state.agenda.eliminar_contacto(nombre_eliminar)
        st.info(resultado)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Lista completa de contactos")
    todos = st.session_state.agenda.obtener_todos()

    if todos:
        for idx, c in todos:
            st.markdown(f'<div class="contact-card">', unsafe_allow_html=True)
            cols = st.columns([1, 4])
            if c.imagen:
                cols[0].image(c.imagen, width=64)
            else:
                cols[0].image("https://cdn-icons-png.flaticon.com/512/747/747376.png", width=64)
            cols[1].markdown(f"""
            <b>Índice:</b> {idx}  
            <b>👤 Nombre:</b> {c.nombre}  
            <b>📱 Teléfono:</b> {c.telefono}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Aún no hay contactos registrados.")
    st.markdown('</div>', unsafe_allow_html=True)

