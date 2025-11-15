from flask import Flask, render_template, request, jsonify, send_file
import os
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv

# Charger automatiquement les variables d'environnement depuis un fichier .env (si présent)
load_dotenv()

# Import des modules backend personnalisés
from backend.backendtow import (
    process_question,
    handle_uploaded_file,
    handle_multiple_uploaded_files,
    rag_fusion_multi_docs,
    load_faiss_index,
    add_document_to_index,
    generate_export_file,
    embeddings,
)
from backend.models import db as sqldb, ChatThread, ChatMessage
from backend.chat_service import handle_question, get_chat_history, generate_title_from_message
from backend.structured_data_models import Product, Ingredient, Incompatibility
from backend.compatibility_checker import CompatibilityChecker
from backend.data_extractor import DataExtractor, DataProcessor
from langchain_community.vectorstores import FAISS
from backend.config import INDEX_PATH, AUTO_PERSIST_STRUCTURED
import re

# ==============================
# INITIALISATION DE L'APPLICATION FLASK
# ==============================

def create_app():
    """Factory function pour créer l'application Flask"""
    app = Flask(__name__)

    # Configuration de l'application
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Dossier pour les fichiers uploadés
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'  # Base SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive le tracking des modifications

    # Création du dossier d'upload s'il n'existe pas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialisation de la base de données avec l'application Flask
    sqldb.init_app(app)
    
    return app

app = create_app()

# Configuration du système de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================
# CONFIGURATION ADMIN ET SÉCURITÉ
# ==============================

# Token d'administration - en production utiliser variables d'environnement
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "mon_token_secret")

# Verrou pour les opérations sur l'index FAISS (évite les accès concurrents)
index_lock = threading.Lock()

def check_admin_auth():
    """
    Vérifie l'authentification admin via token Bearer.
    
    Returns:
        bool: True si authentifié, False sinon
    """
    token = request.headers.get("Authorization", "")
    return token == f"Bearer {ADMIN_TOKEN}"

# ==============================
# FONCTIONS UTILITAIRES
# ==============================

def create_thread_if_not_exists(user_id, thread_id):
    """
    Crée un thread de conversation s'il n'existe pas déjà.
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        thread_id (str): Identifiant du thread
    
    Returns:
        ChatThread: Thread existant ou nouvellement créé
    """
    thread = ChatThread.query.filter_by(id=thread_id).first()
    if not thread:
        new_thread = ChatThread(
            id=thread_id,
            user_id=user_id,
            title="Nouvelle conversation",
            created_at=datetime.utcnow()
        )
        sqldb.session.add(new_thread)
        sqldb.session.commit()
        return new_thread
    return thread

# ==============================
# ROUTES PRINCIPALES DE L'APPLICATION
# ==============================

@app.route("/")
def index():
    """
    Route racine - sert l'interface chat principale.
    
    Returns:
        Response: Page HTML du chat
    """
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    # FAISS index is loaded at startup via backend.backendtow.load_faiss_index()
    """
    Point d'entrée principal pour les questions et uploads de fichiers.
    Gère à la fois le RAG et le mode conversation simple.
    
    Returns:
        JSON: Réponse de l'assistant avec contexte
    """
    try:
        # Extraction des paramètres de la requête
        question = request.form.get("question", "").strip()
        use_rag = request.form.get("use_rag", "true").lower() == "true"
        session_id = request.form.get("session_id")
        user_id = request.form.get("user_id") or "anonymous"
        thread_id = request.form.get("thread_id")
        nb_messages = int(request.form.get("nb_messages", "3"))

        # Validation des paramètres requis
        if not session_id:
            return jsonify({"error": "session_id manquant"}), 400
        
        # Génération d'un thread_id si non fourni
        if not thread_id:
            thread_id = 'thread_' + os.urandom(8).hex()

        # Création du thread si nécessaire
        thread = create_thread_if_not_exists(user_id, thread_id)
        
        # Récupération des fichiers uploadés
        files = request.files.getlist("file")
        
        # Validation qu'il y a au moins une question ou des fichiers
        if not question and not files:
            return jsonify({"error": "Aucune question ni fichier reçu."}), 400

        logging.info(f"/ask reçu - user_id:{user_id} session_id:{session_id} thread_id:{thread_id}")

        # Initialisation des variables de réponse
        user_msg = question if question else ""
        answer = ""
        context = []

        # Section critique protégée par verrou (accès à l'index FAISS)
        with index_lock:
            if files:
                # Traitement avec fichiers uploadés
                answer = handle_multiple_uploaded_files(
                    files,
                    question=question,
                    chat_history=get_chat_history(user_id, session_id, thread_id, nb_messages),
                    use_rag=use_rag,
                    nb_messages=nb_messages
                )
                # Enrichissement du message utilisateur avec les noms de fichiers
                if question:
                    user_msg += " (Fichiers : " + ", ".join([f.filename for f in files]) + ")"
            else:
                # Traitement question seule
                chat_history = get_chat_history(user_id, session_id, thread_id, nb_messages)
                if use_rag:
                    # Mode RAG avec recherche documentaire
                    answer, context = rag_fusion_multi_docs(
                        query=question,
                        chat_history=chat_history,
                        nb_messages=nb_messages
                    )
                else:
                    # Mode conversation simple
                    answer = process_question(
                        question,
                        use_rag=False,
                        chat_history=chat_history,
                        nb_messages=nb_messages
                    )
                    context = []

        # Sauvegarde de l'échange en base de données
        handle_question(user_id, session_id, thread_id, user_msg, answer)

        # Mise à jour du titre du thread si c'est une nouvelle conversation
        if thread and (not thread.title or thread.title == "Nouvelle conversation"):
            thread.title = generate_title_from_message(user_msg)
            thread.created_at = thread.created_at or datetime.utcnow()
            sqldb.session.commit()

        # Sérialisation du contexte pour la réponse JSON
        context_serializable = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in context]

        return jsonify({
            "answer": answer,
            "context": context_serializable,
            "session_id": session_id,
            "thread_id": thread_id
        })

    except Exception as e:
        logging.error(f"Erreur serveur /ask : {e}", exc_info=True)
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@app.route("/export", methods=["POST"])
def export():
    """
    Exporte une conversation dans différents formats (TXT, DOCX, PDF).
    
    Returns:
        File: Fichier d'export à télécharger
    """
    try:
        data = request.get_json()
        # Validation des données requises
        if not data or "answer" not in data or "context" not in data or "format" not in data:
            return jsonify({"error": "Données incomplètes pour l'export."}), 400
        
        # Génération du fichier d'export
        file_path = generate_export_file(data, format=data["format"])
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        logging.error(f"Erreur export fichier : {e}", exc_info=True)
        return jsonify({"error": f"Erreur export : {str(e)}"}), 500

@app.route("/history", methods=["GET"])
def history():
    """
    Récupère l'historique complet d'un thread de conversation.
    
    Returns:
        JSON: Liste des messages du thread
    """
    session_id = request.args.get("session_id", "default")
    user_id = request.args.get("user_id", "anonymous")
    thread_id = request.args.get("thread_id")
    
    if not thread_id:
        return jsonify({"error": "thread_id manquant"}), 400
        
    try:
        messages = get_chat_history(user_id, session_id, thread_id, nb_messages=100)
        # Transformation en format linéaire pour l'affichage
        result = []
        for m in messages:
            result.append({"role": "user", "message": m['user']})
            result.append({"role": "assistant", "message": m['assistant']})
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Erreur récupération historique complet : {e}", exc_info=True)
        return jsonify({"error": "Erreur récupération historique"}), 500

@app.route("/chats", methods=["GET"])
def list_chats():
    """
    Liste tous les threads de conversation d'un utilisateur.
    
    Returns:
        JSON: Liste des threads avec métadonnées
    """
    user_id = request.args.get("user_id", "anonymous")
    try:
        threads = ChatThread.query.filter_by(user_id=user_id).order_by(ChatThread.created_at.desc()).all()
        return jsonify([t.to_dict() for t in threads])
    except Exception as e:
        logging.error(f"Erreur récupération des threads : {e}", exc_info=True)
        return jsonify({"error": "Erreur récupération des discussions"}), 500

@app.route("/threads", methods=["POST"])
def create_thread():
    """
    Crée un nouveau thread de conversation.
    
    Returns:
        JSON: Détails du thread créé
    """
    data = request.get_json() or {}
    user_id = data.get("user_id", "anonymous")
    thread_id = 'thread_' + os.urandom(8).hex()
    try:
        new_thread = ChatThread(
            id=thread_id, 
            user_id=user_id, 
            title="Nouvelle conversation", 
            created_at=datetime.utcnow()
        )
        sqldb.session.add(new_thread)
        sqldb.session.commit()
        return jsonify(new_thread.to_dict())
    except Exception as e:
        logging.error(f"Erreur création thread : {e}", exc_info=True)
        return jsonify({"error": "Impossible de créer une nouvelle conversation."}), 500

@app.route("/threads/<thread_id>", methods=["PUT"])
def rename_thread(thread_id):
    """
    Renomme un thread existant.
    
    Args:
        thread_id (str): Identifiant du thread à renommer
    
    Returns:
        JSON: Confirmation de la mise à jour
    """
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Titre manquant"}), 400
        
    new_title = data["title"].strip()
    if not new_title:
        return jsonify({"error": "Titre vide"}), 400
        
    thread = ChatThread.query.filter_by(id=thread_id).first()
    if not thread:
        return jsonify({"error": "Thread introuvable"}), 404
        
    thread.title = new_title
    sqldb.session.commit()
    return jsonify({"message": "Titre mis à jour"})

@app.route("/threads/<thread_id>", methods=["DELETE"])
def delete_thread(thread_id):
    """
    Supprime un thread et tous ses messages.
    
    Args:
        thread_id (str): Identifiant du thread à supprimer
    
    Returns:
        JSON: Confirmation de la suppression
    """
    thread = ChatThread.query.filter_by(id=thread_id).first()
    if not thread:
        return jsonify({"error": "Thread introuvable"}), 404
        
    try:
        # Suppression en cascade des messages puis du thread
        ChatMessage.query.filter_by(thread_id=thread_id).delete()
        sqldb.session.delete(thread)
        sqldb.session.commit()
        return jsonify({"message": "Thread supprimé"})
    except Exception as e:
        sqldb.session.rollback()
        logging.error(f"Erreur suppression thread : {e}", exc_info=True)
        return jsonify({"error": f"Erreur lors de la suppression: {str(e)}"}), 500

# ==============================
# ROUTES COMPATIBILITÉ INGRÉDIENTS
# ==============================

@app.route("/compatibility/check_pdf", methods=["POST"])
def check_pdf_compatibility():
    """
    Vérifie les incompatibilités à partir d'un PDF sans nécessiter d'enregistrement BD.
    - Champ fichier: form-data key "file" (PDF)
    - Champs optionnels (form-data):
        - product1: Nom du produit 1 (optionnel)
        - product2: Nom du produit 2 (optionnel)
        - persist: true/false (enregistrer les données structurées en BD)

    Returns:
        JSON avec produits extraits, incompatibilités détectées et résumé éventuel.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "Aucun fichier PDF fourni (clé form-data 'file')"}), 400

        upload = request.files["file"]
        if not upload.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Le fichier doit être un PDF"}), 400

        product1_name = (request.form.get("product1") or "").strip()
        product2_name = (request.form.get("product2") or "").strip()
        default_persist = "true" if AUTO_PERSIST_STRUCTURED else "false"
        persist = (request.form.get("persist", default_persist).lower() == "true")

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"tmp_{os.urandom(6).hex()}.pdf")
        upload.save(temp_path)

        api_key = os.getenv('GOOGLE_API_KEY')
        extractor = DataExtractor(api_key)

        raw_text, _ = extractor.extract_from_pdf(temp_path)
        structured = extractor.parse_ingredients_and_products(raw_text)

        # Optionnel: persister en base pour réutilisation (déduplication)
        persisted = False
        if persist:
            try:
                DataProcessor.process_extraction(structured, sqldb, temp_path)
                persisted = True
            except Exception as e:
                # On ne bloque pas la réponse si la persistance échoue
                app.logger.warning(f"Persistance BD échouée: {e}")

        # Utilitaires locaux
        def norm(s: str) -> str:
            return (s or "").strip().lower()

        def find_product_by_name(name: str, products: list):
            n = norm(name)
            for p in products:
                if norm(p.get("name")) == n:
                    return p
            # fallback: recherche partielle
            for p in products:
                if n and n in norm(p.get("name", "")):
                    return p
            return None

        products = structured.get("products", [])
        incompatibilities = structured.get("incompatibilities", [])

        response = {
            "persisted": persisted,
            "extracted": {
                "products": products,
                "ingredients_info": structured.get("ingredients_info", []),
                "incompatibilities": incompatibilities,
            }
        }

        # Si deux produits sont fournis, calculer un résumé ciblé (stateless)
        if product1_name and product2_name and products:
            p1 = find_product_by_name(product1_name, products)
            p2 = find_product_by_name(product2_name, products)

            if not p1 or not p2:
                response["summary"] = {
                    "found": False,
                    "message": "Produits non trouvés dans le PDF fourni.",
                }
            else:
                ing1 = set(map(norm, p1.get("ingredients", [])))
                ing2 = set(map(norm, p2.get("ingredients", [])))

                found_conflicts = []
                for inc in incompatibilities:
                    a = norm(inc.get("ingredient1"))
                    b = norm(inc.get("ingredient2"))
                    if (a in ing1 and b in ing2) or (a in ing2 and b in ing1):
                        found_conflicts.append(inc)

                if found_conflicts:
                    # Préparer un résumé lisible
                    levels = {"CRITICAL": "🔴 Critique", "HIGH": "🟠 Élevé", "MEDIUM": "🟡 Moyen", "LOW": "🟢 Faible"}
                    lines = []
                    for c in found_conflicts:
                        lvl = levels.get((c.get("risk_level") or "").upper(), c.get("risk_level") or "Inconnu")
                        lines.append(
                            f"- {c.get('ingredient1')} + {c.get('ingredient2')} → {lvl}\n  Raison: {c.get('reason') or 'non spécifiée'}"
                        )
                    response["summary"] = {
                        "found": True,
                        "is_compatible": False,
                        "conflicts_count": len(found_conflicts),
                        "text": "\n".join(lines)
                    }
                else:
                    response["summary"] = {
                        "found": True,
                        "is_compatible": True,
                        "conflicts_count": 0,
                        "text": "Aucune incompatibilité trouvée entre ces deux produits dans ce PDF."
                    }

        try:
            os.remove(temp_path)
        except Exception:
            pass

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Erreur check_pdf_compatibility: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/compatibility/products", methods=["POST"])
def check_products_compatibility():
    """
    Vérifie la compatibilité entre deux produits.
    
    JSON: {
        "product1_id": int,
        "product2_id": int
    }
    
    Returns:
        JSON: Résultat de compatibilité
    """
    try:
        data = request.get_json()
        product1_id = data.get("product1_id")
        product2_id = data.get("product2_id")
        
        if not product1_id or not product2_id:
            return jsonify({"error": "product1_id et product2_id requis"}), 400
        
        api_key = os.getenv('GOOGLE_API_KEY')
        checker = CompatibilityChecker(sqldb, api_key)
        
        result = checker.check_products_compatibility(product1_id, product2_id)
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Erreur vérification compatibilité produits: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/compatibility/ingredients", methods=["POST"])
def check_ingredients_compatibility():
    """
    Vérifie la compatibilité entre deux ingrédients.
    
    JSON: {
        "ingredient1_id": int,
        "ingredient2_id": int
    }
    
    Returns:
        JSON: Résultat de compatibilité
    """
    try:
        data = request.get_json()
        ingredient1_id = data.get("ingredient1_id")
        ingredient2_id = data.get("ingredient2_id")
        
        if not ingredient1_id or not ingredient2_id:
            return jsonify({"error": "ingredient1_id et ingredient2_id requis"}), 400
        
        api_key = os.getenv('GOOGLE_API_KEY')
        checker = CompatibilityChecker(sqldb, api_key)
        
        result = checker.check_ingredients_compatibility(ingredient1_id, ingredient2_id)
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Erreur vérification compatibilité ingrédients: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/compatibility/product/<int:product_id>", methods=["GET"])
def get_product_incompatibilities(product_id):
    """
    Récupère tous les ingrédients incompatibles avec un produit.
    
    Returns:
        JSON: Incompatibilités du produit
    """
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        checker = CompatibilityChecker(sqldb, api_key)
        
        result = checker.get_product_incompatibilities(product_id)
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Erreur récupération incompatibilités: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/compatibility/ask", methods=["POST"])
def ask_compatibility():
    """
    Pose une question sur la compatibilité à Gemini.
    
    JSON: {
        "question": "Puis-je utiliser le produit A avec le produit B ?",
        "products": ["Product A", "Product B"]  # optionnel
    }
    
    Returns:
        JSON: Réponse texte de Gemini
    """
    try:
        data = request.get_json()
        question = data.get("question", "").strip()
        products = data.get("products", [])
        
        if not question:
            return jsonify({"error": "question requise"}), 400
        
        api_key = os.getenv('GOOGLE_API_KEY')
        checker = CompatibilityChecker(sqldb, api_key)
        
        response = checker.ask_gemini_compatibility(question, products)
        return jsonify({"response": response})
        
    except Exception as e:
        logging.error(f"Erreur question compatibilité: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/compatibility/from_text", methods=["POST"])
def compatibility_from_text():
    """Analyse la compatibilité de deux produits fournis en texte brut ou structure JSON.

    Formats acceptés:
    1. JSON direct:
       {
         "product1": {"name": "Masque", "ingredients": ["Argile Verte", "Charbon Actif"]},
         "product2": {"name": "Sérum", "ingredients": ["Acide Hyaluronique", "Glycérine"]},
         "persist": true
       }
    2. Texte brut (clé raw_text) avec motifs:
       "Produit 1 : Masque Purifiant ... contient Argile Verte, Charbon Actif, Huile d’Arbre à Thé. Produit 2 : Sérum Hydratant ... contient Acide Hyaluronique, Glycérine, Vitamine B5, Extrait de Concombre."

    Retourne un résumé de compatibilité basé sur:
      - Incompatibilités connues en base (table incompatibilities)
      - Heuristiques simples (irritation cumulative: acides forts + agents asséchants, etc.)
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        persist = bool(data.get("persist"))

        def normalize_ing(name: str) -> str:
            return (name or "").strip().lower()

        product1 = data.get("product1")
        product2 = data.get("product2")

        raw_text = data.get("raw_text")
        # Extraction heuristique si raw_text présent et produits absents
        if raw_text and (not product1 or not product2):
            # Chercher blocs Produit 1 / Produit 2
            p1_match = re.search(r"Produit\s*1\s*:(.+?)(Produit\s*2\s*:|$)", raw_text, re.IGNORECASE | re.DOTALL)
            p2_match = re.search(r"Produit\s*2\s*:(.+)$", raw_text, re.IGNORECASE | re.DOTALL)
            def extract_block(match):
                if not match: return None
                return match.group(1).strip()
            block1 = extract_block(p1_match)
            block2 = extract_block(p2_match)

            def parse_block(block):
                if not block: return None
                # Nom avant "contient" si présent
                name_part = block.split("contient",1)[0].strip()
                # Ingrédients listés après "contient"
                ing_part = block.split("contient",1)[1].strip() if "contient" in block else ""
                # Séparer par virgules
                ingredients = [i.strip() for i in re.split(r",|;", ing_part) if i.strip()]
                return {"name": name_part[:120], "ingredients": ingredients}
            if block1 and not product1:
                product1 = parse_block(block1)
            if block2 and not product2:
                product2 = parse_block(block2)

        if not product1 or not product2:
            return jsonify({"error": "Produits incomplets ou introuvables dans les données fournies."}), 400

        ing_list_1 = product1.get("ingredients", [])
        ing_list_2 = product2.get("ingredients", [])
        if not ing_list_1 or not ing_list_2:
            return jsonify({"error": "Listes d'ingrédients manquantes pour au moins un produit."}), 400

        # Construire sets normalisés
        set1 = {normalize_ing(i) for i in ing_list_1}
        set2 = {normalize_ing(i) for i in ing_list_2}

        # Récupérer incompatibilités base
        conflicts_db = []
        for incomp in Incompatibility.query.all():
            ing1_obj = Ingredient.query.get(incomp.ingredient1_id)
            ing2_obj = Ingredient.query.get(incomp.ingredient2_id)
            if not ing1_obj or not ing2_obj:
                continue
            n1 = normalize_ing(ing1_obj.name)
            n2 = normalize_ing(ing2_obj.name)
            if (n1 in set1 and n2 in set2) or (n1 in set2 and n2 in set1):
                conflicts_db.append({
                    "ingredient1": ing1_obj.name,
                    "ingredient2": ing2_obj.name,
                    "risk_level": incomp.risk_level,
                    "reason": incomp.reason or "Conflit enregistré",
                })

        # Heuristiques additionnelles (simplifiées)
        heuristic_conflicts = []
        def has_any(group, s):
            return any(g in s for g in group)
        acids = {"aha","bha","acide salicylique","acide glycolique","acide lactique","retinol","rétinol"}
        drying = {"peroxyde de benzoyle","alcool","soufre"}
        soothing = {"niacinamide","allantoïne","acide hyaluronique","vitamine b5"}

        # Irritation cumulative
        if (has_any(acids, set1) and has_any(drying, set2)) or (has_any(acids, set2) and has_any(drying, set1)):
            heuristic_conflicts.append({
                "ingredient1": "Actifs exfoliants / rétinoïdes",
                "ingredient2": "Agents asséchants",
                "risk_level": "MEDIUM",
                "reason": "Association potentiellement irritante (sécheresse cumulée)."
            })

        # Neutralisation antioxydants (ex: Cuivre + Vitamine C déjà dans DB mais fallback)
        if ("vitamine c" in set1 and "peptides de cuivre" in set2) or ("vitamine c" in set2 and "peptides de cuivre" in set1):
            heuristic_conflicts.append({
                "ingredient1": "Vitamine C",
                "ingredient2": "Peptides de cuivre",
                "risk_level": "MEDIUM",
                "reason": "Oxydation possible réduisant l'efficacité du peptide."
            })

        all_conflicts = conflicts_db + heuristic_conflicts
        is_compatible = len(all_conflicts) == 0

        # Générer résumé texte
        if all_conflicts:
            lines = []
            trans = {"CRITICAL":"🔴 Critique","HIGH":"🟠 Élevé","MEDIUM":"🟡 Moyen","LOW":"🟢 Faible"}
            for c in all_conflicts:
                lvl = trans.get((c.get("risk_level") or "").upper(), c.get("risk_level") or "?")
                lines.append(f"- {c['ingredient1']} + {c['ingredient2']} → {lvl}\n  Raison: {c['reason']}")
            summary_text = "\n".join(lines)
        else:
            summary_text = "Aucune incompatibilité détectée; combinaison généralement complémentaire (purifiant + hydratant)."

        # Persistence optionnelle
        persisted = False
        created_ids = {}
        if persist:
            try:
                # Créer produits et ingrédients si absents
                for prod in (product1, product2):
                    name = prod.get("name")[:150]
                    existing = Product.query.filter_by(name=name).first()
                    if not existing:
                        existing = Product(name=name, product_type="Auto", brand=None)
                        sqldb.session.add(existing)
                        sqldb.session.flush()
                    created_ids[name] = existing.id
                    for ing_name in prod.get("ingredients", []):
                        ing_norm = ing_name.strip()
                        ing_obj = Ingredient.query.filter_by(name=ing_norm).first()
                        if not ing_obj:
                            ing_obj = Ingredient(name=ing_norm, ingredient_type=None)
                            sqldb.session.add(ing_obj)
                            sqldb.session.flush()
                        # Lier
                        link_exists = ProductIngredient.query.filter_by(product_id=existing.id, ingredient_id=ing_obj.id).first()
                        if not link_exists:
                            sqldb.session.add(ProductIngredient(product_id=existing.id, ingredient_id=ing_obj.id))
                sqldb.session.commit()
                persisted = True
            except Exception as pe:
                sqldb.session.rollback()
                logging.warning(f"Persistance échouée: {pe}")

        return jsonify({
            "product1": product1,
            "product2": product2,
            "compatible": is_compatible,
            "conflicts_count": len(all_conflicts),
            "conflicts": all_conflicts,
            "summary": summary_text,
            "persisted": persisted,
            "product_ids": created_ids
        })
    except Exception as e:
        logging.error(f"Erreur compatibility_from_text: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/data/products", methods=["GET"])
def list_products():
    """
    Liste tous les produits importés.
    
    Returns:
        JSON: Liste des produits
    """
    try:
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])
    except Exception as e:
        logging.error(f"Erreur liste produits: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/data/ingredients", methods=["GET"])
def list_ingredients():
    """
    Liste tous les ingrédients importés.
    
    Returns:
        JSON: Liste des ingrédients
    """
    try:
        ingredients = Ingredient.query.all()
        return jsonify([i.to_dict() for i in ingredients])
    except Exception as e:
        logging.error(f"Erreur liste ingrédients: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/data/incompatibilities", methods=["GET"])
def list_incompatibilities():
    """
    Liste toutes les incompatibilités connues.
    
    Returns:
        JSON: Liste des incompatibilités
    """
    try:
        incomps = Incompatibility.query.all()
        return jsonify([i.to_dict() for i in incomps])
    except Exception as e:
        logging.error(f"Erreur liste incompatibilités: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# ==============================
# ROUTES ADMINISTRATION
# ==============================

@app.route("/admin/reload_index", methods=["POST"])
def admin_reload_index():
    """
    Recharge l'index FAISS (admin seulement).
    
    Returns:
        JSON: Statut de l'opération
    """
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401
        
    with index_lock:
        try:
            load_faiss_index()
            return jsonify({"status": "Index FAISS rechargé."})
        except Exception as e:
            logging.error(f"Erreur reload index : {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

@app.route("/admin/reset_index", methods=["POST"])
def admin_reset_index():
    """
    Réinitialise complètement l'index FAISS (admin seulement).
    
    Returns:
        JSON: Statut de l'opération
    """
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401
        
    with index_lock:
        try:
            # Création d'un nouvel index vide
            db_faiss = FAISS.from_documents([], embeddings)
            db_faiss.save_local(INDEX_PATH)
            
            # Mise à jour de la référence dans le module backend
            from backend import backendtow as backend_mod
            backend_mod.db = db_faiss
            
            return jsonify({"status": "Index FAISS réinitialisé."})
        except Exception as e:
            logging.error(f"Erreur reset index : {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

@app.route("/admin/add_document", methods=["POST"])
def admin_add_document():
    """
    Ajoute un document directement à l'index (admin seulement).
    
    Returns:
        JSON: Statut de l'opération
    """
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401
        
    with index_lock:
        try:
            text = request.json.get("text", "")
            metadata = request.json.get("metadata", {})
            
            if not text.strip():
                return jsonify({"error": "Texte vide fourni."}), 400
                
            success = add_document_to_index(text, metadata)
            if success:
                return jsonify({"status": "Document ajouté à l'index."})
            else:
                return jsonify({"error": "Échec de l'ajout du document."}), 500
                
        except Exception as e:
            logging.error(f"Erreur add document : {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

# ==============================
# POINT D'ENTRÉE DE L'APPLICATION
# ==============================

if __name__ == "__main__":
    # Création des tables de base de données
    with app.app_context():
        sqldb.create_all()
        logging.info("Tables de données créées")
    
    # Chargement de l'index FAISS au démarrage
    load_faiss_index()
    
    # Lancement de l'application Flask
    app.run(debug=True, use_reloader=False)
