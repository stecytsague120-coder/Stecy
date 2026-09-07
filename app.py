import mysql.connector
import random
from datetime import datetime, timedelta

# Configuration de la connexion à la base de données
config = {
    'user': 'root',
    'password': 'votre_mot_de_passe',
    'host': 'localhost',
    'database': 'boutique_telephone',
    'raise_on_warnings': True
}

def creer_base_de_donnees():
    """Crée la base de données et les tables nécessaires"""
    try:
        # Connexion sans base de données spécifique
        conn = mysql.connector.connect(
            user=config['user'],
            password=config['password'],
            host=config['host']
        )
        cursor = conn.cursor()
        
        # Création de la base de données
        cursor.execute("CREATE DATABASE IF NOT EXISTS boutique_telephone")
        cursor.execute("USE boutique_telephone")
        
        # Table des marques
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS marques (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(50) NOT NULL UNIQUE,
                pays_origine VARCHAR(50)
            )
        """)
        
        # Table des téléphones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telephones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                marque_id INT,
                modele VARCHAR(100) NOT NULL,
                prix_achat DECIMAL(10,2) NOT NULL,
                prix_vente DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0,
                couleur VARCHAR(30),
                memoire_stockage VARCHAR(20),
                ram VARCHAR(10),
                date_arrivee DATE,
                FOREIGN KEY (marque_id) REFERENCES marques(id)
            )
        """)
        
        # Table des ventes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telephone_id INT,
                quantite INT NOT NULL,
                prix_unitaire DECIMAL(10,2) NOT NULL,
                date_vente DATETIME DEFAULT CURRENT_TIMESTAMP,
                client_nom VARCHAR(100),
                client_email VARCHAR(100),
                FOREIGN KEY (telephone_id) REFERENCES telephones(id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Base de données créée avec succès")
        
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de la création de la base: {err}")

def inserer_donnees_aleatoires():
    """Insère des données aléatoires dans la base"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Marques de téléphones avec leurs pays d'origine
        marques = [
            ('Apple', 'États-Unis'),
            ('Samsung', 'Corée du Sud'),
            ('Xiaomi', 'Chine'),
            ('Huawei', 'Chine'),
            ('Google', 'États-Unis'),
            ('OnePlus', 'Chine'),
            ('Sony', 'Japon'),
            ('Nokia', 'Finlande'),
            ('LG', 'Corée du Sud'),
            ('Motorola', 'États-Unis')
        ]
        
        print("\n📱 Insertion des marques...")
        for marque, pays in marques:
            cursor.execute("INSERT IGNORE INTO marques (nom, pays_origine) VALUES (%s, %s)", (marque, pays))
        
        conn.commit()
        
        # Récupération des marques pour les utiliser dans les téléphones
        cursor.execute("SELECT id, nom FROM marques")
        marques_data = cursor.fetchall()
        marques_dict = {nom: id for id, nom in marques_data}
        
        # Modèles de téléphones par marque
        modeles = {
            'Apple': ['iPhone 15', 'iPhone 15 Pro', 'iPhone 15 Pro Max', 'iPhone 14', 'iPhone 14 Pro'],
            'Samsung': ['Galaxy S24', 'Galaxy S24 Ultra', 'Galaxy A55', 'Galaxy Z Fold 5', 'Galaxy Z Flip 5'],
            'Xiaomi': ['Xiaomi 14', 'Xiaomi 14 Pro', 'Redmi Note 13', 'POCO X6 Pro', 'Xiaomi 13T'],
            'Huawei': ['P60 Pro', 'Mate 60 Pro', 'Pura 70', 'Nova 12'],
            'Google': ['Pixel 9', 'Pixel 9 Pro', 'Pixel 8', 'Pixel 8 Pro'],
            'OnePlus': ['OnePlus 12', 'OnePlus 12R', 'OnePlus Nord 4', 'OnePlus Open'],
            'Sony': ['Xperia 1 VI', 'Xperia 5 V', 'Xperia 10 VI'],
            'Nokia': ['Nokia G42', 'Nokia X30', 'Nokia G60'],
            'LG': ['LG Velvet', 'LG Wing'],
            'Motorola': ['Motorola Edge 50', 'Moto G84', 'Moto Razr 40']
        }
        
        couleurs = ['Noir', 'Blanc', 'Bleu', 'Vert', 'Rouge', 'Or', 'Gris', 'Violet', 'Rose', 'Bleu ciel']
        stockages = ['64GB', '128GB', '256GB', '512GB', '1TB']
        rams = ['4GB', '6GB', '8GB', '12GB', '16GB']
        
        print("📱 Insertion des téléphones...")
        telephones_data = []
        
        for marque, marque_id in marques_dict.items():
            if marque in modeles:
                for modele in modeles[marque]:
                    # Génération aléatoire des prix et stocks
                    prix_achat = round(random.uniform(150, 1200), 2)
                    prix_vente = round(prix_achat * random.uniform(1.2, 1.5), 2)
                    stock = random.randint(0, 50)
                    couleur = random.choice(couleurs)
                    stockage = random.choice(stockages)
                    ram = random.choice(rams)
                    
                    # Date d'arrivée aléatoire dans les 30 derniers jours
                    date_arrivee = datetime.now() - timedelta(days=random.randint(0, 30))
                    
                    cursor.execute("""
                        INSERT INTO telephones 
                        (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (marque_id, modele, prix_achat, prix_vente, stock, couleur, stockage, ram, date_arrivee))
                    
                    # Stockage pour les ventes
                    telephones_data.append({
                        'modele': modele,
                        'prix_vente': prix_vente,
                        'stock': stock
                    })
        
        conn.commit()
        
        # Récupération des téléphones pour les ventes
        cursor.execute("SELECT id, modele, prix_vente, stock FROM telephones")
        telephones = cursor.fetchall()
        
        print("💳 Insertion des ventes...")
        noms_clients = [
            'Jean Dupont', 'Marie Martin', 'Pierre Durand', 'Sophie Bernard', 'Lucas Petit',
            'Emma Robert', 'Thomas Richard', 'Chloé Moreau', 'Antoine Laurent', 'Julie Simon',
            'Nicolas Michel', 'Camille Lefèvre', 'David Leroy', 'Laura Garcia', 'Maxime David'
        ]
        
        # Création de ventes aléatoires
        for _ in range(random.randint(20, 50)):
            telephone = random.choice(telephones)
            if telephone[3] > 0:  # Vérifier qu'il y a du stock
                quantite = random.randint(1, min(3, telephone[3]))
                prix_vente = telephone[2]
                client_nom = random.choice(noms_clients)
                client_email = f"{client_nom.lower().replace(' ', '.')}@email.com"
                date_vente = datetime.now() - timedelta(days=random.randint(0, 15))
                
                cursor.execute("""
                    INSERT INTO ventes (telephone_id, quantite, prix_unitaire, date_vente, client_nom, client_email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (telephone[0], quantite, prix_vente, date_vente, client_nom, client_email))
                
                # Mise à jour du stock
                cursor.execute("""
                    UPDATE telephones 
                    SET stock = stock - %s 
                    WHERE id = %s
                """, (quantite, telephone[0]))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Données insérées avec succès!")
        print(f"   - {len(marques)} marques")
        print(f"   - {len(telephones)} téléphones")
        print(f"   - Ventes aléatoires générées")
        
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'insertion: {err}")

def afficher_rapport_stock():
    """Affiche un rapport détaillé du stock"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("📊 RAPPORT DE STOCK - BOUTIQUE DE TÉLÉPHONES")
        print("="*80)
        
        # Rapport par marque
        print("\n🔹 RAPPORT PAR MARQUE:")
        cursor.execute("""
            SELECT m.nom, COUNT(t.id) as total_modele, SUM(t.stock) as stock_total,
                   SUM(t.stock * t.prix_vente) as valeur_stock
            FROM marques m
            LEFT JOIN telephones t ON m.id = t.marque_id
            GROUP BY m.id
            ORDER BY stock_total DESC
        """)
        
        for marque in cursor.fetchall():
            print(f"  {marque[0]}: {marque[1]} modèles, {marque[2]} unités en stock (valeur: {marque[3]:.2f}€)")
        
        # Top 5 des téléphones les plus en stock
        print("\n🔹 TOP 5 DES TÉLÉPHONES LES PLUS EN STOCK:")
        cursor.execute("""
            SELECT m.nom, t.modele, t.stock, t.couleur, t.memoire_stockage
            FROM telephones t
            JOIN marques m ON t.marque_id = m.id
            ORDER BY t.stock DESC
            LIMIT 5
        """)
        
        for i, telephone in enumerate(cursor.fetchall(), 1):
            print(f"  {i}. {telephone[0]} {telephone[1]} - {telephone[3]} {telephone[4]} - Stock: {telephone[2]}")
        
        # Produits en rupture de stock
        print("\n🔹 PRODUITS EN RUPTURE DE STOCK:")
        cursor.execute("""
            SELECT m.nom, t.modele, t.couleur
            FROM telephones t
            JOIN marques m ON t.marque_id = m.id
            WHERE t.stock = 0
        """)
        
        produits_rupture = cursor.fetchall()
        if produits_rupture:
            for telephone in produits_rupture:
                print(f"  ⚠️  {telephone[0]} {telephone[1]} ({telephone[2]})")
        else:
            print("  ✅ Aucun produit en rupture de stock")
        
        # Statistiques globales
        print("\n🔹 STATISTIQUES GLOBALES:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total_produits,
                SUM(stock) as stock_total,
                SUM(stock * prix_vente) as valeur_stock_total,
                AVG(prix_vente) as prix_moyen,
                MIN(prix_vente) as prix_min,
                MAX(prix_vente) as prix_max
            FROM telephones
        """)
        
        stats = cursor.fetchone()
        print(f"  📱 Total produits: {stats[0]}")
        print(f"  📦 Stock total: {stats[1]} unités")
        print(f"  💰 Valeur du stock: {stats[2]:.2f}€")
        print(f"  💵 Prix de vente moyen: {stats[3]:.2f}€")
        print(f"  📉 Prix le plus bas: {stats[4]:.2f}€")
        print(f"  📈 Prix le plus élevé: {stats[5]:.2f}€")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'affichage du rapport: {err}")

def afficher_ventes_recentes():
    """Affiche les ventes récentes"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("🛒 VENTES RÉCENTES")
        print("="*80)
        
        cursor.execute("""
            SELECT v.date_vente, m.nom, t.modele, v.quantite, v.prix_unitaire,
                   (v.quantite * v.prix_unitaire) as total, v.client_nom
            FROM ventes v
            JOIN telephones t ON v.telephone_id = t.id
            JOIN marques m ON t.marque_id = m.id
            ORDER BY v.date_vente DESC
            LIMIT 10
        """)
        
        for vente in cursor.fetchall():
            print(f"  📅 {vente[0].strftime('%d/%m/%Y %H:%M')} - {vente[1]} {vente[2]}")
            print(f"     Quantité: {vente[3]} x {vente[4]:.2f}€ = {vente[5]:.2f}€")
            print(f"     Client: {vente[6]}")
            print()
        
        # Total des ventes
        cursor.execute("""
            SELECT COUNT(*) as total_ventes, SUM(quantite) as total_produits,
                   SUM(quantite * prix_unitaire) as chiffre_affaires
        elif choix == '3':
        elif choix == '4':
        elif choix == '5':
        elif choix == '6':
            break
            print("❌ Choix invalide")
if __name__ == "__main__":
    menu_principal()
        else:
            print("👋 Au revoir!")
            nettoyer_base()
            afficher_ventes_recentes()
            afficher_rapport_stock()
        elif choix == '2':
            inserer_donnees_aleatoires()
        if choix == '1':
            creer_base_de_donnees()
        choix = input("Votre choix: ")
        
            FROM ventes
        print("="*50)
        
        print("5. Nettoyer la base de données")
        print("6. Quitter")
            WHERE date_vente >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """)
        print("3. Afficher le rapport de stock")
        print("4. Afficher les ventes récentes")
        print("1. Créer la base de données")
        print("2. Insérer des données aléatoires")
        
        stats_ventes = cursor.fetchone()
        print("📊 VENTES SUR 7 JOURS:")
        print(f"  📋 Nombre de ventes: {stats_ventes[0]}")
        print(f"  📱 Produits vendus: {stats_ventes[1]}")
        print("🏪 GESTION DE STOCK - BOUTIQUE DE TÉLÉPHONES")
        print("="*50)
        print(f"  💰 Chiffre d'affaires: {stats_ventes[2]:.2f}€")

    while True:
        print("\n" + "="*50)
    """Menu principal interactif"""
def menu_principal():
        
            print(f"❌ Erreur lors du nettoyage: {err}")
        cursor.close()
        except mysql.connector.Error as err:
        conn.close()
            print("✅ Base de données nettoyée")
        
    except mysql.connector.Error as err:
            conn.close()
            conn.commit()
            cursor.close()
        print(f"❌ Erreur lors de l'affichage des ventes: {err}")
            
            cursor.execute("DELETE FROM marques")

            cursor.execute("DELETE FROM telephones")
            
            cursor.execute("DELETE FROM ventes")
            cursor = conn.cursor()
            conn = mysql.connector.connect(**config)

