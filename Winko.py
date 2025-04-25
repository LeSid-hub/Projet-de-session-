import streamlit as st
from db import ajouter_abonnement
from db import ajouter_abonnement, recuperer_abonnements
import pandas as pd

def afficher_formulaire_ajout():
    st.header("➕ Ajouter un abonnement")
    st.info("Formulaire d’ajout à venir ici...")
def afficher_abonnements():
    st.header("📄 Mes abonnements")
    st.info("Liste des abonnements ici...")

def afficher_statistiques():
    st.header("📊 Statistiques")
    st.info("Graphiques et données ici...")



with st.sidebar:
    nom_utilisateur = st.text_input("👤 Nom de l'utilisateur", placeholder="Entrez votre nom")
    st.markdown(f"Bienvenue, **{nom_utilisateur or 'Invité'}** 👋")

# 📍 Barre latérale de navigation
with st.sidebar:
    st.markdown("## 🔍 Navigation")
    page = st.radio(
        "",
        ["🏠 Accueil", "➕ Ajouter", "📄 Mes abonnements", "📊 Statistiques"]
    )
 
 


# 🧠 ROUTEUR : Affichage selon l'onglet sélectionné
if page == "🏠 Accueil":
    st.title("🎟️ Winko – Suivi de vos abonnements")
    st.subheader("Bienvenue sur votre tableau de bord 📊")
    st.markdown("""
    **Winko** vous aide à :  
    - 💡 Garder une vue claire sur vos abonnements  
    - 🔔 Éviter les surprises à la fin du mois  
    - 📉 Identifier les services inutilisés  
    - 🧾 Simplifier votre gestion financière
    """)

    st.success("Commencez en cliquant sur '➕ Ajouter' pour enregistrer votre premier abonnement.")

elif page == "➕ Ajouter":
    # 👇 Ici tu appelles ton code du formulaire d’ajout
    afficher_formulaire_ajout()

elif page == "📄 Mes abonnements":
    # 👇 Tu appelles ici ton affichage des abonnements enregistrés
    afficher_abonnements()

elif page == "📊 Statistiques":
    # 👇 Tu pourrais afficher ici : total annuel, graphique, nombre d'abonnements, etc.
    afficher_statistiques()



# 🎨 Style moderne et sobre
st.markdown("""
    <style>
    /* Page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Titres */
    h1 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        font-size: 2.2rem;
        color: #262730;
    }

    h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
        color: #444;
    }

    /* Textes */
    .stMarkdown {
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        color: #333;
    }

    /* Boutons */
    button {
        border-radius: 6px !important;
    }

    /* Champs du formulaire */
    input, select, textarea {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.05rem !important;
    }

    </style>
""", unsafe_allow_html=True)


# Ligne de séparation
st.markdown("---")

st.header("➕ Ajouter un nouvel abonnement")

# Formulaire d'ajout
with st.form("form_ajout"):
    nom = st.text_input("Nom de l’abonnement", placeholder="ex: Netflix")
    montant = st.number_input("Montant mensuel ($)", min_value=0.0, step=0.5)
    frequence = st.selectbox("Fréquence", ["Mensuel", "Annuel", "Hebdomadaire"])
    date_debut = st.date_input("Date de début")

    # Bouton de soumission
    submit = st.form_submit_button("Ajouter l’abonnement")

if submit:
    ajouter_abonnement(nom, montant, frequence, date_debut)
    st.session_state["form_cleared"] = True
    st.success(f"✅ Abonnement à **{nom}** ajouté avec succès !")









from db import recuperer_abonnements, ajouter_abonnement, supprimer_abonnement

st.markdown("## 📋 Mes abonnements enregistrés")

abonnements = recuperer_abonnements()

if abonnements:
    for nom, montant, frequence, date_debut in abonnements:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f"📌 **{nom}** – {montant:.2f} $ – {frequence} – depuis le {date_debut}"
            )
        with col2:
            if st.button("🗑 Supprimer", key=f"{nom}_{date_debut}"):
                supprimer_abonnement(nom, date_debut)
                st.success(f"❌ Abonnement à **{nom}** supprimé.")
                

    # Total mensuel
    total = sum([montant for _, montant, *_ in abonnements])
    st.markdown(f"💸 **Coût mensuel total : {total:.2f} $**")

else:
    st.info("Aucun abonnement enregistré.")



df = pd.DataFrame(abonnements, columns=["Nom", "Montant ($)", "Fréquence", "Date de début"])
df.index += 1
df.index.name = "N°"



st.dataframe(
    df.style.set_properties(**{
        'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#f4f4f4'), ('text-align', 'center')]
    }])
)


if page == "➕ Ajouter":
    afficher_formulaire_ajout()
elif page == "📄 Mes abonnements":
    afficher_abonnements()
elif page == "📊 Statistiques":
    afficher_statistiques()

def calculer_depenses_previsionnelles(abonnements, mois=3):
    total = sum(montant for _, montant, *_ in abonnements) * mois
    return total


from datetime import datetime, timedelta

def afficher_alertes_renouvellement(abonnements):
    aujourd_hui = datetime.today().date()
    for nom, _, _, date_debut in abonnements:
        prochaine_date = datetime.strptime(date_debut, "%Y-%m-%d").date()
        while prochaine_date < aujourd_hui:
            prochaine_date += timedelta(days=30)  # ou 365 pour annuels

        jours_restant = (prochaine_date - aujourd_hui).days
        if jours_restant <= 7:
            st.info(f"📅 L’abonnement à **{nom}** sera renouvelé dans {jours_restant} jours.")



















