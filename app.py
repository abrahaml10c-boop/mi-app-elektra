
import streamlit as st

st.set_page_config(page_title="Control Familiar Abraham", page_icon="🏠")

st.title("🏠 Control Familiar - Abraham")
st.caption("Tú: semanal (viernes) | Esposa: quincenal")

# --- INGRESOS ---
st.header("1. Ingresos")
col1, col2 = st.columns(2)
with col1:
    mi_sueldo = st.number_input("Tu sueldo (viernes)", value=2500)
with col2:
    sueldo_esposa_qna = st.number_input("Sueldo esposa (quincenal)", value=3000)

ingreso_esposa_semanal = sueldo_esposa_qna / 2
extra = st.number_input("Extra / Otro ingreso", value=0)

total_ingresos = mi_sueldo + ingreso_esposa_semanal + extra
st.info(f"Total para esta semana: ${total_ingresos:,.0f} (Tuyo ${mi_sueldo} + Esposa ${ingreso_esposa_semanal:.0f} + Extra ${extra})")

# --- ELEKTRA PRIMERO ---
st.header("2. Elektra - PRIORIDAD")
pago_elektra = st.number_input("Pago Elektra semanal", value=966)
dinero_para_casa = total_ingresos - pago_elektra

if dinero_para_casa < 0:
    st.error(f"🚨 ¡ALERTA! Te faltan ${abs(dinero_para_casa):.0f} para pagar Elektra")
else:
    st.success(f"✅ Pagas Elektra y te quedan ${dinero_para_casa:.0f} para la casa")

# --- GASTOS CASA ---
st.header("3. Gastos de Casa")

if "gastos" not in st.session_state:
    st.session_state.gastos = [
        {"nombre": "Renta", "monto": 500, "tipo": "Semanal"},
        {"nombre": "Gas", "monto": 200, "tipo": "Mensual"},
        {"nombre": "Luz", "monto": 300, "tipo": "Mensual"},
        {"nombre": "Internet", "monto": 400, "tipo": "Mensual"},
    ]

# Mostrar gastos
total_gastos_semanales = 0
for i, g in enumerate(st.session_state.gastos):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    with c1:
        g["nombre"] = st.text_input(f"Concepto {i+1}", value=g["nombre"], key=f"nom_{i}")
    with c2:
        g["monto"] = st.number_input(f"Monto", value=g["monto"], key=f"mon_{i}")
    with c3:
        g["tipo"] = st.selectbox("Tipo", ["Semanal", "Mensual"], index=0 if g["tipo"]=="Semanal" else 1, key=f"tip_{i}")
    with c4:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.gastos.pop(i)
            st.rerun()
    
    # Convertir a semanal
    if g["tipo"] == "Mensual":
        total_gastos_semanales += g["monto"] / 4
    else:
        total_gastos_semanales += g["monto"]

if st.button("➕ Agregar otro gasto"):
    st.session_state.gastos.append({"nombre": "Nuevo", "monto": 0, "tipo": "Semanal"})
    st.rerun()

st.divider()
st.metric("Total gastos esta semana", f"${total_gastos_semanales:.0f}")

# --- RESUMEN FINAL ---
restante = dinero_para_casa - total_gastos_semanales
st.header("4. Resumen Final")

st.write(f"Ingresos: ${total_ingresos:.0f}")
st.write(f"- Elektra: ${pago_elektra:.0f}")
st.write(f"- Casa: ${total_gastos_semanales:.0f}")

if restante >= 0:
    if restante >= 500:
        st.balloons()
    st.success(f"¡TE QUEDAN ${restante:.0f} LIBRES! Vas con todo bro 🙏")
else:
    st.error(f"Te faltan ${abs(restante):.0f}. Hay que recortar gastos esta semana")
