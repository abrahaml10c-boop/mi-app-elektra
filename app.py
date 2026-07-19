
import streamlit as st
from datetime import date

st.set_page_config(page_title="Control Abraham", page_icon="🏠")
st.title("🏠 Control - Abraham")

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

# --- 1. INGRESOS ---
st.header("1. Tus Ingresos")
mi_sueldo = st.number_input("Tu sueldo del viernes ($)", value=2500, step=100)
extra = st.number_input("Extra ($)", value=0, step=50)
total_ingresos = mi_sueldo + extra
st.metric("Total", f"${total_ingresos:,.0f}")

# --- 2. ELEKTRA ---
st.header("2. Elektra")
pago_elektra = st.number_input("Pago Elektra ($)", value=966)
if st.button("✅ Ya pagué Elektra" if not st.session_state.elektra_pagado else "✔️ PAGADO"):
    st.session_state.elektra_pagado = not st.session_state.elektra_pagado
    st.rerun()
dinero_para_casa = total_ingresos - pago_elektra

# --- 3. GASTOS ---
st.header("3. Casa")
total_gastos_semanales = 0
for i, g in enumerate(st.session_state.gastos):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    with c1:
        g["nombre"] = st.text_input("Nombre", value=g["nombre"], key=f"nom_{i}", label_visibility="collapsed")
    with c2:
        g["monto"] = st.number_input("Monto", value=g["monto"], key=f"mon_{i}", label_visibility="collapsed")
    with c3:
        g["tipo"] = st.selectbox("Tipo", ["Semanal", "Mensual"], index=0 if g["tipo"]=="Semanal" else 1, key=f"tip_{i}", label_visibility="collapsed")
    with c4:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()
    total_gastos_semanales += g["monto"]/4 if g["tipo"]=="Mensual" else g["monto"]

if st.button("➕ Agregar gasto"):
    st.session_state.gastos.append({"nombre": "Nuevo", "monto": 0, "tipo": "Semanal"})
    st.rerun()

restante = dinero_para_casa - total_gastos_semanales
st.divider()
if restante >= 500:
    st.balloons()
    st.success(f"TE QUEDAN ${restante:.0f} LIBRES")
elif restante >=0:
    st.success(f"Te quedan ${restante:.0f}")
else:
    st.error(f"Te faltan ${abs(restante):.0f}")

# --- 4. CALENDARIO 100% ESPAÑOL ---
st.header("4. Calendario")
st.write("Elige la semana (Todo en español)")

meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

c1, c2, c3 = st.columns(3)
with c1:
    dia = st.selectbox("Día", list(range(1,32)), index=date.today().day-1)
with c2:
    mes_nombre = st.selectbox("Mes", meses, index=date.today().month-1)
    mes_num = meses.index(mes_nombre)+1
with c3:
    anio = st.selectbox("Año", [2025,2026,2027], index=1)

fecha_es = f"{dia} de {mes_nombre} de {anio}"

st.info(f"Semana seleccionada: **{fecha_es}**")

if st.button("💾 Guardar semana", type="primary", use_container_width=True):
    st.session_state.historial.append({
        "fecha_es": fecha_es,
        "restante": restante,
        "elektra": "Pagado" if st.session_state.elektra_pagado else "Pendiente"
    })
    st.success(f"¡Guardado {fecha_es}!")

if st.session_state.historial:
    st.subheader("📜 Historial")
    for h in reversed(st.session_state.historial):
        icono = "✅" if h['restante']>=0 else "❌"
        st.write(f"{icono} {h['fecha_es']} | Quedaron ${h['restante']:.0f} | {h['elektra']}")
    if st.button("🗑️ Borrar historial"):
        st.session_state.historial=[]
        st.rerun()
