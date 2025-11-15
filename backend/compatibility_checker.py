"""
Système de vérification de compatibilité des ingrédients et produits
Répond aux questions comme "Puis-je utiliser le produit A avec le produit B ?"
"""

import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import google.generativeai as genai

logger = logging.getLogger(__name__)


class CompatibilityChecker:
    """Vérifie la compatibilité entre ingrédients et produits"""
    
    RISK_LEVELS = {
        'CRITICAL': {'score': 4, 'emoji': '🔴', 'label': 'Critique'},
        'HIGH': {'score': 3, 'emoji': '🟠', 'label': 'Élevé'},
        'MEDIUM': {'score': 2, 'emoji': '🟡', 'label': 'Moyen'},
        'LOW': {'score': 1, 'emoji': '🟢', 'label': 'Faible'},
        'UNKNOWN': {'score': 0, 'emoji': '⚪', 'label': 'Inconnu'}
    }
    
    def __init__(self, db=None, api_key: str = None):
        self.db = db
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def check_products_compatibility(self, product1_id: int, product2_id: int) -> Dict:
        """
        Vérifie la compatibilité entre deux produits
        
        Args:
            product1_id: ID du premier produit
            product2_id: ID du second produit
            
        Returns:
            Dictionnaire avec résultats de compatibilité
        """
        from .structured_data_models import (
            Product, Incompatibility, CompatibilityCache
        )
        
        try:
            # Vérifier le cache d'abord
            cache = CompatibilityCache.query.filter_by(
                product1_id=product1_id,
                product2_id=product2_id
            ).first()
            
            if cache:
                # Cache valide si < 7 jours
                if datetime.utcnow() - cache.checked_at < timedelta(days=7):
                    logger.info(f"Cache hit pour {product1_id}-{product2_id}")
                    return cache.to_dict()
            
            # Récupérer les produits
            product1 = Product.query.get(product1_id)
            product2 = Product.query.get(product2_id)
            
            if not product1 or not product2:
                return {'error': 'Produit non trouvé'}
            
            # Récupérer tous les ingrédients des deux produits
            ingredients1 = set(ing.ingredient_id for ing in product1.ingredients)
            ingredients2 = set(ing.ingredient_id for ing in product2.ingredients)
            
            # Chercher les incompatibilités
            incompatibilities = []
            max_risk_score = 0
            
            for ing1_id in ingredients1:
                for ing2_id in ingredients2:
                    # Vérifier dans les deux sens
                    incomp = Incompatibility.query.filter(
                        ((Incompatibility.ingredient1_id == ing1_id) & 
                         (Incompatibility.ingredient2_id == ing2_id)) |
                        ((Incompatibility.ingredient1_id == ing2_id) & 
                         (Incompatibility.ingredient2_id == ing1_id))
                    ).first()
                    
                    if incomp:
                        risk_score = self.RISK_LEVELS.get(
                            incomp.risk_level, 
                            self.RISK_LEVELS['UNKNOWN']
                        )['score']
                        max_risk_score = max(max_risk_score, risk_score)
                        
                        incompatibilities.append({
                            'ingredient1': incomp.ingredient1_incomp[0].name if incomp.ingredient1_incomp else None,
                            'ingredient2': incomp.ingredient2.name,
                            'risk_level': incomp.risk_level,
                            'reason': incomp.reason,
                            'consequence': incomp.consequence,
                            'solution': incomp.solution
                        })
            
            is_compatible = len(incompatibilities) == 0 or max_risk_score <= 1
            
            # Mettre en cache
            cache_entry = CompatibilityCache(
                product1_id=product1_id,
                product2_id=product2_id,
                is_compatible=is_compatible,
                incompatibilities_found=incompatibilities
            )
            self.db.session.add(cache_entry)
            self.db.session.commit()
            
            return {
                'product1': product1.to_dict(),
                'product2': product2.to_dict(),
                'is_compatible': is_compatible,
                'incompatibilities': incompatibilities,
                'risk_score': max_risk_score,
                'summary': self._generate_summary(
                    product1.name, 
                    product2.name, 
                    is_compatible, 
                    incompatibilities
                )
            }
            
        except Exception as e:
            logger.error(f"Erreur vérification compatibilité: {e}")
            return {'error': str(e)}
    
    def check_ingredients_compatibility(self, ingredient1_id: int, ingredient2_id: int) -> Dict:
        """
        Vérifie la compatibilité entre deux ingrédients spécifiques
        
        Args:
            ingredient1_id: ID du premier ingrédient
            ingredient2_id: ID du second ingrédient
            
        Returns:
            Dictionnaire avec résultats
        """
        from .structured_data_models import Ingredient, Incompatibility
        
        try:
            ing1 = Ingredient.query.get(ingredient1_id)
            ing2 = Ingredient.query.get(ingredient2_id)
            
            if not ing1 or not ing2:
                return {'error': 'Ingrédient non trouvé'}
            
            incomp = Incompatibility.query.filter(
                ((Incompatibility.ingredient1_id == ingredient1_id) & 
                 (Incompatibility.ingredient2_id == ingredient2_id)) |
                ((Incompatibility.ingredient1_id == ingredient2_id) & 
                 (Incompatibility.ingredient2_id == ingredient1_id))
            ).first()
            
            if incomp:
                return {
                    'ingredient1': ing1.to_dict(),
                    'ingredient2': ing2.to_dict(),
                    'is_compatible': False,
                    'risk_level': incomp.risk_level,
                    'reason': incomp.reason,
                    'consequence': incomp.consequence,
                    'solution': incomp.solution,
                    'emoji': self.RISK_LEVELS.get(incomp.risk_level, {}).get('emoji', '⚪')
                }
            else:
                return {
                    'ingredient1': ing1.to_dict(),
                    'ingredient2': ing2.to_dict(),
                    'is_compatible': True,
                    'risk_level': 'UNKNOWN',
                    'reason': 'Aucune incompatibilité connue',
                    'emoji': '🟢'
                }
            
        except Exception as e:
            logger.error(f"Erreur vérification ingrédients: {e}")
            return {'error': str(e)}
    
    def get_product_incompatibilities(self, product_id: int) -> Dict:
        """
        Récupère tous les ingrédients incompatibles avec un produit
        
        Args:
            product_id: ID du produit
            
        Returns:
            Dictionnaire avec incompatibilités
        """
        from .structured_data_models import Product, Incompatibility
        
        try:
            product = Product.query.get(product_id)
            if not product:
                return {'error': 'Produit non trouvé'}
            
            ingredient_ids = set(ing.ingredient_id for ing in product.ingredients)
            
            incomp_ingredients = {}
            for ing_id in ingredient_ids:
                incomp_list = Incompatibility.query.filter(
                    (Incompatibility.ingredient1_id == ing_id) |
                    (Incompatibility.ingredient2_id == ing_id)
                ).all()
                
                for incomp in incomp_list:
                    other_ing_id = (incomp.ingredient2_id 
                                   if incomp.ingredient1_id == ing_id 
                                   else incomp.ingredient1_id)
                    
                    if other_ing_id not in incomp_ingredients:
                        incomp_ingredients[other_ing_id] = []
                    
                    incomp_ingredients[other_ing_id].append(incomp)
            
            return {
                'product': product.to_dict(),
                'incompatible_ingredients': incomp_ingredients,
                'total_incompatibilities': len(incomp_ingredients)
            }
            
        except Exception as e:
            logger.error(f"Erreur récupération incompatibilités: {e}")
            return {'error': str(e)}
    
    def _generate_summary(self, product1: str, product2: str, 
                         is_compatible: bool, incompatibilities: List[Dict]) -> str:
        """Génère un résumé textuel de la compatibilité"""
        if is_compatible:
            return f"✅ {product1} et {product2} sont compatibles !"
        
        if not incompatibilities:
            return f"❓ Aucune information de compatibilité trouvée entre {product1} et {product2}"
        
        risks = {}
        for incomp in incompatibilities:
            risk = incomp['risk_level']
            if risk not in risks:
                risks[risk] = []
            risks[risk].append(f"{incomp['ingredient1']} + {incomp['ingredient2']}")
        
        summary = f"⚠️ **{product1} et {product2} peuvent présenter des incompatibilités :**\n\n"
        
        for risk_level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if risk_level in risks:
                emoji = self.RISK_LEVELS[risk_level]['emoji']
                label = self.RISK_LEVELS[risk_level]['label']
                summary += f"{emoji} **Risque {label}:**\n"
                for pair in risks[risk_level][:3]:  # Max 3 par niveau
                    summary += f"  • {pair}\n"
        
        return summary
    
    def ask_gemini_compatibility(self, user_question: str, 
                                context_products: List[str] = None) -> str:
        """
        Demande à Gemini de répondre une question de compatibilité
        
        Args:
            user_question: Question de l'utilisateur
            context_products: Liste des produits pertinents
            
        Returns:
            Réponse texte structurée
        """
        if not self.model:
            return "Modèle Gemini non configuré"
        
        try:
            context = ""
            if context_products:
                context = f"\nProduits mentionnés: {', '.join(context_products)}\n"
            
            prompt = f"""Vous êtes un expert en compatibilité de produits cosmétiques et médicaux.

{context}

Répondez à cette question sur la compatibilité:
{user_question}

Fournissez une réponse claire, structurée et basée sur les données disponibles."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Erreur Gemini: {e}")
            return f"Erreur lors de la requête: {e}"
