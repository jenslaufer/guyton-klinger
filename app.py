import streamlit as st

from entnahme import naechste_entnahme

st.set_page_config(page_title="Guyton-Klinger Entnahme-Rechner", layout="centered")

st.title("🛡️ Guyton-Klinger Entnahme-Rechner")
st.write("Deine persönliche Entnahmestrategie für den Ruhestand ab Januar.")


# Sidebar für Grundeinstellungen
st.sidebar.header("Grunddaten")
start_portfolio = st.sidebar.number_input("Start-Depotwert (EUR)", value=1000000.0, step=10000.0)
start_withdrawal = st.sidebar.number_input("Gewünschte Start-Entnahme (EUR/Jahr)", value=36000.0, step=1000.0)

upper_guardrail = st.sidebar.slider("Obere Leitplanke (% Abweichung zur Startrate)", 10, 30, 20) / 100.0
lower_guardrail = st.sidebar.slider("Untere Leitplanke (% Abweichung zur Startrate)", 10, 30, 20) / 100.0
adjustment_pct = st.sidebar.slider("Anpassungs-Schritt bei Leitplanken", 5, 20, 10) / 100.0

initial_rate = start_withdrawal / start_portfolio
upper_threshold = initial_rate * (1 + upper_guardrail)
lower_threshold = initial_rate * (1 - lower_guardrail)

st.divider()

# Dashboard-Metriken
col1, col2, col3 = st.columns(3)
col1.metric("Depotwert Basis", f"{start_portfolio:,.2f} EUR")
col2.metric("Jährliche Entnahme", f"{start_withdrawal:,.2f} EUR", f"{start_withdrawal/12:,.2f} EUR / Mo")
col3.metric("Start-Entnahmerate", f"{initial_rate*100:.2f}%")

st.info(f"Leitplanken-Schwellen: Oberer Schwellenwert (Kürzung bei >): {upper_threshold*100:.2f}% | Unterer Schwellenwert (Erhöhung bei <): {lower_threshold*100:.2f}%")

st.divider()
st.subheader("Jährliche Neuberechnung & Simulation")

year = st.number_input("Aktuelles Jahr", value=2027, step=1)
current_portfolio = st.number_input("Depotwert am Jahresende (EUR)", value=1020000.0, step=10000.0)
inflation_rate = st.number_input("Inflation zum Vorjahr (%)", value=2.0, step=0.1) / 100.0

if "current_withdrawal" not in st.session_state:
    st.session_state.current_withdrawal = start_withdrawal

if st.button("Entnahme für das nächste Jahr berechnen"):
    neue_entnahme, regel = naechste_entnahme(
        st.session_state.current_withdrawal,
        current_portfolio,
        inflation_rate,
        upper_threshold,
        lower_threshold,
        adjustment_pct,
    )

    if regel == "oben":
        action_text = f"🚨 OBERE LEITPLANKE GEGRIFFEN: Entnahme um {int(adjustment_pct*100)}% gekürzt!"
    elif regel == "unten":
        action_text = f"🚀 UNTERE LEITPLANKE GEGRIFFEN: Entnahme um {int(adjustment_pct*100)}% erhöht!"
    else:
        action_text = "Standard (Inflationsangepasst)"

    st.session_state.current_withdrawal = neue_entnahme

    st.success("Berechnung erfolgreich durchgeführt!")
    st.markdown(f"### Resultat für das Folgejahr:")
    st.write(f"- Neue Entnahme (jährlich): {st.session_state.current_withdrawal:,.2f} EUR")
    st.write(f"- Neue Entnahme (monatlich): {st.session_state.current_withdrawal/12:,.2f} EUR / Monat")
    st.write(f"- Effektive Entnahmerate: {(st.session_state.current_withdrawal/current_portfolio)*100:.2f}%")
    st.write(f"- Status: {action_text}")
