"""
Script pour visualiser les données de la base de données
"""
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from backend.models import db as sqldb, ChatThread, ChatMessage
from backend.structured_data_models import Product, Ingredient, ProductIngredient, Incompatibility, ExtractionLog, CompatibilityCache

def view_chat_data():
    """Afficher les données de chat"""
    print("=" * 80)
    print("📊 DONNÉES DE CHAT")
    print("=" * 80)
    
    threads = ChatThread.query.all()
    print(f"\n📁 Threads de conversation: {len(threads)}")
    for thread in threads[:10]:  # Afficher les 10 premiers
        print(f"  • {thread.title} (ID: {thread.id})")
        print(f"    Créé: {thread.created_at}, Mis à jour: {thread.last_updated}")
    
    messages = ChatMessage.query.all()
    print(f"\n💬 Messages total: {len(messages)}")
    for msg in messages[:5]:  # Afficher les 5 premiers
        print(f"  • {msg.role}: {msg.message[:50]}...")

def view_cosmetics_data():
    """Afficher les données cosmétiques"""
    print("\n" + "=" * 80)
    print("🧴 DONNÉES COSMÉTIQUES (Ingrédients et Incompatibilités)")
    print("=" * 80)
    
    # Produits
    products = Product.query.all()
    print(f"\n📦 Produits: {len(products)}")
    for prod in products:
        print(f"  • {prod.name}")
        print(f"    Type: {prod.product_type}, Marque: {prod.brand or 'N/A'}")
        # Afficher les ingrédients liés
        prod_ingredients = ProductIngredient.query.filter_by(product_id=prod.id).all()
        if prod_ingredients:
            ing_names = []
            for pi in prod_ingredients[:5]:  # Max 5 ingrédients
                ing = Ingredient.query.get(pi.ingredient_id)
                if ing:
                    ing_names.append(ing.name)
            print(f"    Ingrédients: {', '.join(ing_names)}{'...' if len(prod_ingredients) > 5 else ''}")
    
    # Ingrédients
    ingredients = Ingredient.query.all()
    print(f"\n🧪 Ingrédients: {len(ingredients)}")
    for ing in ingredients[:20]:  # Afficher les 20 premiers
        print(f"  • {ing.name} ({ing.ingredient_type or 'Type non spécifié'})")
        if ing.description:
            print(f"    {ing.description[:60]}...")
    
    # Incompatibilités
    incompatibilities = Incompatibility.query.all()
    print(f"\n⚠️  Incompatibilités: {len(incompatibilities)}")
    for incomp in incompatibilities:
        ing1 = Ingredient.query.get(incomp.ingredient1_id)
        ing2 = Ingredient.query.get(incomp.ingredient2_id)
        if ing1 and ing2:
            risk_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(incomp.risk_level, '⚪')
            print(f"  {risk_emoji} {ing1.name} × {ing2.name}")
            print(f"    Niveau: {incomp.risk_level}, Raison: {incomp.reason[:60]}...")
    
    # Logs d'extraction
    logs = ExtractionLog.query.all()
    print(f"\n📝 Logs d'extraction: {len(logs)}")
    for log in logs[-5:]:  # Afficher les 5 derniers
        print(f"  • Source: {log.source_file}")
        print(f"    Statut: {log.status}, {log.num_products_extracted} produits, {log.num_ingredients_extracted} ingrédients")
        print(f"    Date: {log.created_at}")
    
    # Cache de compatibilité
    cache_entries = CompatibilityCache.query.all()
    print(f"\n💾 Entrées de cache: {len(cache_entries)}")
    for entry in cache_entries[-5:]:  # Afficher les 5 derniers
        print(f"  • Produits: {entry.product1_id} × {entry.product2_id}")
        print(f"    Compatible: {entry.is_compatible}, Créé: {entry.created_at}")

def main():
    """Fonction principale"""
    with app.app_context():
        print("\n🔍 VISUALISATION DE LA BASE DE DONNÉES\n")
        
        # Données de chat
        view_chat_data()
        
        # Données cosmétiques
        view_cosmetics_data()
        
        print("\n" + "=" * 80)
        print("✅ Visualisation terminée")
        print("=" * 80)

if __name__ == "__main__":
    main()
