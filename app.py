import streamlit as st
import random
import calendar
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Planning l'El Walda", page_icon="🏠")
st.title("🏠 Planning de Garde Familial")

# --- LOGIC DU PLANNING ---
@st.cache_data # Houni bech el planning maytebdalch kol ma ta3mel refresh
def generate_planning(year, month):
    exwet = ["Mouna", "Soumaya", "Hajer", "Khaled"]
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    num_days = calendar.monthrange(year, month)[1]
    
    pool = []
    for e in exwet: pool.extend([e] * (num_days // 4))
    pool.extend(random.sample(exwet, num_days % 4))
    random.shuffle(pool)

    planning = []
    last_p = None
    for day in range(1, num_days + 1):
        wd = calendar.weekday(year, month, day)
        nom_j = jours_fr[wd]
        cand = [p for p in pool if p != last_p]
        chosen = None
        if nom_j in ["Mardi", "Mercredi"] and "Soumaya" in cand: chosen = "Soumaya"
        elif nom_j in ["Lundi", "Dimanche"]:
            safe = [p for p in cand if p != "Hajer"]
            if safe: chosen = random.choice(safe)
        if not chosen: chosen = random.choice(cand) if cand else random.choice(exwet)
        if chosen in pool: pool.remove(chosen)
        planning.append({"date": f"{day:02d}/{month:02d}", "jour": nom_j, "nom": chosen, "day_int": day})
        last_p = chosen
    return planning

# --- INTERFACE ---
user = st.selectbox("Qui êtes-vous ?", ["Mouna", "Soumaya", "Hajer", "Khaled"])

now = datetime.now()
current_plan = generate_planning(now.year, now.month)

# 1. NOTIFICATION DE CE SOIR (Faza 9wiya)
today_str = now.strftime("%d/%m")
today_guard = next((d for d in current_plan if d["date"] == today_str), None)

st.divider()

if today_guard:
    if today_guard["nom"] == user:
        st.error(f"🔔 **NOTIFICATION :** C'est TON tour ce soir, **{user}** ! N'oublie pas l'Walda. ❤️")
        st.balloons()
        # Bouton Check-in
        if st.button("✅ J'ai fait ma garde / Je suis présent"):
            st.success("C'est noté ! Merci pour ton dévouement. 🙏")
    else:
        st.info(f"📅 Ce soir ({today_str}), c'est le tour de : **{today_guard['nom']}**")

st.divider()

# 2. PLANNING PERSONNEL
if st.button("Afficher mon planning complet"):
    mes_jours = [d for d in current_plan if d["nom"] == user]
    st.subheader(f"📅 Tes nuits en {calendar.month_name[now.month]} :")
    for d in mes_jours:
        if d["date"] == today_str:
            st.warning(f"👉 {d['jour']} {d['date']} (AUJOURD'HUI)")
        else:
            st.success(f"✅ {d['jour']} {d['date']}")

# Sidebar pour les stats
st.sidebar.write(f"Année: {now.year} | Mois: {now.month}")
st.sidebar.info("Le planning est généré automatiquement avec équité totale.")


