
import streamlit as st
import math

st.title("UA and NTU Estimator for Air-Cooled Condenser")

st.header("🔧 Coil and Airflow Inputs")

# Coil geometry
rows = st.number_input("Number of Tube Rows", value=4)
tubes_per_row = st.number_input("Tubes per Row", value=80)
tube_length = st.number_input("Tube Length (m)", value=2.5)
tube_od = st.number_input("Tube Outer Diameter (m)", value=0.009525)
fpi = st.number_input("Fins per Inch (FPI)", value=10)
fin_thickness = st.number_input("Fin Thickness (mm)", value=0.0155) / 1000

# Air properties
airflow = st.number_input("Air Volume Flow Rate (m³/s)", value=12.0)
air_inlet_temp = st.number_input("Air Inlet Temperature (°C)", value=35.0)
air_outlet_temp = st.number_input("Air Outlet Temperature (°C)", value=48.0)

# Refrigerant heat rejection
q_refrigerant = st.number_input("Total Heat Load (kW)", value=180.0)

# Constants for air
cp_air = 1.005  # kJ/kg.K
rho_air = 1.16  # kg/m³ at ~35°C
mu_air = 1.9e-5  # Pa.s
k_air = 0.0263   # W/m.K

st.header("📐 Area and h Estimation")

# Fin calculations
fin_density = fpi * 39.37  # fins/m
fin_surface_area = fin_density * tube_length * rows * tubes_per_row * 0.020 * 2  # approx per fin: 20mm wide
bare_tube_area = math.pi * tube_od * tube_length * rows * tubes_per_row

# Total external area
A_total = fin_surface_area + bare_tube_area

# Air velocity and Re
flow_area = tube_length * 0.6  # Assume 0.6m coil height across face
v_air = airflow / flow_area
Re_air = (rho_air * v_air * tube_od) / mu_air

# Air-side h (Dittus-Boelter style estimate)
Nu = 0.3 + 0.62 * Re_air**0.5 * (cp_air * 1000 * mu_air / k_air)**(1/3)
h_air = Nu * k_air / tube_od

# Estimate overall U (assume h_refrigerant = 1800 W/m²·K, fouling resistances small)
h_refrigerant = 1800
U_est = 1 / (1/h_air + 1/h_refrigerant)

# UA and NTU
UA = U_est * A_total  # W/K
c_min = airflow * rho_air * cp_air * 1000  # W/K
ntu = UA / c_min

details = f"""
### 🔍 Results
- Total External Area (m²): {A_total:.1f}
- Air Velocity (m/s): {v_air:.2f}
- Reynolds Number (air): {Re_air:.0f}
- Air-side Heat Transfer Coeff. h (W/m²·K): {h_air:.1f}
- Overall U (W/m²·K): {U_est:.1f}
- Total UA (W/K): {UA:.0f}
- NTU: {ntu:.2f}
"""

st.markdown(details)
