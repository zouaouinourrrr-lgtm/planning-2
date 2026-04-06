import streamlit as st
import random
import calendar
from datetime import datetime

st.set_page_config(page_title="Planning l'El Walda", page_icon="🏠")
st.title("🏠 Planning & Mode Urgence")

# --- LOGIQUE DU PLANNING ---
def generate_initial_planning(year, month):
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
        planning.append({"date": f"{day:02d}/{month:02d}", "jour": nom_j, "nom": chosen})
        last_p = chosen
    return planning

# --- GESTION DE LA MÉMOIRE (Session State) ---
if 'full_plan' not in st.session_state:
    now = datetime.now()
    st.session_state.full_plan = generate_initial_planning(now.year, now.month)

# --- INTERFACE ---
user = st.selectbox("Qui êtes-vous ?", ["Mouna", "Soumaya", "Hajer", "Khaled"])
today_str = datetime.now().strftime("%d/%m")

# Trouver qui doit être là ce soir
tonight_idx = next((i for i, d in enumerate(st.session_state.full_plan) if d["date"] == today_str), None)

st.divider()

if tonight_idx is not None:
    current_guard = st.session_state.full_plan[tonight_idx]
    
    if current_guard["nom"] == user:
        st.error(f"🚨 **Urgence :** {user}, c'est ton tour ce soir !")
        
        # BOUTON SWAP (L'URGENCE)
        if st.sidebar.button("🚨 JE NE PEUX PAS CE SOIR"):
            # Chercher un remplaçant parmi les 3 autres
            others = [n for n in ["Mouna", "Soumaya", "Hajer", "Khaled"] if n != user]
            # Contrainte Hajer : mouch Lundi/Dimanche
            if current_guard["jour"] in ["Lundi", "Dimanche"]:
                others = [n for n in others if n != "Hajer"]
            
            new_person = random.choice(others)
            st.session_state.full_plan[tonight_idx]["nom"] = new_person
            st.warning(f"🔄 Changement effectué ! **{new_person}** te remplace pour ce soir.")
            st.rerun()
            
    else:
        st.info(f"📅 Ce soir : **{current_guard['nom']}** est de garde.")

st.divider()

# --- AFFICHAGE DU PLANNING ---
if st.button("Afficher mon planning"):
    my_days = [d for d in st.session_state.full_plan if d["nom"] == user]


