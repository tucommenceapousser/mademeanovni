import streamlit as st
import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

st.set_page_config(
    page_title="TRHACKNON – Custom Devices",
    page_icon="🟢",
    layout="wide"
)

# ---------------------------------------
# STYLE HACKER DARK
# ---------------------------------------
st.markdown("""
<style>
body {
    background-color:#0A0A0A;
    color:#00FFD5;
}
h1,h2,h3 {
    color:#39ff14 !important;
}
.stButton>button {
    background:linear-gradient(90deg,#00ff88,#00e1ff);
    border-radius:12px;
    color:black;
    font-weight:bold;
}
.sidebar .sidebar-content {
    background:#111111;
}
.device-preview {
    padding: 15px;
    border: 1px solid #00ff88;
    border-radius: 12px;
    background-color: #111111;
}
</style>
""", unsafe_allow_html=True)

st.title("🛠️ TRHACKNON Custom Devices")
st.write("Crée ton appareil sur mesure : hardware + firmware + options + accessoires.")
st.write("---")

# ---------------------------------------
# IMAGES POUR CERTAINS APPAREILS
# ---------------------------------------
device_images = {
    "LilyGO T-Display S3": "lilygo.jpeg",
    "LilyGO T-Deck": "lilygo.jpeg",
    "LilyGO T-Pico": "lilygo.jpeg",
    "BjornOS": "bjorn.jpg",
    "Pwnagotchi": "pwnagotchi.webp",
    "ESP32 Marauder": "marauder.jpeg",
}

# ---------------------------------------
# BASE PRIX
# ---------------------------------------
boards = {
    "ESP32 DevKit": 25,
    "ESP32-S3": 35,
    "ESP32-C3": 18,
    "LilyGO T-Display S3": 42,
    "LilyGO T-Deck": 69,
    "LilyGO T-Pico": 48,
    "Heltec WiFi LoRa V3": 55,
    "Heltec CubeCell": 30,
    "Raspberry Pi Zero 2 W": 60,
    "Bus Pirate v6": 45,
    "ESP32 Marauder": 75
}

modules = {
    "Écran OLED 0.96\"": 8,
    "Écran IPS 1.9\"": 12,
    "GPS NEO-6M": 15,
    "LoRa SX1276": 17,
    "Caméra OV2640": 10,
    "Batterie LiPo 1200mAh": 9,
    "Batterie 18650": 6,
    "Chargeur TP4056": 3,
    "NRF24L01": 4,
}

firmwares = {
    "Bruce": 0,
    "GhostESP": 0,
    "CapybaraOS": 0,
    "BjornOS": 0,
    "Pwnagotchi": 0,
    "Firmware Bus Pirate": 0
}

options = {
    "Montage + soudure complète": 15,
    "Boîtier imprimé 3D": 12,
    "Flash du firmware & tests": 10,
    "Batterie intégrée & câblage": 7
}

# ---------------------------------------
# INTERFACE PRINCIPALE
# ---------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1️⃣ Sélectionne la carte principale")
    board = st.selectbox("Carte :", list(boards.keys()))
    base_price = boards[board]

    st.subheader("2️⃣ Choisis les modules")
    user_modules = st.multiselect("Modules & capteurs :", list(modules.keys()))

with col2:
    st.subheader("3️⃣ Choisis le Firmware")
    firmware = st.selectbox("Firmware :", list(firmwares.keys()))

    st.subheader("4️⃣ Options supplémentaires")
    user_options = st.multiselect("Options :", list(options.keys()))

# ---------------------------------------
# AFFICHAGE D'IMAGE SI DISPONIBLE
# ---------------------------------------
st.write("---")
st.subheader("📸 Aperçu du matériel")

preview_col = st.container()
with preview_col:
    st.markdown('<div class="device-preview">', unsafe_allow_html=True)

    img_displayed = False

    # Affiche image liée au firmware (ex : Bjorn, Pwnagotchi)
    if firmware in device_images:
        image_path = device_images[firmware]
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Firmware : {firmware}")
            img_displayed = True

    # Affiche image liée à la carte (ex : LilyGO)
    if not img_displayed and board in device_images:
        image_path = device_images[board]
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Appareil : {board}")
            img_displayed = True

    if not img_displayed:
        st.markdown("🕶️ _Aucune image disponible pour cet appareil._")

    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# ---------------------------------------
# CALCUL PRIX
# ---------------------------------------
total = base_price + sum(modules[m] for m in user_modules) + sum(options[o] for o in user_options)
st.markdown(f"## 💰 Total : **{total} €**")

buyer_name = st.text_input("Nom client :")
buyer_email = st.text_input("Email :")
add_notes = st.text_area("Notes spécifiques (couleur boîtier, dimensions, modifications...)")

st.write("---")


# ---------------------------------------
# PDF DEVIS
# ---------------------------------------
def generate_pdf(name, email, total, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, "TRHACKNON Custom Devices – Devis")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Client : {name}")
    c.drawString(50, 755, f"Email : {email}")
    c.drawString(50, 725, "Configuration sélectionnée :")

    y = 705
    c.setFont("Helvetica", 11)

    c.drawString(50, y, f"- Carte : {board} ({boards[board]} €)")
    y -= 20

    c.drawString(50, y, "- Modules :")
    y -= 20
    for m in user_modules:
        c.drawString(70, y, f"{m} ({modules[m]} €)")
        y -= 18

    c.drawString(50, y, "- Options :")
    y -= 20
    for o in user_options:
        c.drawString(70, y, f"{o} ({options[o]} €)")
        y -= 18

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 15, f"Total : {total} €")
    c.save()

# ---------------------------------------
# BOUTON PDF
# ---------------------------------------
if st.button("📄 Générer devis PDF"):
    if buyer_name.strip() == "" or buyer_email.strip() == "":
        st.error("Merci d’entrer nom + email pour générer un devis.")
    else:
        filename = f"devis_{buyer_name.replace(' ', '_')}.pdf"
        generate_pdf(buyer_name, buyer_email, total, filename)
        st.success("Devis généré avec succès !")
        with open(filename, "rb") as pdf:
            st.download_button(
                "📥 Télécharger le devis PDF",
                pdf,
                file_name=filename
            )

st.write("---")
st.info("📩 Pour commander : contactez-moi via Telegram @trhacknon ou WhatsApp.")
