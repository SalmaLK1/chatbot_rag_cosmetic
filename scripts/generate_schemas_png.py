"""Génère des images PNG des schémas pour intégration PowerPoint.
Usage: python scripts/generate_schemas_png.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPM

def create_architecture_schema():
    """Schéma: Architecture hybride Conversationnel + RAG"""
    d = Drawing(600, 500)
    
    # Titre
    d.add(String(300, 480, "ARCHITECTURE HYBRIDE", 
                fontSize=18, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    d.add(String(300, 460, "Conversationnel + RAG dans une seule route /ask", 
                fontSize=12, fontName='Helvetica-Oblique', 
                textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # USER
    d.add(Rect(200, 390, 200, 50, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=3))
    d.add(String(300, 425, "👤 UTILISATEUR", fontSize=13, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(300, 410, "POST /ask", fontSize=11, textAnchor='middle'))
    d.add(String(300, 398, "question + file? + use_rag?", fontSize=10, 
                fontName='Courier', textAnchor='middle'))
    
    # Flèche
    d.add(Line(300, 390, 300, 365, strokeColor=colors.HexColor('#1a5490'), strokeWidth=4))
    d.add(Polygon([295, 365, 300, 355, 305, 365], 
                 fillColor=colors.HexColor('#1a5490'), strokeColor=None))
    
    # BACKEND
    d.add(Rect(170, 310, 260, 45, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(300, 340, "⚙️ BACKEND INTELLIGENT", fontSize=12, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(300, 325, "Détecte: fichier? + use_rag?", fontSize=10, textAnchor='middle'))
    d.add(String(300, 315, "Route automatiquement", fontSize=9, textAnchor='middle'))
    
    # ROUTER
    d.add(Polygon([300,300, 380,260, 300,220, 220,260], 
                 fillColor=colors.HexColor('#17a2b8'), 
                 strokeColor=colors.black, strokeWidth=3))
    d.add(String(300, 270, "🔀 ROUTING", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.white))
    d.add(String(300, 258, "HYBRIDE", fontSize=10, textAnchor='middle', 
                fillColor=colors.white))
    
    # Branche GAUCHE: Conversationnel
    d.add(Line(220, 260, 130, 180, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(160, 220, "use_rag=False", fontSize=9, fontName='Helvetica-Bold', 
                textAnchor='start', fillColor=colors.HexColor('#28a745')))
    
    d.add(Rect(20, 135, 220, 60, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(130, 180, "💬 CONVERSATIONNEL", fontSize=12, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(130, 165, "Gemini direct", fontSize=10, textAnchor='middle'))
    d.add(String(130, 152, "Rapide (1-2s)", fontSize=9, textAnchor='middle'))
    d.add(String(130, 141, "Sans sources", fontSize=8, textAnchor='middle'))
    
    # Branche DROITE: RAG
    d.add(Line(380, 260, 470, 180, strokeColor=colors.red, strokeWidth=3))
    d.add(String(440, 220, "use_rag=True + PDF", fontSize=9, fontName='Helvetica-Bold', 
                textAnchor='end', fillColor=colors.red))
    
    d.add(Rect(360, 135, 220, 60, fillColor=colors.HexColor('#ffe6e6'), 
               strokeColor=colors.red, strokeWidth=3))
    d.add(String(470, 180, "🔥 MODE RAG", fontSize=12, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(470, 165, "Pipeline 10 étapes", fontSize=10, textAnchor='middle'))
    d.add(String(470, 152, "Précis (92%)", fontSize=9, textAnchor='middle'))
    d.add(String(470, 141, "Avec sources", fontSize=8, textAnchor='middle'))
    
    # Convergence
    d.add(Line(130, 135, 300, 80, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Line(470, 135, 300, 80, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    
    # RÉPONSE
    d.add(Rect(200, 40, 200, 40, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(300, 67, "✅ RÉPONSE UNIFIÉE", fontSize=13, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(300, 52, "JSON: {answer, context...}", fontSize=10, 
                fontName='Courier', textAnchor='middle'))
    
    # Note
    d.add(String(300, 15, "🚀 Extension future : Mode Multimodal (Audio, Image, DOCX)", 
                fontSize=10, fontName='Helvetica-Oblique', textAnchor='middle', 
                fillColor=colors.HexColor('#ff8c00')))
    
    return d

def create_pipeline_rag_schema():
    """Schéma: Pipeline RAG détaillé"""
    d = Drawing(600, 550)
    
    # Titre
    d.add(String(300, 530, "PIPELINE RAG COMPLET", 
                fontSize=18, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    d.add(String(300, 510, "10 étapes du PDF à la réponse citée", 
                fontSize=12, fontName='Helvetica-Oblique', 
                textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # INPUT
    d.add(Rect(225, 460, 150, 35, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(String(300, 485, "INPUT", fontSize=12, fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(300, 470, "PDF + Question", fontSize=10, textAnchor='middle'))
    
    # Flèche
    d.add(Line(300, 460, 300, 445, strokeColor=colors.red, strokeWidth=3))
    d.add(Polygon([295, 445, 300, 435, 305, 445], fillColor=colors.red, strokeColor=None))
    
    # PHASE 1: INDEXATION
    d.add(Rect(50, 380, 500, 55, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=3))
    d.add(String(300, 420, "PHASE 1 : INDEXATION (3.5s - unique par PDF)", 
                fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    steps = [
        "1. Chunking (NLTK) → 500 tokens, overlap 100",
        "2. Embeddings (Sentence-Transformers) → 384 dimensions",
        "3. FAISS Indexation (IndexFlatL2) → Recherche exhaustive"
    ]
    y = 402
    for step in steps:
        d.add(String(70, y, step, fontSize=9, textAnchor='start'))
        y -= 14
    
    # Flèche
    d.add(Line(300, 380, 300, 365, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([295, 365, 300, 355, 305, 365], fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # PHASE 2: PIPELINE RAG
    d.add(Rect(50, 195, 500, 160, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(300, 343, "PHASE 2 : PIPELINE RAG (2.65s - à chaque question)", 
                fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    steps_rag = [
        "4. RAG Fusion : Gemini génère 3 variantes de la question",
        "5. FAISS Search : 3 recherches parallèles → Top 15 chunks",
        "6. Reciprocal Rank Fusion (k=60) : Combine les résultats",
        "7. CrossEncoder Rerank : Affine précision → Top 3 chunks",
        "8. Build Prompt : Contexte + Instructions structurées",
        "9. Gemini Generate (temp=0.3) : Génération factuelle",
        "10. Attach Sources : PDF + Page + Paragraphe"
    ]
    y = 320
    for step in steps_rag:
        d.add(String(70, y, step, fontSize=8, textAnchor='start'))
        y -= 18
    
    # Flèche
    d.add(Line(300, 195, 300, 170, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([295, 170, 300, 160, 305, 170], fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # OUTPUT
    d.add(Rect(175, 110, 250, 50, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(300, 145, "✅ RÉPONSE AVEC SOURCES", fontSize=13, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(300, 130, "Texte + Citations (PDF, page, §)", fontSize=10, textAnchor='middle'))
    d.add(String(300, 118, "Précision: 92% | Sources: 100%", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#28a745')))
    
    # TEMPS TOTAL
    d.add(Rect(50, 70, 500, 30, fillColor=colors.HexColor('#ffe6e6'), 
               strokeColor=colors.red, strokeWidth=2))
    d.add(String(300, 92, "⏱️ TEMPS TOTAL : 6.15s (1ère fois) = 3.5s + 2.65s", 
                fontSize=11, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.red))
    d.add(String(300, 78, "Questions suivantes : 2.65s seulement (index déjà créé)", 
                fontSize=9, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # INNOVATIONS
    d.add(Rect(50, 35, 500, 25, fillColor=colors.white, 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(300, 52, "⭐ INNOVATIONS CLÉS", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#ff8c00')))
    d.add(String(300, 40, "RAG Fusion (3 variantes) | Double filtrage (FAISS+CrossEncoder) | Cache MD5", 
                fontSize=8, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    return d

def create_comparison_table():
    """Tableau comparatif"""
    d = Drawing(650, 450)
    
    d.add(String(325, 430, "SYSTÈME HYBRIDE : Conversationnel + RAG", 
                fontSize=16, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    # Colonnes headers
    d.add(Rect(50, 390, 160, 30, fillColor=colors.HexColor('#1a5490'), 
               strokeColor=colors.black, strokeWidth=2))
    d.add(String(130, 408, "Critère", fontSize=11, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.white))
    
    d.add(Rect(210, 390, 200, 30, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.black, strokeWidth=2))
    d.add(String(310, 408, "Conversationnel", fontSize=11, fontName='Helvetica-Bold', 
                textAnchor='middle'))
    
    d.add(Rect(410, 390, 200, 30, fillColor=colors.HexColor('#ffe6e6'), 
               strokeColor=colors.black, strokeWidth=2))
    d.add(String(510, 408, "RAG", fontSize=11, fontName='Helvetica-Bold', 
                textAnchor='middle'))
    
    # Données
    data = [
        ['Input', 'Texte seul', 'Texte + PDF'],
        ['Traitement', 'Gemini direct', 'Pipeline 10 étapes'],
        ['Sources', '❌ Non', '✅ Oui (100%)'],
        ['Précision', '~70%', '92%'],
        ['Temps', '1-2s', '6s puis 2.65s'],
        ['Use case', 'Questions générales', 'Analyse documentaire'],
        ['Hallucinations', 'Possibles', 'Réduites']
    ]
    
    y = 360
    for i, row in enumerate(data):
        # Critère
        d.add(Rect(50, y, 160, 28, fillColor=colors.HexColor('#f9f9f9') if i%2 else colors.white, 
                  strokeColor=colors.black, strokeWidth=1))
        d.add(String(60, y+14, row[0], fontSize=10, fontName='Helvetica-Bold', textAnchor='start'))
        
        # Conv
        d.add(Rect(210, y, 200, 28, fillColor=colors.white, 
                  strokeColor=colors.black, strokeWidth=1))
        d.add(String(310, y+14, row[1], fontSize=9, textAnchor='middle'))
        
        # RAG
        d.add(Rect(410, y, 200, 28, fillColor=colors.white, 
                  strokeColor=colors.black, strokeWidth=1))
        d.add(String(510, y+14, row[2], fontSize=9, textAnchor='middle'))
        
        y -= 28
    
    # Conclusion
    d.add(Rect(50, 130, 560, 35, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(330, 155, "✅ COMBINAISON INTELLIGENTE", fontSize=12, 
                fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#28a745')))
    d.add(String(330, 140, "Conversationnel pour rapidité, RAG pour précision avec sources", 
                fontSize=10, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # Extension
    d.add(Rect(50, 85, 560, 35, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(330, 110, "🚀 EXTENSION FUTURE : Mode Multimodal", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#ff8c00')))
    d.add(String(330, 95, "Audio (Whisper) + Image (OCR) + DOCX → Même architecture RAG", 
                fontSize=9, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # Note
    d.add(String(330, 65, "📌 Point clé : MÊME route /ask pour les 2 modes", 
                fontSize=10, fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.HexColor('#1a5490')))
    d.add(String(330, 50, "= Architecture simple + UX fluide + Extensibilité", 
                fontSize=9, fontName='Helvetica-Oblique', textAnchor='middle', 
                fillColor=colors.HexColor('#666666')))
    
    return d

def generate_png_schemas():
    """Génère les 3 schémas en PNG haute résolution"""
    
    # Schéma 1: Architecture
    print("Génération schéma 1: Architecture hybride...")
    d1 = create_architecture_schema()
    renderPM.drawToFile(d1, "SCHEMA_1_ARCHITECTURE_HYBRIDE.png", fmt="PNG", dpi=150)
    print("✅ SCHEMA_1_ARCHITECTURE_HYBRIDE.png créé")
    
    # Schéma 2: Pipeline RAG
    print("Génération schéma 2: Pipeline RAG...")
    d2 = create_pipeline_rag_schema()
    renderPM.drawToFile(d2, "SCHEMA_2_PIPELINE_RAG.png", fmt="PNG", dpi=150)
    print("✅ SCHEMA_2_PIPELINE_RAG.png créé")
    
    # Schéma 3: Tableau comparatif
    print("Génération schéma 3: Tableau comparatif...")
    d3 = create_comparison_table()
    renderPM.drawToFile(d3, "SCHEMA_3_COMPARAISON.png", fmt="PNG", dpi=150)
    print("✅ SCHEMA_3_COMPARAISON.png créé")
    
    print("\n🎉 3 images PNG générées avec succès !")
    print("📁 Prêtes pour insertion dans PowerPoint")

if __name__ == '__main__':
    generate_png_schemas()
