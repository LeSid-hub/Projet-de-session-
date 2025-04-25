import sqlite3

def ajouter_abonnement(nom, montant, frequence, date_debut):
    print("✅ Données reçues :", nom, montant, frequence, date_debut)
    conn = sqlite3.connect('abonnements.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO abonnements (nom, montant, frequence, date_debut)
        VALUES (?, ?, ?, ?)
    """, (nom, montant, frequence, str(date_debut)))
    conn.commit()
    conn.close()

    # Fonction pour récupérer tous les abonnements
def recuperer_abonnements():
    conn = sqlite3.connect('abonnements.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nom, montant, frequence, date_debut FROM abonnements")
    resultats = cursor.fetchall()
    conn.close()
    return resultats

def supprimer_abonnement(nom, date_debut):
    conn = sqlite3.connect('abonnements.db')
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM abonnements
        WHERE nom = ? AND date_debut = ?
    """, (nom, str(date_debut)))
    conn.commit()
    conn.close()




