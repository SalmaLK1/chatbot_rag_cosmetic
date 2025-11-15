"""Diagnostique l'état de la base: chemins, counts, champs manquants.
Usage: python scripts/diagnose_db.py
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, sqldb
from backend.structured_data_models import Product, Ingredient, ProductIngredient, Incompatibility, ExtractionLog, CompatibilityCache

def diagnose():
    with app.app_context():
        uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        engine = sqldb.get_engine()
        db_path = engine.url.database  # chemin relatif (instance/chat_history.db)
        abs_path = os.path.abspath(db_path)
        exists = os.path.exists(abs_path)
        print("URI:", uri)
        print("SQLite path:", db_path)
        print("Absolute path:", abs_path)
        print("Exists:", exists)
        if not exists:
            print("⚠️ Fichier introuvable: vérifiez le dossier 'instance/'")
            return
        print("\n=== COUNTS ===")
        print("Products:", Product.query.count())
        print("Ingredients:", Ingredient.query.count())
        print("ProductIngredients:", ProductIngredient.query.count())
        print("Incompatibilities:", Incompatibility.query.count())
        print("ExtractionLogs:", ExtractionLog.query.count())
        print("CompatibilityCache:", CompatibilityCache.query.count())

        def null_count(model, attr):
            return model.query.filter(getattr(model, attr).is_(None)).count()

        print("\n=== NULL FIELDS SUMMARY ===")
        print("Products.brand NULL:", null_count(Product, 'brand'))
        print("Products.category NULL:", null_count(Product, 'category'))
        print("Products.description NULL:", null_count(Product, 'description'))
        print("Products.source_file NULL:", null_count(Product, 'source_file'))
        print("Ingredients.chemical_name NULL:", null_count(Ingredient, 'chemical_name'))
        print("Ingredients.ingredient_type NULL:", null_count(Ingredient, 'ingredient_type'))
        print("Ingredients.description NULL:", null_count(Ingredient, 'description'))
        print("ProductIngredient.concentration NULL:", null_count(ProductIngredient, 'concentration'))
        print("ProductIngredient.unit NULL:", null_count(ProductIngredient, 'unit'))
        print("Incompatibility.reason NULL:", null_count(Incompatibility, 'reason'))
        print("Incompatibility.consequence NULL:", null_count(Incompatibility, 'consequence'))
        print("Incompatibility.solution NULL:", null_count(Incompatibility, 'solution'))
        print("Incompatibility.verified FALSE:", Incompatibility.query.filter(Incompatibility.verified.is_(False)).count())

        # Exemple de 3 produits
        print("\n=== SAMPLE PRODUCTS ===")
        for p in Product.query.limit(3).all():
            print(f"- {p.name} | brand={p.brand} category={p.category} source_file={p.source_file}")
        print("\n=== SAMPLE INGREDIENTS ===")
        for i in Ingredient.query.limit(5).all():
            print(f"- {i.name} type={i.ingredient_type} chemical={i.chemical_name}")
        print("\n=== SAMPLE INCOMPATIBILITIES ===")
        for inc in Incompatibility.query.limit(3).all():
            ing1 = inc.ingredient1_incomp[0] if inc.ingredient1_incomp else None
            ing2 = inc.ingredient2
            print(f"- {(ing1.name if ing1 else '?')} + {ing2.name} risk={inc.risk_level} verified={inc.verified}")

if __name__ == '__main__':
    diagnose()
