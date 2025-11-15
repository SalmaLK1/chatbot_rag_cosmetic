"""
Modèles de données structurées pour les produits et ingrédients
Transforme les données non-structurées (PDF, images, audio) en données structurées
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Importer le db existant des modèles
from .models import db


class Product(db.Model):
    """Modèle pour les produits (cosmétiques, médicaments, etc.)"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=True)  # Cosmétique, Médicament, etc.
    brand = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    source_file = db.Column(db.String(500), nullable=True)  # Fichier PDF/Image d'origine
    source_type = db.Column(db.String(50), nullable=True)  # PDF, IMAGE, AUDIO
    extraction_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    ingredients = db.relationship('ProductIngredient', backref='product', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'brand': self.brand,
            'description': self.description,
            'ingredients': [ing.to_dict() for ing in self.ingredients]
        }


class Ingredient(db.Model):
    """Modèle pour les ingrédients individuels"""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    chemical_name = db.Column(db.String(500), nullable=True)
    ingredient_type = db.Column(db.String(100), nullable=True)  # Actif, Conservant, Colorant, etc.
    properties = db.Column(db.JSON, nullable=True)  # Propriétés JSON
    description = db.Column(db.Text, nullable=True)
    
    # Relations
    products = db.relationship('ProductIngredient', backref='ingredient', cascade='all, delete-orphan')
    incompatibilities = db.relationship('Incompatibility', 
        foreign_keys='Incompatibility.ingredient1_id',
        backref='ingredient1_incomp',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'chemical_name': self.chemical_name,
            'type': self.ingredient_type,
            'description': self.description
        }


class ProductIngredient(db.Model):
    """Relation M2M entre produits et ingrédients avec concentration"""
    __tablename__ = 'product_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    concentration = db.Column(db.Float, nullable=True)  # Pourcentage
    unit = db.Column(db.String(50), nullable=True)  # %, mg/ml, etc.
    extraction_confidence = db.Column(db.Float, default=1.0)  # Confiance de l'extraction (0-1)
    
    __table_args__ = (db.UniqueConstraint('product_id', 'ingredient_id', name='unique_product_ingredient'),)
    
    def __repr__(self):
        return f'<ProductIngredient {self.product_id}-{self.ingredient_id}>'
    
    def to_dict(self):
        return {
            'ingredient': self.ingredient.to_dict(),
            'concentration': self.concentration,
            'unit': self.unit
        }


class Incompatibility(db.Model):
    """Modèle pour les incompatibilités entre ingrédients"""
    __tablename__ = 'incompatibilities'
    
    id = db.Column(db.Integer, primary_key=True)
    ingredient1_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    ingredient2_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    reason = db.Column(db.Text, nullable=True)  # Explication de l'incompatibilité
    consequence = db.Column(db.Text, nullable=True)  # Conséquences possibles
    solution = db.Column(db.Text, nullable=True)  # Solutions/alternatives
    verified = db.Column(db.Boolean, default=False)  # Vérifiée par expert ?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation au second ingrédient
    ingredient2 = db.relationship('Ingredient', foreign_keys=[ingredient2_id])
    
    __table_args__ = (
        db.UniqueConstraint('ingredient1_id', 'ingredient2_id', name='unique_incompatibility'),
        db.Index('idx_ingredient1', 'ingredient1_id'),
        db.Index('idx_ingredient2', 'ingredient2_id'),
    )
    
    def __repr__(self):
        return f'<Incompatibility {self.ingredient1_id}-{self.ingredient2_id}>'
    
    def to_dict(self):
        return {
            'ingredient1': self.ingredient1_incomp[0].to_dict() if self.ingredient1_incomp else None,
            'ingredient2': self.ingredient2.to_dict(),
            'risk_level': self.risk_level,
            'reason': self.reason,
            'consequence': self.consequence,
            'solution': self.solution
        }


class ExtractionLog(db.Model):
    """Traçabilité des extractions de données"""
    __tablename__ = 'extraction_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    source_file = db.Column(db.String(500), nullable=False)
    extraction_type = db.Column(db.String(50), nullable=False)  # PDF, IMAGE, AUDIO
    status = db.Column(db.String(20), nullable=False)  # SUCCESS, PARTIAL, FAILED
    num_products_extracted = db.Column(db.Integer, default=0)
    num_ingredients_extracted = db.Column(db.Integer, default=0)
    extraction_time = db.Column(db.Float, nullable=True)  # Temps en secondes
    error_message = db.Column(db.Text, nullable=True)
    extracted_data = db.Column(db.JSON, nullable=True)  # Données brutes extraites
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExtractionLog {self.source_file} - {self.status}>'


class CompatibilityCache(db.Model):
    """Cache pour les vérifications de compatibilité (optimisation)"""
    __tablename__ = 'compatibility_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    product1_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product2_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    is_compatible = db.Column(db.Boolean, nullable=False)
    incompatibilities_found = db.Column(db.JSON, nullable=True)  # Liste des incompatibilités
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('product1_id', 'product2_id', name='unique_compatibility_check'),
        db.Index('idx_product1', 'product1_id'),
        db.Index('idx_product2', 'product2_id'),
    )
    
    def to_dict(self):
        return {
            'product1_id': self.product1_id,
            'product2_id': self.product2_id,
            'is_compatible': self.is_compatible,
            'incompatibilities': self.incompatibilities_found or []
        }
