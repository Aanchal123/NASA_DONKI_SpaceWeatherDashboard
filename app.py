import streamlit as st
from PIL import Image

st.set_page_config(page_title="Space Weather Observatory", layout="wide")

st.title("☀️ Space Weather Observatory")

# 🌌 Insert the Solar System image
image = Image.open("Space.jpeg")  # Make sure this image is in the same directory or adjust the path accordingly
st.image(image, use_column_width=True, caption="The stage for space weather events")

st.markdown("""
Welcome to the NASA Space Weather Observatory — a collection of interactive dashboards powered by live data from the [DONKI API](https://kauai.ccmc.gsfc.nasa.gov/DONKI/).

This platform helps visualize and understand key space weather events that originate from solar activity and impact Earth’s magnetosphere and technology systems.

---

### 🌞 What You Can Explore

#### 🔸 Solar Flares
Sudden, intense bursts of radiation from the Sun's surface. Flares are classified as **C**, **M**, or **X** based on intensity. Severe flares can disrupt communications, GPS, and satellites.  

#### 🔸 Coronal Mass Ejections (CMEs)
Massive bursts of solar wind and magnetic fields rising above the solar corona and being released into space. CMEs can cause severe geomagnetic storms if Earth-directed.  

#### 🔸 Geomagnetic Storms
Disturbances in Earth's magnetic field caused by solar wind shockwaves or CMEs. Can cause auroras, power grid disruptions, and satellite malfunctions.  

#### 🔸 Interplanetary Shocks
Shocks formed in the solar wind due to abrupt changes in speed or density, often tied to CMEs or flares. These precede larger space weather events and can compress Earth's magnetic field.  

#### 🔸 Solar Energetic Particles (SEPs)
High-energy particles emitted by solar events. They can endanger astronauts and interfere with spacecraft electronics.  

---

### 🔭 Why This Matters

Understanding space weather is critical to:  
- 🛰️ **Protecting satellites & spacecraft**  
- 🧭 **Safeguarding communication and navigation systems**  
- ⚡ **Managing risks to power infrastructure**  
- 🚀 **Planning safe crewed missions to space**

All visualizations are interactive, updated via NASA’s DONKI API, and designed to be accessible for both public and research use.

---

### 👨‍💻 Project Team

Developed by:  

• Aanchal Malhotra  
• Ankit Sawant  
• Ishan Desai  
• Mihika Bodke  
• Jingchen Liu

---

### 🧭 Get Started
Use the sidebar to explore each event type!
""")
