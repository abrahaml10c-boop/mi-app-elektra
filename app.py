import streamlit as st

st.title("Mi Control Elektra - Mai")
st.write("Préstamo de $58,500 - Pago $966 x semana")

sueldo = st.number_input("¿Cuánto ganaste esta semana?", min_value=0, value=2500, step=100)
deuda_hoy = 32960
pago_semana = 966
semanas_faltan = 46

if st.button("Calcular mi semana"):
    queda = sueldo - pago_semana
    
    st.divider()
    st.subheader(f"Te quedan: ${queda}")
    
    if queda >= 1000:
        st.success("✅ Vas bien bro, la armas")
    elif queda >= 500:
        st.warning("⚠️ Vas justo, no gastes de más")
    else:
        st.error("🚨 Estás muy apretado, cuidado")

    st.divider()
    st.write(f"Si liquidas hoy debes: **${deuda_hoy}**")
    st.write(f"Si pagas semana a semana pagarás: **${pago_semana * semanas_faltan}**")
    st.write(f"Te ahorras liquidando hoy: **${(pago_semana * semanas_faltan) - deuda_hoy}**")

    extra = st.number_input("¿Si das extra cuánto darías?", min_value=0, value=0, step=50)
    if extra > 0:
        nueva_deuda = deuda_hoy - extra
        st.info(f"Si das ${extra} extra, tu nueva deuda sería ${nueva_deuda}")
