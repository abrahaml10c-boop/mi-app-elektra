
import streamlit as st
from datetime import date

st.set_page_config(page_title="Control Abraham", page_icon="🏠")
st.title("🏠 Control - Abraham")

# --- INICIALIZAR MEMORIA ---
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
st.header("1. Ingresos de la semana")
mi_sueldo = st.number_input("Tu sueldo (viernes)", value=2500)
extra = st.number_input("Extra", value=0)
total_ingresos = mi_sueldo + extra
st.metric("Total", f"${total_ingresos:,.0f}")

# --- 2. ELEKTRA ---
st.header("2. Elektra")
pago_elektra = st.number_input("Pago Elektra", value=966)

if st.button("✅ Ya pagué Elektra esta semana" if not st.session_state.elektra_pagado else "✔️ Elektra PAGADO"):
    st.session_state.elektra_pagado = not st.session_state.elektra_pagado
    st.rerun()

if st.session_state.elektra_pagado:
    st.success("Elektra pagado - ¡Bien hecho!")
else:
    st.warning("Pendiente de pagar Elektra")

dinero_para_casa = total_ingresos - pago_elektra

# --- 3. GASTOS ---
st.header("3. Casa - Renta, Gas, Luz, Internet")
total_gastos_semanales = 0
for i, g in enumerate(st.session_state.gastos):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    with c1:
        g["nombre"] = st.text_input(f"Concepto", value=g["nombre"], key=f"nom_{i}", label_visibility="collapsed")
    with c2:
        g["monto"] = st.number_input(f"Monto", value=g["monto"], key=f"mon_{i}", label_visibility="collapsed")
    with c3:
        g["tipo"] = st.selectbox("Tipo", ["Semanal", "Mensual"], index=0 if g["tipo"]=="Semanal" else 1, key=f"tip_{i}", label_visibility="collapsed")
    with c4:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()
    if g["tipo"] == "Mensual":
        total_gastos_semanales += g["monto"] / 4
    else:
        total_gastos_semanales += g["monto"]

if st.button("➕ Agregar gasto"):
    st.session_state.gastos.append({"nombre": "Nuevo", "monto": 0, "tipo": "Semanal"})
    st.rerun()

# --- 4. RESUMEN ---
st.divider()
restante = dinero_para_casa - total_gastos_semanales

st.header("4. Resumen")
st.write(f"Ingresos: ${total_ingresos:.0f} - Elektra: ${pago_elektra:.0f} - Casa: ${total_gastos_semanales:.0f}")

if restante >= 500:
    st.balloons()
    st.success(f"TE QUEDAN ${restante:.0f} LIBRES")
elif restante >= 0:
    st.success(f"TE QUEDAN ${restante:.0f} LIBRES")
else:
    st.error(f"Te faltan ${abs(restante):.0f}")

if st.button("💾 Guardar esta semana en historial"):
    st.session_state.historial.append({"fecha": str(date.today()), "restante": restante, "ingreso": total_ingresos})
    st.success("Guardado")

if st.session_state.historial:
    st.subheader("Historial")
    for h in reversed(st.session_state.historial[-5:]):
        st.write(f"{h['fecha']}: te quedaron ${h['restante']:.0f}")
