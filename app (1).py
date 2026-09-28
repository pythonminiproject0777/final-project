import math
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Milling MRR & Power Estimator | Group KAI", page_icon="⚙️", layout="wide")

MATERIALS = {
    "Mild steel (1020)": 2000, "Medium-carbon steel (1045)": 2200, "Alloy steel (4140)": 2600,
    "Stainless steel (304)": 2400, "Grey cast iron": 1100, "Aluminium alloy": 700,
    "Brass / bronze": 800, "Titanium (Ti-6Al-4V)": 1400,
}

tab_web, tab_calc = st.tabs(["Web app (3D)", "Quick calculator"])

with tab_web:
    html = (Path(__file__).parent / "milling-estimator.html").read_text(encoding="utf-8")
    components.html(html, height=2600, scrolling=True)

with tab_calc:
    st.subheader("Milling MRR & Power Estimator · Group KAI")
    c1, c2 = st.columns(2)
    with c1:
        mat = st.selectbox("Workpiece material", list(MATERIALS), index=1)
        D = st.number_input("Cutter diameter (mm)", 10.0, 400.0, 100.0)
        z = st.number_input("Number of teeth", 1, 40, 8)
        fz = st.number_input("Feed per tooth (mm)", 0.01, 0.6, 0.15, 0.01)
    with c2:
        vc = st.number_input("Cutting speed (m/min)", 10.0, 1000.0, 180.0)
        ap = st.number_input("Depth of cut (mm)", 0.1, 20.0, 3.0)
        ae = st.number_input("Width of cut (mm)", 1.0, 400.0, 70.0)
        eta = st.slider("Machine efficiency (%)", 30, 100, 80) / 100

    n = 1000 * vc / (math.pi * D)
    vf = fz * z * n
    mrr = ae * ap * vf / 1000
    pc = mrr * MATERIALS[mat] / 60000
    pm = pc / eta
    m = st.columns(4)
    m[0].metric("Spindle speed", f"{n:,.0f} rpm")
    m[1].metric("Table feed rate", f"{vf:,.0f} mm/min")
    m[2].metric("MRR", f"{mrr:,.1f} cm³/min")
    m[3].metric("Motor power", f"{pm:,.2f} kW")
    if ae > D:
        st.warning("Width of cut exceeds cutter diameter.")
    st.caption("Group KAI · results are estimates based on handbook cutting-force values.")
