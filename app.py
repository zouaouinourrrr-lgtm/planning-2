import streamlit as st
import random
import calendar
from datetime import datetime

st.title("🏠 Planning l'El Walda")

def generate_planning(year, month):
    exwet = ["Mouna", "Soumaya", "Hajer", "Khaled"]
    sans_hajer = ["Mouna", "Soumaya", "Khaled"]
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

user = st.selectbox("Eshkoun enti?", ["Mouna", "Soumaya", "Hajer", "Khaled"])
if st.button("Afficher mon planning "):
    now = datetime.now()
    plan = generate_planning(now.year, now.month)
    mes_jours = [d for d in plan if d["nom"] == user]
    for d in mes_jours:
        st.success(f"✅ {d['jour']} {d['date']}")
