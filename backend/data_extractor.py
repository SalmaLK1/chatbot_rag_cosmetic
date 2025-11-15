"""
Extraction automatique des données non-structurées (PDF, images, audio)
Transforme les données brutes en données structurées
"""

import PyPDF2
import json
import time
import logging
from typing import List, Dict, Tuple
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)


class DataExtractor:
    """Classe pour extraire les ingrédients des PDF, images et audio"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def extract_from_pdf(self, pdf_path: str) -> Tuple[str, Dict]:
        """
        Extrait le texte et les données structurées d'un PDF
        
        Args:
            pdf_path: Chemin vers le fichier PDF
            
        Returns:
            Tuple[texte_brut, données_structurées]
        """
        try:
            logger.info(f"Extraction du PDF: {pdf_path}")
            text = ""
            
            # Extraction du texte brut
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    text += f"\n--- PAGE {page_num + 1} ---\n{page_text}"
            
            logger.info(f"Texte extrait: {len(text)} caractères")
            return text, {'raw_text': text}
            
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {e}")
            raise
    
    def parse_ingredients_and_products(self, text: str) -> Dict:
        """
        Utilise Gemini pour analyser le texte et extraire les ingrédients/produits
        
        Args:
            text: Texte brut extrait du PDF
            
        Returns:
            Dictionnaire contenant les produits et ingrédients structurés
        """
        try:
            logger.info("Analyse du texte avec Gemini...")
            
            prompt = f"""Vous êtes un expert en analyse de produits cosmétiques et médicaux.
            
Analysez le texte suivant et extrayez les informations dans ce format JSON strict:

{{
    "products": [
        {{
            "name": "Nom du produit",
            "category": "Catégorie (Cosmétique/Médicament/etc)",
            "brand": "Marque",
            "description": "Description brève",
            "ingredients": ["Ingrédient1", "Ingrédient2", ...]
        }}
    ],
    "ingredients_info": [
        {{
            "name": "Nom ingrédient",
            "chemical_name": "Nom chimique si connu",
            "type": "Type (Actif/Conservant/Colorant/etc)",
            "description": "Description"
        }}
    ],
    "incompatibilities": [
        {{
            "ingredient1": "Ingrédient A",
            "ingredient2": "Ingrédient B",
            "risk_level": "HIGH/MEDIUM/LOW",
            "reason": "Raison de l'incompatibilité",
            "consequence": "Conséquences possibles"
        }}
    ]
}}

Texte à analyser:
{text}

Retournez UNIQUEMENT le JSON sans autre texte."""
            
            response = self.model.generate_content(prompt)
            
            # Extraire le JSON de la réponse
            response_text = response.text
            
            # Essayer de trouver le JSON dans la réponse
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                data = json.loads(json_str)
                logger.info(f"Extraction réussie: {len(data.get('products', []))} produits, "
                          f"{len(data.get('ingredients_info', []))} ingrédients")
                return data
            else:
                logger.error("Pas de JSON trouvé dans la réponse Gemini")
                return {'products': [], 'ingredients_info': [], 'incompatibilities': []}
                
        except json.JSONDecodeError as e:
            logger.error(f"Erreur JSON: {e}")
            return {'products': [], 'ingredients_info': [], 'incompatibilities': []}
        except Exception as e:
            logger.error(f"Erreur Gemini: {e}")
            raise
    
    def extract_ingredients_from_image(self, image_path: str) -> Dict:
        """
        Extrait les ingrédients d'une image de produit
        
        Args:
            image_path: Chemin vers l'image
            
        Returns:
            Dictionnaire avec les données extraites
        """
        try:
            logger.info(f"Extraction image: {image_path}")
            
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """Analysez cette image de produit et extraites les informations dans ce format JSON:
{
    "product_name": "Nom du produit",
    "brand": "Marque",
    "ingredients": ["Ingrédient1", "Ingrédient2", ...],
    "warnings": ["Avertissement1", "Avertissement2", ...]
}

Retournez UNIQUEMENT le JSON sans autre texte."""
            
            response = self.model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_data}])
            
            response_text = response.text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                return json.loads(response_text[start_idx:end_idx])
            return {}
            
        except Exception as e:
            logger.error(f"Erreur extraction image: {e}")
            raise
    
    def extract_incompatibilities_from_text(self, text: str) -> List[Dict]:
        """
        Extrait les incompatibilités d'ingrédients du texte
        
        Args:
            text: Texte brut
            
        Returns:
            Liste des incompatibilités trouvées
        """
        try:
            logger.info("Extraction des incompatibilités...")
            
            prompt = f"""Extrayez toutes les incompatibilités entre ingrédients mentionnées dans ce texte.
            
Format JSON requis:
[
    {{
        "ingredient1": "Ingrédient A",
        "ingredient2": "Ingrédient B",
        "risk_level": "CRITICAL/HIGH/MEDIUM/LOW",
        "reason": "Raison scientifique",
        "consequence": "Conséquences possibles",
        "solution": "Alternative ou solution"
    }}
]

Texte:
{text}

Retournez UNIQUEMENT le JSON sans autre texte."""
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                return json.loads(response_text[start_idx:end_idx])
            return []
            
        except Exception as e:
            logger.error(f"Erreur extraction incompatibilités: {e}")
            return []


class DataProcessor:
    """Traite et structure les données extraites dans la BD"""
    
    @staticmethod
    def process_extraction(extracted_data: Dict, db, pdf_path: str) -> Tuple[int, int]:
        """
        Insère les données extraites dans la base de données
        
        Args:
            extracted_data: Données extraites par DataExtractor
            db: Instance SQLAlchemy
            pdf_path: Chemin du fichier source
            
        Returns:
            Tuple[nombre_produits, nombre_ingrédients]
        """
        from .structured_data_models import Product, Ingredient, ProductIngredient, Incompatibility
        
        try:
            products_count = 0
            ingredients_count = 0
            
            # Créer les ingrédients d'abord
            ingredients_map = {}
            for ing_data in extracted_data.get('ingredients_info', []):
                existing = Ingredient.query.filter_by(name=ing_data['name']).first()
                if not existing:
                    ing = Ingredient(
                        name=ing_data['name'],
                        chemical_name=ing_data.get('chemical_name'),
                        ingredient_type=ing_data.get('type'),
                        description=ing_data.get('description')
                    )
                    db.session.add(ing)
                    db.session.flush()
                    ingredients_map[ing_data['name']] = ing
                    ingredients_count += 1
                else:
                    ingredients_map[ing_data['name']] = existing
            
            # Créer les produits et leurs ingrédients
            for prod_data in extracted_data.get('products', []):
                existing_prod = Product.query.filter_by(name=prod_data['name']).first()
                if not existing_prod:
                    prod = Product(
                        name=prod_data['name'],
                        category=prod_data.get('category'),
                        brand=prod_data.get('brand'),
                        description=prod_data.get('description'),
                        source_file=pdf_path,
                        source_type='PDF'
                    )
                    db.session.add(prod)
                    db.session.flush()
                    
                    # Ajouter les ingrédients au produit
                    for ing_name in prod_data.get('ingredients', []):
                        if ing_name in ingredients_map:
                            prod_ing = ProductIngredient(
                                product_id=prod.id,
                                ingredient_id=ingredients_map[ing_name].id
                            )
                            db.session.add(prod_ing)
                    
                    products_count += 1
            
            # Créer les incompatibilités
            for incomp_data in extracted_data.get('incompatibilities', []):
                ing1 = Ingredient.query.filter_by(name=incomp_data['ingredient1']).first()
                ing2 = Ingredient.query.filter_by(name=incomp_data['ingredient2']).first()
                
                if ing1 and ing2:
                    existing_incomp = Incompatibility.query.filter_by(
                        ingredient1_id=ing1.id,
                        ingredient2_id=ing2.id
                    ).first()
                    
                    if not existing_incomp:
                        incomp = Incompatibility(
                            ingredient1_id=ing1.id,
                            ingredient2_id=ing2.id,
                            risk_level=incomp_data.get('risk_level', 'MEDIUM'),
                            reason=incomp_data.get('reason'),
                            consequence=incomp_data.get('consequence'),
                            solution=incomp_data.get('solution'),
                            verified=False
                        )
                        db.session.add(incomp)
            
            db.session.commit()
            logger.info(f"Insertion BD: {products_count} produits, {ingredients_count} ingrédients")
            return products_count, ingredients_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur insertion BD: {e}")
            raise
