import base64
import hashlib
import os
from datetime import date, time
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

st.set_page_config(
    page_title="Pedicure Beauty",
    page_icon="✿",
    layout="wide",
)

WHATSAPP_URL = "https://wa.me/51918839586"
BASE_DIR = Path(__file__).parent
IMAGEN_INICIO = BASE_DIR / "fondo_inicio.png"


def resolver_imagen_secciones(base_dir: Path) -> Path:
    candidatas = [
        base_dir / "fondo rosas-rosadas.jpg",
        base_dir / "fondo rosas-rosadas.jpeg",
        base_dir / "fondo rosas-rosadas.png",
        base_dir / "fondo rosas-rosadas",
    ]
    for ruta in candidatas:
        if ruta.exists() and ruta.is_file():
            return ruta
    return candidatas[0]


IMAGEN_SECCIONES = resolver_imagen_secciones(BASE_DIR)

SERVICIOS = [
    {
        "icono": "✿",
        "nombre": "Pedicure clásico",
        "descripcion": "Limpieza, limado, cuidado de cutículas y esmalte tradicional.",
        "precio": "S/ 35",
    },
    {
        "icono": "✧",
        "nombre": "Pedicure spa",
        "descripcion": "Pedicure clásico, exfoliación, mascarilla e hidratación.",
        "precio": "S/ 55",
    },
    {
        "icono": "♡",
        "nombre": "Pedicure con gel",
        "descripcion": "Cuidado de uñas con acabado en gel de larga duración.",
        "precio": "S/ 65",
    },
    {
        "icono": "❀",
        "nombre": "Retiro de esmalte",
        "descripcion": "Retiro cuidadoso del producto y limpieza de la uña.",
        "precio": "S/ 15",
    },
    {
        "icono": "✦",
        "nombre": "Decoración sencilla",
        "descripcion": "Detalles decorativos para complementar tu pedicure.",
        "precio": "Desde S/ 10",
    },
    {
        "icono": "♡",
        "nombre": "Hidratación profunda",
        "descripcion": "Tratamiento hidratante para consentir tus pies.",
        "precio": "S/ 25",
    },
]


def get_image_base64(image_path: Path) -> str:
    if not image_path.exists() or not image_path.is_file():
        return ""
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")


def get_connection():
    db = st.secrets["postgres"]
    return psycopg2.connect(
        host=db["host"],
        port=int(db["port"]),
        dbname=db["dbname"],
        user=db["user"],
        password=db["password"],
        sslmode="require",
        cursor_factory=RealDictCursor,
    )


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return f"{salt.hex()}:{digest.hex()}"


if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"
if "servicio_seleccionado" not in st.session_state:
    st.session_state.servicio_seleccionado = SERVICIOS[0]["nombre"]

bg_inicio_b64 = get_image_base64(IMAGEN_INICIO)
bg_secciones_b64 = get_image_base64(IMAGEN_SECCIONES)
pagina = st.session_state.pagina

if pagina == "Inicio":
    bg_layer = (
        f'linear-gradient(rgba(255, 228, 238, 0.72), rgba(252, 209, 226, 0.78)), '
        f'url("data:image/png;base64,{bg_inicio_b64}") center / cover no-repeat fixed'
        if bg_inicio_b64
        else "linear-gradient(180deg, #ffeef4 0%, #ffd6e6 100%)"
    )
else:
    bg_layer = (
        f'linear-gradient(rgba(255, 245, 249, 0.62), rgba(255, 235, 243, 0.68)), '
        f'url("data:image/jpeg;base64,{bg_secciones_b64}") center / cover no-repeat fixed'
        if bg_secciones_b64
        else "linear-gradient(180deg, #fff5f9 0%, #ffe3ee 100%)"
    )

fondo_pagina_css = f"""
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{
    background: {bg_layer} !important;
}}
[data-testid="stHeader"] {{
    background: rgba(255, 235, 243, 0.75) !important;
}}
"""

st.markdown(
    f"""
    <style>
    {fondo_pagina_css}
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {{
        background: linear-gradient(180deg, #ffe4ee 0%, #fbd0e0 100%) !important;
        border-right: 1px solid #f4b6ce !important;
    }}
    section[data-testid="stSidebar"] a[data-testid="stLinkButton"] {{
        background-color: #fff5f8 !important;
        border: 1px solid #e5739f !important;
        color: #880e4f !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] a[data-testid="stLinkButton"]:hover {{
        background-color: #fce4ec !important;
        border-color: #c2185b !important;
    }}
    .hero-box {{
        background:
            linear-gradient(135deg, rgba(255, 240, 245, 0.72) 0%, rgba(255, 214, 229, 0.78) 100%)
            {f', url("data:image/png;base64,{bg_inicio_b64}") center / cover no-repeat' if bg_inicio_b64 else ''};
        padding: 2.4rem;
        border-radius: 18px;
        border: 1px solid #f48fb1;
        box-shadow: 0 8px 24px rgba(173, 20, 87, 0.08);
        margin-bottom: 1.5rem;
    }}
    .service-card {{
        background-color: rgba(255, 255, 255, 0.94);
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid #f3d1dc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
        min-height: 210px;
    }}
    .price-tag {{
        font-size: 1.15rem;
        font-weight: 700;
        color: #ad1457;
    }}
    .gallery-tile {{
        border-radius: 14px;
        padding: 2.5rem 1rem;
        text-align: center;
        font-weight: 600;
        color: #4a1525;
        margin-bottom: 1rem;
        border: 1px solid rgba(244, 143, 177, 0.55);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    [data-testid="stForm"] {{
        background-color: rgba(255, 255, 255, 0.92);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #f3d1dc;
        box-shadow: 0 4px 14px rgba(173, 20, 87, 0.05);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Pedicure Beauty")
    st.caption("Cuidado • Belleza • Bienestar")
    opciones = ["Inicio", "Catálogo", "Galería", "Reservas", "Registro", "Contacto"]
    indice_actual = opciones.index(st.session_state.pagina)
    seleccion = st.radio("Navegación", opciones, index=indice_actual)
    if seleccion != st.session_state.pagina:
        st.session_state.pagina = seleccion
        st.rerun()

    st.divider()
    st.link_button("Escribir por WhatsApp", WHATSAPP_URL, use_container_width=True)

if pagina == "Inicio":
    st.markdown(
        """
        <div class="hero-box">
            <p style="color:#ad1457; font-weight:600; margin-bottom:0.3rem;">CUIDADO • BELLEZA • BIENESTAR</p>
            <h1 style="margin-top:0;">Un momento para ti, de pies a cabeza.</h1>
            <p>Descubre nuestros servicios de pedicure y regálate un momento de cuidado y relajación.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_cta1, col_cta2, _ = st.columns([1, 1, 3])
    with col_cta1:
        if st.button("Ver catálogo", type="primary", use_container_width=True):
            st.session_state.pagina = "Catálogo"
            st.rerun()
    with col_cta2:
        if st.button("Reservar cita", use_container_width=True):
            st.session_state.pagina = "Reservas"
            st.rerun()

    st.subheader("Nuestros favoritos")
    cols = st.columns(3)
    for idx, srv in enumerate(SERVICIOS[:3]):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="service-card">
                    <div style="font-size:1.5rem;">{srv['icono']}</div>
                    <h4>{srv['nombre']}</h4>
                    <p>{srv['descripcion']}</p>
                    <p class="price-tag">{srv['precio']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

elif pagina == "Catálogo":
    st.title("Catálogo de pedicure")
    st.caption("Precios referenciales en soles. Confirma el costo final al reservar.")

    cols = st.columns(3)
    for idx, srv in enumerate(SERVICIOS):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="service-card">
                    <div style="font-size:1.5rem;">{srv['icono']}</div>
                    <h4>{srv['nombre']}</h4>
                    <p>{srv['descripcion']}</p>
                    <p class="price-tag">{srv['precio']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Reservar {srv['nombre']}", key=f"btn_{idx}", use_container_width=True):
                st.session_state.servicio_seleccionado = srv["nombre"]
                st.session_state.pagina = "Reservas"
                st.rerun()

elif pagina == "Galería":
    st.title("Galería")
    st.caption("Ideas de colores y estilos para tu próxima cita.")

    estilos_galeria = [
        ("Colores suaves", "rgba(252, 228, 236, 0.92)"),
        ("Detalles delicados", "rgba(248, 187, 208, 0.92)"),
        ("Un toque de brillo", "rgba(243, 229, 245, 0.92)"),
        ("Estilo natural", "rgba(255, 243, 224, 0.92)"),
        ("Momentos spa", "rgba(224, 242, 241, 0.92)"),
        ("Tu estilo, tus uñas", "rgba(255, 235, 238, 0.92)"),
    ]
    cols = st.columns(3)
    for idx, (titulo, color) in enumerate(estilos_galeria):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="gallery-tile" style="background:{color};">{titulo}</div>',
                unsafe_allow_html=True,
            )
    st.info("Puedes reemplazar estos bloques por fotos reales usando st.image('ruta/foto.jpg').")

elif pagina == "Reservas":
    st.title("Reserva una cita")
    st.caption("Completa tus datos y nos pondremos en contacto para confirmar.")

    nombres_servicios = [s["nombre"] for s in SERVICIOS]
    idx_servicio = (
        nombres_servicios.index(st.session_state.servicio_seleccionado)
        if st.session_state.servicio_seleccionado in nombres_servicios
        else 0
    )

    with st.form("form_reservas", clear_on_submit=True):
        nombre = st.text_input("Nombre completo *", max_chars=100)
        celular = st.text_input("Celular *", max_chars=20)
        correo = st.text_input("Correo electrónico *", max_chars=150)
        servicio = st.selectbox("Servicio *", nombres_servicios, index=idx_servicio)
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha *", min_value=date.today())
        with col2:
            hora = st.time_input("Hora *", value=time(10, 0))
        mensaje = st.text_area("Mensaje (opcional)", max_chars=1000)

        enviado = st.form_submit_button("Enviar solicitud", type="primary")
        if enviado:
            if not nombre.strip() or not celular.strip() or not correo.strip():
                st.error("Por favor completa los campos obligatorios.")
            else:
                try:
                    with get_connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                """
                                INSERT INTO reservas (nombre, celular, correo, servicio, fecha, hora, mensaje)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    nombre.strip(),
                                    celular.strip(),
                                    correo.strip().lower(),
                                    servicio,
                                    fecha.isoformat(),
                                    hora.strftime("%H:%M:%S"),
                                    mensaje.strip(),
                                ),
                            )
                        conn.commit()
                    st.success("¡Solicitud enviada! Te contactaremos pronto para confirmar tu cita.")
                except Exception as e:
                    st.error(f"No se pudo guardar la reserva: {e}")

elif pagina == "Registro":
    st.title("Registro de clientes")
    st.caption("Crea tu cuenta para que podamos contactarte y gestionar tus citas.")

    with st.form("form_registro", clear_on_submit=True):
        nombre = st.text_input("Nombre *", max_chars=80)
        apellido = st.text_input("Apellido *", max_chars=80)
        celular = st.text_input("Celular *", max_chars=20)
        correo = st.text_input("Correo electrónico *", max_chars=150)
        password = st.text_input("Contraseña (mínimo 8 caracteres) *", type="password", max_chars=72)

        registrado = st.form_submit_button("Registrarme", type="primary")
        if registrado:
            if not all([nombre.strip(), apellido.strip(), celular.strip(), correo.strip(), password]):
                st.error("Todos los campos son obligatorios.")
            elif len(password) < 8:
                st.error("La contraseña debe tener al menos 8 caracteres.")
            else:
                try:
                    with get_connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                """
                                INSERT INTO clientes (nombre, apellido, celular, correo, password_hash)
                                VALUES (%s, %s, %s, %s, %s)
                                """,
                                (
                                    nombre.strip(),
                                    apellido.strip(),
                                    celular.strip(),
                                    correo.strip().lower(),
                                    hash_password(password),
                                ),
                            )
                        conn.commit()
                    st.success("¡Cuenta creada con éxito!")
                except psycopg2.errors.UniqueViolation:
                    st.warning("Ese correo electrónico ya está registrado.")
                except Exception as e:
                    st.error(f"No se pudo completar el registro: {e}")

elif pagina == "Contacto":
    st.title("Contáctanos")
    col_info, col_form = st.columns([1, 2])

    with col_info:
        st.subheader("Pedicure Beauty")
        st.write("**WhatsApp:** +51 918 839 586")
        st.write("**Atención:** Con cita previa")
        st.link_button("Escribir por WhatsApp", WHATSAPP_URL, use_container_width=True)

    with col_form:
        with st.form("form_contacto", clear_on_submit=True):
            nombre = st.text_input("Nombre *", max_chars=100)
            correo = st.text_input("Correo electrónico *", max_chars=150)
            mensaje = st.text_area("Mensaje *", max_chars=2000)

            enviado = st.form_submit_button("Enviar mensaje", type="primary")
            if enviado:
                if not nombre.strip() or not correo.strip() or not mensaje.strip():
                    st.error("Completa todos los campos antes de enviar.")
                else:
                    try:
                        with get_connection() as conn:
                            with conn.cursor() as cur:
                                cur.execute(
                                    "INSERT INTO mensajes (nombre, correo, mensaje) VALUES (%s, %s, %s)",
                                    (nombre.strip(), correo.strip().lower(), mensaje.strip()),
                                )
                            conn.commit()
                        st.success("Mensaje enviado. ¡Gracias por escribirnos!")
                    except Exception as e:
                        st.error(f"No se pudo enviar el mensaje: {e}")

st.divider()
st.caption("© 2026 Pedicure Beauty. Todos los derechos reservados.")
