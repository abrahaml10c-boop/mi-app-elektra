
import streamlit as st
from datetime import date

st.set_page_config(page_title="Control Abraham", page_icon="🏠", layout="centered")
st.title("🏠 Control - Abraham")

# --- MEMORIA ---
if "gastos" not in st.session_state:
    st.session_state.gastos = [
        {"nombre": "Renta", "monto": 500, "tipo": "Semanal"},
        {"nombre": "Gas", "monto": 200, "tipo": "Mensual"},
        {"nombre": "Luz", "monto": 300, "tipo": "Mensual"},
        {"nombre": "Internet", "monto": 400, "tipo": "Mensual"},
    ]
if "historial" not in st.session_state:
    st.session_state.historial = []
if "elektra_pagado" not in st.session_state:
    st.session_state.elektra_pagado = False

meses_es = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

# --- 1. INGRESOS ---
st.header("1. Tus Ingresos")
mi_sueldo = st.number_input("Tu sueldo del viernes ($)", value=2500, step=100)
extra = st.number_input("Extra de la semana ($)", value=0, step=50)
total_ingresos = mi_sueldo + extra
st.metric("Total ingresos", f"${total_ingresos:,.0f}")

# --- 2. ELEKTRA ---
st.header("2. Elektra")
pago_elektra = st.number_input("Pago semanal Elektra ($)", value=966, step=10)

texto_boton = "✔️ ELEKTRA PAGADO" if st.session_state.elektra_pagado else "✅ Ya pagué Elektra"
if st.button(texto_boton, use_container_width=True):
    st.session_state.elektra_pagado = not st.session_state.elektra_pagado
    st.rerun()

if st.session_state.elektra_pagado:
    st.success("Elektra pagado - ¡Excelente!")
else:
    st.warning("Pendiente de pagar Elektra")

dinero_para_casa = total_ingresos - pago_elektra
st.info(f"Te quedan para la casa: ${dinero_para_casa:,.0f}")

# --- 3. GASTOS DE CASA ---
st.header("3. Gastos de Casa")
total_gastos_semanales = 0
for i, g in enumerate(st.session_state.gastos):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    with c1:
        g["nombre"] = st.text_input("Nombre", value=g["nombre"], key=f"nom_{i}", label_visibility="collapsed")
    with c2:
        g["monto"] = st.number_input("Monto", value=g["monto"], key=f"mon_{i}", label_visibility="collapsed", step=50)
    with c3:
        g["tipo"] = st.selectbox("Tipo", ["Semanal", "Mensual"], index=0 if g["tipo"]=="Semanal" else 1, key=f"tip_{i}", label_visibility="collapsed")
    with c4:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()
    # Convertir mensual a semanal
    if g["tipo"] == "Mensual":
        total_gastos_semanales += g["monto"] / 4
    else:
        total_gastos_semanales += g["monto"]

if st.button("➕ Agregar gasto"):
    st.session_state.gastos.append({"nombre": "Nuevo", "monto": 0, "tipo": "Semanal"})
    st.rerun()

st.write(f"**Total gastos casa por semana:** ${total_gastos_semanales:,.0f}")

# --- 4. RESUMEN + CALENDARIO ---
st.divider()
st.header("4. Resumen y Calendario")

restante = dinero_para_casa - total_gastos_semanales

if restante >= 500:
    st.balloons()
    st.success(f"¡TE QUEDAN ${restante:.0f} LIBRES! Vas con todo bro 🙏")
elif restante >= 0:
    st.success(f"Te quedan ${restante:.0f} libres")
else:
    st.error(f"Te faltan ${abs(restante):.0f} - Hay que recortar")

st.subheader("📅 ¿Qué semana es?")
semana = st.date_input("Elige el viernes de esta semana", value=date.today(), format="DD/MM/YYYY")
fecha_es = f"{semana.day} de {meses_es[semana.month-1]} de {semana.year}"

if st.button("💾 Guardar semana", use_container_width=True, type="primary"):
    st.session_state.historial.append({
        "fecha_es": fecha_es,
        "restante": restante,
        "ingreso": total_ingresos,
        "elektra": "Pagado" if st.session_state.elektra_pagado else "Pendiente"
    })
    st.success(f"Guardado: {fecha_es} - Te quedaron ${restante:.0f}")

# --- HISTORIAL ---
if st.session_state.historial:
    st.subheader("📜 Tu Historial")
    for h in reversed(st.session_state.historial[-10:]):
        icono = "✅" if h['restante'] >= 0 else "❌"
        st.write(f"{icono} **{h['fecha_es']}** | Quedaron: ${h['restante']:.0f} | Elektra: {h['elektra']}")
    
    if st.button("🗑️ Borrar todo el historial"):
        st.session_state.historial = []
        st.session_state.elektra_pagado = False
        st.rerun()
