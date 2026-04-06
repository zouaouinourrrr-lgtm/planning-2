import streamlit as st
import random
import calendar
from datetime import datetime

# 1. Config
st.set_page_config(page_title="Planning l'El Walda", page_icon="🏠")
st.title("🏠 Planning & Mode Urgence")

# 2. Fonction de génération
def generate_initial_planning(year, month):
    exwet = ["Mouna", "Soumaya", "Hajer", "Khaled"]
    num_days = calendar.monthrange(year, month)[1]
    pool = []
    for e in exwet: pool.extend([e] * (num_days // 4))
    pool.extend(random.sample(exwet, num_days % 4))
    random.shuffle(pool)

    planning = []
    last_p = None
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
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
        planning.append({"date": f"{day:02d}/{month:02d}", "jour": nom_j, "nom": chosen})
        last_p = chosen
    return planning

# 3. INITIALISATION
now = datetime.now()
if 'full_plan' not in st.session_state:
    st.session_state.full_plan = generate_initial_planning(now.year, now.month)

# 4. Interface
user = st.selectbox("Qui êtes-vous ?", ["Mouna", "Soumaya", "Hajer", "Khaled"])
today_str = now.strftime("%d/%m")

# Sécurité si le plan est vide
if st.session_state.full_plan:
    current_plan = st.session_state.full_plan
    tonight_idx = next((i for i, d in enumerate(current_plan) if d["date"] == today_str), None)

    st.divider()

    if tonight_idx is not None:
        guard_tonight = current_plan[tonight_idx]
        if guard_tonight["nom"] == user:
            st.error(f"🚨 **Urgence :** {user}, c'est ton tour ce soir !")
            if st.button("🚨 JE NE PEUX PAS CE SOIR"):
                others = [n for n in ["Mouna", "Soumaya", "Hajer", "Khaled"] if n != user]
                if guard_tonight["jour"] in ["Lundi", "Dimanche"]:
                    others = [n for n in others if n != "Hajer"]
                new_person = random.choice(others)
                st.session_state.full_plan[tonight_idx]["nom"] = new_person
                st.warning(f"🔄 Changement effectué ! **{new_person}** te remplace.")
                st.rerun()
        else:
            st.info(f"📅 Ce soir : **{guard_tonight['nom']}** est de garde.")

    st.divider()

    if st.button("Afficher mon planning complet"):
        st.subheader(f"📅 Tes nuits pour {calendar.month_name[now.month]} :")
        my_days = [d for d in st.session_state.full_plan if d["nom"] == user]
        for d in my_days:
            # EL FIX HOUNI: badalna "status" b "emoji" 3adi
            emoji = "🟢" if d["date"] != today_str else "🟠 (CE SOIR)"
            st.write(f"{emoji} **{d['jour']} {d['date']}**")

    # Sidebar Stats
    st.sidebar.header("📊 Score du mois")
    for p in ["Mouna", "Soumaya", "Hajer", "Khaled"]:
        count = sum(1 for d in st.session_state.full_plan if d["nom"] == p)
        st.sidebar.text(f"{p}: {count} nuits")
       


