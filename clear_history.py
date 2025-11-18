"""
Script pour vider l'historique des conversations de test
"""
import sqlite3
import os

def clear_all_history():
    """Supprime tous les threads et messages de la base de données SQLite"""
    db_path = "chat_history.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données introuvable : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Compter avant suppression
        cursor.execute("SELECT COUNT(*) FROM chat_messages")
        messages_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM chat_threads")
        threads_count = cursor.fetchone()[0]
        
        print(f"📊 Avant suppression : {messages_count} messages, {threads_count} threads")
        
        # Supprimer tous les messages
        cursor.execute("DELETE FROM chat_messages")
        
        # Supprimer tous les threads
        cursor.execute("DELETE FROM chat_threads")
        
        # Commit des changements
        conn.commit()
        
        print(f"✅ Historique supprimé avec succès !")
        print(f"   - {messages_count} messages supprimés")
        print(f"   - {threads_count} threads supprimés")
        
        # Fermer la connexion
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression : {e}")

if __name__ == "__main__":
    print("🗑️  Suppression de l'historique...")
    clear_all_history()
