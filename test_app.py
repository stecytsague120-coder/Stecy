import unittest
import mysql.connector
from datetime import datetime, timedelta
import random
import os
import tempfile

# Import des fonctions de l'application principale
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import (
    creer_base_de_donnees, 
    inserer_donnees_aleatoires,
    afficher_rapport_stock,
    afficher_ventes_recentes,
    config
)

class TestBoutiqueTelephone(unittest.TestCase):
    """Classe de tests pour l'application de gestion de stock"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale avant tous les tests"""
        # Base de données de test
        cls.test_config = config.copy()
        cls.test_config['database'] = 'boutique_telephone_test'
        
        # Connexion de test
        try:
            conn = mysql.connector.connect(
                user=cls.test_config['user'],
                password=cls.test_config['password'],
                host=cls.test_config['host']
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.test_config['database']}")
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(f"Erreur de configuration: {e}")
            raise
    
    def setUp(self):
        """Configuration avant chaque test"""
        # Configuration de la base de données de test
        self.conn = mysql.connector.connect(
            user=self.test_config['user'],
            password=self.test_config['password'],
            host=self.test_config['host'],
            database=self.test_config['database']
        )
        self.cursor = self.conn.cursor()
        
        # Création des tables de test
        self.creer_tables_test()
        
        # Redirection de la config pour utiliser la base de test
        global config
        config.update(self.test_config)
    
    def creer_tables_test(self):
        """Crée les tables pour les tests"""
        # Table des marques
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS marques (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(50) NOT NULL UNIQUE,
                pays_origine VARCHAR(50)
            )
        """)
        
        # Table des téléphones
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS telephones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                marque_id INT,
                modele VARCHAR(100) NOT NULL,
                prix_achat DECIMAL(10,2) NOT NULL,
                prix_vente DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0,
                couleur VARCHAR(30),
                memoire_stockage VARCHAR(20),
        self.cursor.execute("DELETE FROM ventes")
        self.cursor.execute("DELETE FROM marques")
        """Nettoyage après tous les tests"""
                password=cls.test_config['password'],
            )
            cursor.execute(f"DROP DATABASE IF EXISTS {cls.test_config['database']}")
            cursor.close()
            conn.close()
            print(f"Erreur lors du nettoyage: {e}")
class TestCreationBase(TestBoutiqueTelephone):
    """Tests pour la création de la base de données"""
    
    def test_creation_base_donnees(self):
        """Test de création de la base de données"""
        creer_base_de_donnees()
        
        # Vérification que les tables existent
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
        
        self.assertIn('marques', tables)
        self.assertIn('telephones', tables)
        self.assertIn('ventes', tables)
    
    def test_structure_tables(self):
        """Test de la structure des tables"""
        # Créer la base
        creer_base_de_donnees()
        
        self.assertIn('nom', colonnes_marques)
        self.assertIn('pays_origine', colonnes_marques)
        # Vérification de la structure de la table telephones
        self.assertIn('marque_id', colonnes_telephones)
        self.assertIn('prix_achat', colonnes_telephones)
        self.assertIn('prix_vente', colonnes_telephones)

class TestInsertionDonnees(TestBoutiqueTelephone):
    """Tests pour l'insertion des données"""
    
    def test_insertion_marques(self):
        # Insérer des données
        
        # Vérifier que des marques ont été insérées
        self.cursor.execute("SELECT COUNT(*) FROM marques")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)
    
    def test_insertion_telephones(self):
        """Test d'insertion des téléphones"""
        # Insérer des données
        inserer_donnees_aleatoires()
        
        # Vérifier que des téléphones ont été insérés
        self.cursor.execute("SELECT COUNT(*) FROM telephones")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)
    
        inserer_donnees_aleatoires()
        """Test d'insertion des marques"""
    def test_insertion_ventes(self):
        self.assertIn('stock', colonnes_telephones)
        """Test d'insertion des ventes"""
        # Insérer des données
        self.assertIn('modele', colonnes_telephones)
        self.assertIn('id', colonnes_telephones)
        inserer_donnees_aleatoires()
        colonnes_telephones = [col[0] for col in self.cursor.fetchall()]
        self.cursor.execute("DESCRIBE telephones")
        
        
        self.assertIn('id', colonnes_marques)
        # Vérifier que des ventes ont été insérées
        # Vérification de la structure de la table marques
        self.cursor.execute("DESCRIBE marques")
        self.cursor.execute("SELECT COUNT(*) FROM ventes")
        colonnes_marques = [col[0] for col in self.cursor.fetchall()]
        # Création de la base
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)
    

        except mysql.connector.Error as e:
            cursor = conn.cursor()
                host=cls.test_config['host']
    def test_stock_mise_a_jour_apres_vente(self):
        """Test que le stock est mis à jour après une vente"""
            conn = mysql.connector.connect(
                user=cls.test_config['user'],
        try:
    @classmethod
    def tearDownClass(cls):
        self.conn.close()
    
        # Insérer d'abord une marque
        
        self.cursor.close()
        self.conn.commit()
        self.cursor.execute("""
            INSERT INTO marques (nom, pays_origine) 
        self.cursor.execute("DELETE FROM telephones")
        # Suppression des données
        """Nettoyage après chaque test"""
            VALUES ('TestMarque', 'TestPays')
        """)
        self.conn.commit()
        
        # Insérer un téléphone avec stock
        self.cursor.execute("""
            INSERT INTO telephones 
            (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
            VALUES (1, 'TestPhone', 500, 700, 10, 'Noir', '128GB', '8GB', CURDATE())
        """)
        self.conn.commit()
        
        # Vérifier le stock initial
        self.cursor.execute("SELECT stock FROM telephones WHERE id = 1")
        stock_initial = self.cursor.fetchone()[0]
        self.assertEqual(stock_initial, 10)
        
        # Insérer une vente
        self.cursor.execute("""
            INSERT INTO ventes (telephone_id, quantite, prix_unitaire, client_nom, client_email)
            VALUES (1, 3, 700, 'Test Client', 'test@email.com')
        """)
        self.conn.commit()
        
        # Mettre à jour le stock
        self.cursor.execute("""
            UPDATE telephones 
            SET stock = stock - 3 
            WHERE id = 1
        """)
        self.conn.commit()
        
        # Vérifier le stock après la vente
        self.cursor.execute("SELECT stock FROM telephones WHERE id = 1")
        stock_final = self.cursor.fetchone()[0]
        self.assertEqual(stock_final, 7)

class TestRapports(TestBoutiqueTelephone):
    """Tests pour les rapports"""
    
    def setUp(self):
        """Préparer des données de test spécifiques"""
        super().setUp()
        
        # Insérer des données de test
        self.inserer_donnees_test()
    
    def inserer_donnees_test(self):
        """Insertion de données de test contrôlées"""
        # Insérer des marques
        marques = [('Apple', 'États-Unis'), ('Samsung', 'Corée du Sud')]
        for marque, pays in marques:
            self.cursor.execute(
                "INSERT INTO marques (nom, pays_origine) VALUES (%s, %s)",
                (marque, pays)
            )
        self.conn.commit()
        
        # Insérer des téléphones
        telephones = [
            (1, 'iPhone 15', 700, 900, 15, 'Noir', '128GB', '8GB', datetime.now().date()),
            (1, 'iPhone 15 Pro', 900, 1200, 8, 'Or', '256GB', '8GB', datetime.now().date()),
            (2, 'Galaxy S24', 600, 800, 20, 'Bleu', '128GB', '8GB', datetime.now().date()),
            (2, 'Galaxy S24 Ultra', 800, 1100, 5, 'Noir', '512GB', '12GB', datetime.now().date())
        ]
        
        for tel in telephones:
            self.cursor.execute("""
                INSERT INTO telephones 
                (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tel)
        self.conn.commit()
        
        # Insérer des ventes
        ventes = [
            (1, 2, 900, datetime.now() - timedelta(days=1), 'Client 1', 'client1@email.com'),
            (2, 1, 1200, datetime.now() - timedelta(days=2), 'Client 2', 'client2@email.com'),
            (3, 3, 800, datetime.now() - timedelta(hours=5), 'Client 3', 'client3@email.com')
        ]
        
        for vente in ventes:
            self.cursor.execute("""
                INSERT INTO ventes 
                (telephone_id, quantite, prix_unitaire, date_vente, client_nom, client_email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, vente)
        self.conn.commit()
    
    def test_rapport_stock(self):
        """Test de génération du rapport de stock"""
        # Récupérer les données pour le rapport
        self.cursor.execute("""
            SELECT COUNT(*) as total_produits,
                   SUM(stock) as stock_total
            FROM telephones
        """)
        stats = self.cursor.fetchone()
        
        self.assertEqual(stats[0], 4)  # 4 téléphones
        self.assertEqual(stats[1], 48)  # 15 + 8 + 20 + 5 = 48
    
    def test_rapport_par_marque(self):
        """Test du rapport par marque"""
        self.cursor.execute("""
            SELECT m.nom, COUNT(t.id) as total_modele, SUM(t.stock) as stock_total
            FROM marques m
            LEFT JOIN telephones t ON m.id = t.marque_id
            GROUP BY m.id
            ORDER BY stock_total DESC
        """)
        
        resultats = self.cursor.fetchall()
        
        # Vérifier les résultats par marque
        self.assertEqual(len(resultats), 2)
        
        # Samsung devrait avoir plus de stock (25)
        self.assertEqual(resultats[0][0], 'Samsung')
        self.assertEqual(resultats[0][2], 25)  # 20 + 5
        
        # Apple devrait avoir 23
        self.assertEqual(resultats[1][0], 'Apple')
        self.assertEqual(resultats[1][2], 23)  # 15 + 8
    
    def tearDown(self):
    
        self.conn.commit()
                ram VARCHAR(10),
    def test_ventes_recentes(self):
        
        """Test de récupération des ventes récentes"""
        """)
        self.cursor.execute("""
                date_arrivee DATE,
                FOREIGN KEY (marque_id) REFERENCES marques(id)
            SELECT COUNT(*) FROM ventes
            WHERE date_vente >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            )
                FOREIGN KEY (telephone_id) REFERENCES telephones(id)
            )
                client_email VARCHAR(100),
                client_nom VARCHAR(100),
                quantite INT NOT NULL,
                date_vente DATETIME DEFAULT CURRENT_TIMESTAMP,
                prix_unitaire DECIMAL(10,2) NOT NULL,
                telephone_id INT,
        """)
        """)

        count = self.cursor.fetchone()[0]

        self.assertEqual(count, 3)  # 3 ventes dans les 7 derniers jours
    

    def test_chiffre_affaires(self):

        """Test du calcul du chiffre d'affaires"""

        self.cursor.execute("""

            SELECT SUM(quantite * prix_unitaire) as chiffre_affaires
            FROM ventes

        """)
        ca = self.cursor.fetchone()[0]
        

        # Calcul manuel: (2*900) + (1*1200) + (3*800) = 1800 + 1200 + 2400 = 5400
        self.assertEqual(ca, 5400)


class TestValidationDonnees(TestBoutiqueTelephone):
    """Tests de validation des données"""
    

    def test_prix_positifs(self):
        """Test que les prix sont positifs"""
        inserer_donnees_aleatoires()
        
        self.cursor.execute("SELECT prix_achat, prix_vente FROM telephones")
        for prix_achat, prix_vente in self.cursor.fetchall():
            self.assertGreater(prix_achat, 0)
            self.assertGreater(prix_vente, 0)
    
    def test_stock_non_negatif(self):
        """Test que le stock n'est pas négatif"""
        inserer_donnees_aleatoires()
        
        self.cursor.execute("SELECT stock FROM telephones")
        for stock in self.cursor.fetchall():
            self.assertGreaterEqual(stock[0], 0)
    
    def test_prix_vente_superieur_achat(self):
        """Test que le prix de vente est supérieur au prix d'achat"""
        inserer_donnees_aleatoires()
        
        self.cursor.execute("SELECT prix_achat, prix_vente FROM telephones")
        for prix_achat, prix_vente in self.cursor.fetchall():
            self.assertGreater(prix_vente, prix_achat)
    
    def test_contrainte_integrite(self):
        """Test des contraintes d'intégrité référentielle"""
        # Insérer une marque
        self.cursor.execute("""
            INSERT INTO marques (nom, pays_origine) 
            VALUES ('TestMarque', 'TestPays')
        """)
        self.conn.commit()
        
        # Insérer un téléphone avec une marque existante
        self.cursor.execute("""
            INSERT INTO telephones 
            (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
            VALUES (1, 'TestPhone', 500, 700, 10, 'Noir', '128GB', '8GB', CURDATE())
        """)
        self.conn.commit()
        
        # Vérifier que l'insertion a fonctionné
        self.cursor.execute("SELECT COUNT(*) FROM telephones WHERE marque_id = 1")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)

class TestPerformance(TestBoutiqueTelephone):
    """Tests de performance"""
    
    def test_insertion_massive(self):
        """Test d'insertion massive de données"""
        import time
        
        # Mesurer le temps d'insertion
        debut = time.time()
        
        # Insérer 100 marques
        for i in range(100):
            self.cursor.execute(
                "INSERT INTO marques (nom, pays_origine) VALUES (%s, %s)",
                (f'Marque_{i}', f'Pays_{i}')
            )
        self.conn.commit()
        
        # Insérer 1000 téléphones
        for i in range(1000):
            marque_id = random.randint(1, 100)
            self.cursor.execute("""
                INSERT INTO telephones 
                (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                marque_id,
                f'Modele_{i}',
                random.uniform(100, 1000),
                random.uniform(200, 1500),
                random.randint(0, 50),
                random.choice(['Noir', 'Blanc', 'Bleu']),
                random.choice(['64GB', '128GB', '256GB']),
                random.choice(['4GB', '8GB']),
                datetime.now().date()
            ))
        self.conn.commit()
        
        fin = time.time()
        temps_execution = fin - debut
        
        # Vérifier que l'insertion est raisonnable (< 5 secondes)
        self.assertLess(temps_execution, 5.0)
        
        # Vérifier le nombre d'enregistrements
        self.cursor.execute("SELECT COUNT(*) FROM marques")
        count_marques = self.cursor.fetchone()[0]
        self.assertEqual(count_marques, 100)
        
        self.cursor.execute("SELECT COUNT(*) FROM telephones")
        count_telephones = self.cursor.fetchone()[0]
        self.assertEqual(count_telephones, 1000)

class TestExports(TestBoutiqueTelephone):
    """Tests d'export des données"""
    
    def test_export_csv(self):
        """Test d'export des données en CSV"""
        import csv
        import tempfile
        
        # Insérer des données de test
        self.inserer_donnees_test()
        
        # Exporter les données en CSV
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)
            
            # En-têtes
            writer.writerow(['ID', 'Marque', 'Modèle', 'Stock', 'Prix Vente'])
            
            # Données
            self.cursor.execute("""
                SELECT t.id, m.nom, t.modele, t.stock, t.prix_vente
                FROM telephones t
                JOIN marques m ON t.marque_id = m.id
            """)
            
            for row in self.cursor.fetchall():
                writer.writerow(row)
            
            temp_filename = temp_file.name
        
        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(temp_filename))
        
        # Lire le fichier pour vérifier son contenu
        with open(temp_filename, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 5)  # 1 en-tête + 4 lignes
        
        # Nettoyer
        os.unlink(temp_filename)
    
    def inserer_donnees_test(self):
        """Insertion de données de test pour les exports"""
        # Insérer des marques
        self.cursor.execute(
            "INSERT INTO marques (nom, pays_origine) VALUES ('Apple', 'États-Unis')"
        )
        self.conn.commit()
        
        # Insérer des téléphones
        self.cursor.execute("""
            INSERT INTO telephones 
            (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
            VALUES (1, 'iPhone 15', 700, 900, 15, 'Noir', '128GB', '8GB', CURDATE())
        """)
        self.conn.commit()

class TestScenarios(TestBoutiqueTelephone):
    """Tests de scénarios d'utilisation"""
    
    def test_scenario_achat_complet(self):
        """Test d'un scénario complet d'achat"""
        # 1. Insérer un produit
        self.cursor.execute("""
            INSERT INTO marques (nom, pays_origine) 
            VALUES ('TestMarque', 'TestPays')
        """)
        self.conn.commit()
        
        self.cursor.execute("""
            INSERT INTO telephones 
            (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
            VALUES (1, 'TestPhone', 500, 700, 10, 'Noir', '128GB', '8GB', CURDATE())
        """)
        self.conn.commit()
        
        # 2. Vérifier le stock
        self.cursor.execute("SELECT stock FROM telephones WHERE id = 1")
        stock_initial = self.cursor.fetchone()[0]
        self.assertEqual(stock_initial, 10)
        
        # 3. Effectuer une vente
        quantite = 3
        self.cursor.execute("""
            INSERT INTO ventes (telephone_id, quantite, prix_unitaire, client_nom, client_email)
            VALUES (1, %s, 700, 'Client Test', 'test@email.com')
        """, (quantite,))
        self.conn.commit()
        
        # 4. Mettre à jour le stock
        self.cursor.execute("""
            UPDATE telephones 
            SET stock = stock - %s 
            WHERE id = 1
        """, (quantite,))
        self.conn.commit()
        
        # 5. Vérifier que le stock a diminué
        self.cursor.execute("SELECT stock FROM telephones WHERE id = 1")
        stock_final = self.cursor.fetchone()[0]
        self.assertEqual(stock_final, stock_initial - quantite)
        
        # 6. Vérifier que la vente a été enregistrée
        self.cursor.execute("""
            SELECT COUNT(*) FROM ventes 
            WHERE telephone_id = 1 AND quantite = %s
        """, (quantite,))
        count_ventes = self.cursor.fetchone()[0]
        self.assertEqual(count_ventes, 1)
    
    def test_scenario_rupture_stock(self):
        """Test du scénario de rupture de stock"""
        # 1. Insérer un produit avec stock faible
        self.cursor.execute("""
            INSERT INTO marques (nom, pays_origine) 
            VALUES ('TestMarque', 'TestPays')
        """)
        self.conn.commit()
        
        self.cursor.execute("""
            INSERT INTO telephones 
            (marque_id, modele, prix_achat, prix_vente, stock, couleur, memoire_stockage, ram, date_arrivee)
            VALUES (1, 'TestPhone', 500, 700, 2, 'Noir', '128GB', '8GB', CURDATE())
        """)
        self.conn.commit()
        
        # 2. Identifier les produits en rupture de stock
        self.cursor.execute("""
            SELECT COUNT(*) FROM telephones 
            WHERE stock = 0
        """)
        count_rupture_initial = self.cursor.fetchone()[0]
        
        # 3. Vendre tout le stock
        self.cursor.execute("""
            INSERT INTO ventes (telephone_id, quantite, prix_unitaire, client_nom, client_email)
            VALUES (1, 2, 700, 'Client Test', 'test@email.com')
        """)
        self.conn.commit()
        
        self.cursor.execute("""
            UPDATE telephones 
            SET stock = stock - 2 
            WHERE id = 1
        """)
        self.conn.commit()
        
        # 4. Vérifier que le produit est maintenant en rupture
        self.cursor.execute("SELECT stock FROM telephones WHERE id = 1")
        stock_final = self.cursor.fetchone()[0]
        self.assertEqual(stock_final, 0)
        
        # 5. Vérifier qu'il est dans la liste des ruptures
        self.cursor.execute("""
            SELECT COUNT(*) FROM telephones 
            WHERE stock = 0
        """)
        count_rupture_final = self.cursor.fetchone()[0]
        self.assertGreater(count_rupture_final, count_rupture_initial)

# Fonction pour exécuter les tests
def run_tests():
    """Exécute tous les tests"""
    # Configurer les tests
    loader = unittest.TestLoader()

    suite = unittest.TestSuite()

    
    # Ajouter toutes les classes de test

    suite.addTests(loader.loadTestsFromTestCase(TestCreationBase))
    suite.addTests(loader.loadTestsFromTestCase(TestInsertionDonnees))

    suite.addTests(loader.loadTestsFromTestCase(TestRapports))

    suite.addTests(loader.loadTestsFromTestCase(TestValidationDonnees))

    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestExports))

    suite.addTests(loader.loadTestsFromTestCase(TestScenarios))

    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)

    result = runner.run(suite)
    

    return result

if __name__ == '__main__':
    # Exécuter les tests
    print("="*80)
    print("🧪 EXÉCUTION DES TESTS - BOUTIQUE DE TÉLÉPHONES")
    print("="*80)
    
    result = run_tests()
    
    # Afficher le résumé
    print("\n" + "="*80)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*80)
    print(f"✅ Tests réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Échecs: {len(result.failures)}")
    print(f"⚠️ Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 TOUS LES TESTS ONT RÉUSSI!")
    else:
        print("\n❌ DES TESTS ONT ÉCHOUÉ!")
