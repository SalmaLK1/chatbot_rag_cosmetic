"""Génère des images PNG des schémas pour PowerPoint (version PIL).
Usage: python scripts/generate_schemas_ppt.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

def draw_rounded_rectangle(draw, xy, radius, fill, outline=None, width=2):
    """Dessine un rectangle aux coins arrondis"""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=outline, width=width)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=fill, outline=outline)
    draw.pieslice([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=fill, outline=outline)
    draw.pieslice([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=fill, outline=outline)
    draw.pieslice([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=fill, outline=outline)

def create_architecture_schema():
    """Schéma 1: Architecture hybride"""
    # Créer image
    img = Image.new('RGB', (900, 750), color='white')
    draw = ImageDraw.Draw(img)
    
    # Polices
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_subtitle = ImageFont.truetype("arial.ttf", 18)
        font_large = ImageFont.truetype("arialbd.ttf", 20)
        font_normal = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 13)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = font_large = font_normal = font_small = font_title
    
    # Titre
    draw.text((450, 30), "ARCHITECTURE HYBRIDE", fill='#1a5490', font=font_title, anchor='mm')
    draw.text((450, 65), "Conversationnel + RAG dans route /ask unique", fill='#666666', font=font_subtitle, anchor='mm')
    
    # USER
    draw_rounded_rectangle(draw, [300, 120, 600, 200], 15, '#e7f3ff', '#1a5490', 3)
    draw.text((450, 145), "👤 UTILISATEUR", fill='black', font=font_large, anchor='mm')
    draw.text((450, 170), "POST /ask", fill='black', font=font_normal, anchor='mm')
    draw.text((450, 190), "question + file? + use_rag?", fill='#333', font=font_small, anchor='mm')
    
    # Flèche
    draw.line([(450, 200), (450, 250)], fill='#1a5490', width=5)
    draw.polygon([(440, 240), (450, 250), (460, 240)], fill='#1a5490')
    
    # BACKEND
    draw_rounded_rectangle(draw, [250, 250, 650, 330], 15, '#fff3cd', '#ff8c00', 2)
    draw.text((450, 275), "⚙️ BACKEND INTELLIGENT", fill='black', font=font_large, anchor='mm')
    draw.text((450, 300), "Détecte: fichier? + use_rag?", fill='black', font=font_normal, anchor='mm')
    draw.text((450, 318), "Route automatiquement", fill='#666', font=font_small, anchor='mm')
    
    # ROUTER (losange)
    draw.polygon([(450, 370), (550, 420), (450, 470), (350, 420)], fill='#17a2b8', outline='black', width=3)
    draw.text((450, 420), "🔀 ROUTING", fill='white', font=font_large, anchor='mm')
    
    # Branche GAUCHE: Conversationnel
    draw.line([(350, 420), (200, 530)], fill='#28a745', width=4)
    draw.text((260, 470), "use_rag=False", fill='#28a745', font=font_normal, anchor='mm')
    
    draw_rounded_rectangle(draw, [50, 500, 350, 600], 15, '#e8f5e9', '#28a745', 3)
    draw.text((200, 530), "💬 CONVERSATIONNEL", fill='black', font=font_large, anchor='mm')
    draw.text((200, 555), "Gemini direct", fill='black', font=font_normal, anchor='mm')
    draw.text((200, 575), "Rapide (1-2s), Sans sources", fill='#666', font=font_small, anchor='mm')
    
    # Branche DROITE: RAG
    draw.line([(550, 420), (700, 530)], fill='red', width=4)
    draw.text((640, 470), "use_rag=True + PDF", fill='red', font=font_normal, anchor='mm')
    
    draw_rounded_rectangle(draw, [550, 500, 850, 600], 15, '#ffe6e6', 'red', 3)
    draw.text((700, 530), "🔥 MODE RAG", fill='black', font=font_large, anchor='mm')
    draw.text((700, 555), "Pipeline 10 étapes", fill='black', font=font_normal, anchor='mm')
    draw.text((700, 575), "Précis (92%), Avec sources", fill='#666', font=font_small, anchor='mm')
    
    # Convergence
    draw.line([(200, 600), (450, 650)], fill='#28a745', width=4)
    draw.line([(700, 600), (450, 650)], fill='#28a745', width=4)
    
    # RÉPONSE
    draw_rounded_rectangle(draw, [300, 650, 600, 710], 15, '#d4edda', '#28a745', 3)
    draw.text((450, 675), "✅ RÉPONSE UNIFIÉE", fill='black', font=font_large, anchor='mm')
    draw.text((450, 695), "JSON: {answer, context...}", fill='#333', font=font_small, anchor='mm')
    
    # Note
    draw.text((450, 735), "🚀 Extension future : Mode Multimodal (Audio, Image, DOCX)", 
             fill='#ff8c00', font=font_normal, anchor='mm')
    
    return img

def create_pipeline_schema():
    """Schéma 2: Pipeline RAG"""
    img = Image.new('RGB', (900, 850), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_subtitle = ImageFont.truetype("arial.ttf", 18)
        font_large = ImageFont.truetype("arialbd.ttf", 18)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = font_large = font_normal = font_small = font_title
    
    # Titre
    draw.text((450, 30), "PIPELINE RAG COMPLET", fill='#1a5490', font=font_title, anchor='mm')
    draw.text((450, 60), "10 étapes du PDF à la réponse citée", fill='#666666', font=font_subtitle, anchor='mm')
    
    # INPUT
    draw_rounded_rectangle(draw, [325, 90, 575, 140], 12, '#e7f3ff', '#1a5490', 2)
    draw.text((450, 105), "INPUT", fill='black', font=font_large, anchor='mm')
    draw.text((450, 125), "PDF + Question", fill='black', font=font_normal, anchor='mm')
    
    # Flèche
    draw.line([(450, 140), (450, 175)], fill='red', width=4)
    draw.polygon([(440, 170), (450, 175), (460, 170)], fill='red')
    
    # PHASE 1
    draw_rounded_rectangle(draw, [100, 175, 800, 280], 12, '#fff3cd', '#ff8c00', 3)
    draw.text((450, 195), "PHASE 1 : INDEXATION (3.5s - unique par PDF)", 
             fill='black', font=font_large, anchor='mm')
    steps1 = [
        "1. Chunking (NLTK) → 500 tokens, overlap 100",
        "2. Embeddings (Sentence-Transformers) → 384 dimensions",
        "3. FAISS Indexation (IndexFlatL2) → Recherche exhaustive"
    ]
    y = 220
    for step in steps1:
        draw.text((120, y), step, fill='black', font=font_normal)
        y += 20
    
    # Flèche
    draw.line([(450, 280), (450, 315)], fill='#28a745', width=4)
    draw.polygon([(440, 310), (450, 315), (460, 310)], fill='#28a745')
    
    # PHASE 2
    draw_rounded_rectangle(draw, [100, 315, 800, 570], 12, '#e8f5e9', '#28a745', 3)
    draw.text((450, 335), "PHASE 2 : PIPELINE RAG (2.65s - à chaque question)", 
             fill='black', font=font_large, anchor='mm')
    steps2 = [
        "4. RAG Fusion : Gemini génère 3 variantes de la question",
        "5. FAISS Search : 3 recherches parallèles → Top 15 chunks",
        "6. Reciprocal Rank Fusion (k=60) : Combine résultats",
        "7. CrossEncoder Rerank : Affine précision → Top 3 chunks",
        "8. Build Prompt : Contexte + Instructions structurées",
        "9. Gemini Generate (temp=0.3) : Génération factuelle",
        "10. Attach Sources : PDF + Page + Paragraphe"
    ]
    y = 365
    for step in steps2:
        draw.text((120, y), step, fill='black', font=font_normal)
        y += 29
    
    # Flèche
    draw.line([(450, 570), (450, 605)], fill='#28a745', width=4)
    draw.polygon([(440, 600), (450, 605), (460, 600)], fill='#28a745')
    
    # OUTPUT
    draw_rounded_rectangle(draw, [250, 605, 650, 680], 12, '#d4edda', '#28a745', 3)
    draw.text((450, 625), "✅ RÉPONSE AVEC SOURCES", fill='black', font=font_large, anchor='mm')
    draw.text((450, 648), "Texte + Citations (PDF, page, §)", fill='black', font=font_normal, anchor='mm')
    draw.text((450, 668), "Précision: 92% | Sources: 100%", fill='#28a745', font=font_normal, anchor='mm')
    
    # TEMPS
    draw_rounded_rectangle(draw, [100, 700, 800, 760], 12, '#ffe6e6', 'red', 2)
    draw.text((450, 720), "⏱️ TEMPS TOTAL : 6.15s (1ère fois) = 3.5s + 2.65s", 
             fill='red', font=font_large, anchor='mm')
    draw.text((450, 745), "Questions suivantes : 2.65s seulement (index déjà créé)", 
             fill='#666', font=font_normal, anchor='mm')
    
    # INNOVATIONS
    draw.text((450, 790), "⭐ INNOVATIONS : RAG Fusion | Double filtrage | Cache MD5", 
             fill='#ff8c00', font=font_large, anchor='mm')
    draw.text((450, 815), "(3 variantes) | (FAISS+CrossEncoder) | (97% gain temps)", 
             fill='#666', font=font_small, anchor='mm')
    
    return img

def create_comparison_table():
    """Schéma 3: Tableau comparatif"""
    img = Image.new('RGB', (950, 700), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_header = ImageFont.truetype("arialbd.ttf", 17)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = font_header = font_normal = font_small = ImageFont.load_default()
    
    # Titre
    draw.text((475, 30), "SYSTÈME HYBRIDE : Conversationnel + RAG", 
             fill='#1a5490', font=font_title, anchor='mm')
    
    # Headers
    draw_rounded_rectangle(draw, [50, 70, 250, 115], 8, '#1a5490', 'black', 2)
    draw.text((150, 93), "Critère", fill='white', font=font_header, anchor='mm')
    
    draw_rounded_rectangle(draw, [260, 70, 540, 115], 8, '#e8f5e9', 'black', 2)
    draw.text((400, 93), "Conversationnel", fill='black', font=font_header, anchor='mm')
    
    draw_rounded_rectangle(draw, [550, 70, 830, 115], 8, '#ffe6e6', 'black', 2)
    draw.text((690, 93), "RAG", fill='black', font=font_header, anchor='mm')
    
    # Données
    data = [
        ['Input', 'Texte seul', 'Texte + PDF'],
        ['Traitement', 'Gemini direct', 'Pipeline 10 étapes'],
        ['Sources', '❌ Non', '✅ Oui (100%)'],
        ['Précision', '~70%', '92%'],
        ['Temps', '1-2s', '6s puis 2.65s'],
        ['Use case', 'Questions générales', 'Analyse documentaire'],
        ['Transparence', 'Faible', 'Totale (PDF+page+§)']
    ]
    
    y = 125
    for i, row in enumerate(data):
        bg = '#f9f9f9' if i % 2 else 'white'
        
        # Colonne 1
        draw_rounded_rectangle(draw, [50, y, 250, y+40], 5, bg, 'black', 1)
        draw.text((60, y+20), row[0], fill='black', font=font_header, anchor='lm')
        
        # Colonne 2
        draw_rounded_rectangle(draw, [260, y, 540, y+40], 5, 'white', 'black', 1)
        draw.text((400, y+20), row[1], fill='black', font=font_normal, anchor='mm')
        
        # Colonne 3
        draw_rounded_rectangle(draw, [550, y, 830, y+40], 5, 'white', 'black', 1)
        draw.text((690, y+20), row[2], fill='black', font=font_normal, anchor='mm')
        
        y += 45
    
    # Conclusion
    draw_rounded_rectangle(draw, [50, 470, 900, 530], 10, '#d4edda', '#28a745', 2)
    draw.text((475, 490), "✅ COMBINAISON INTELLIGENTE", 
             fill='#28a745', font=font_header, anchor='mm')
    draw.text((475, 512), "Conversationnel pour rapidité, RAG pour précision avec sources", 
             fill='#666', font=font_normal, anchor='mm')
    
    # Extension
    draw_rounded_rectangle(draw, [50, 550, 900, 610], 10, '#fff3cd', '#ff8c00', 2)
    draw.text((475, 570), "🚀 EXTENSION FUTURE : Mode Multimodal", 
             fill='#ff8c00', font=font_header, anchor='mm')
    draw.text((475, 592), "Audio (Whisper) + Image (OCR) + DOCX → Même architecture RAG", 
             fill='#666', font=font_normal, anchor='mm')
    
    # Note
    draw.text((475, 640), "📌 Point clé : MÊME route /ask pour les 2 modes", 
             fill='#1a5490', font=font_header, anchor='mm')
    draw.text((475, 665), "= Architecture simple + UX fluide + Extensibilité", 
             fill='#666', font=font_normal, anchor='mm')
    
    return img

def generate_png_for_ppt():
    """Génère les 3 schémas en PNG haute résolution"""
    
    print("Génération des schémas pour PowerPoint...")
    
    # Schéma 1
    print("  1/3 - Architecture hybride...")
    img1 = create_architecture_schema()
    img1.save("SCHEMA_1_ARCHITECTURE_HYBRIDE.png", "PNG", dpi=(150, 150))
    print("  ✅ SCHEMA_1_ARCHITECTURE_HYBRIDE.png")
    
    # Schéma 2
    print("  2/3 - Pipeline RAG...")
    img2 = create_pipeline_schema()
    img2.save("SCHEMA_2_PIPELINE_RAG.png", "PNG", dpi=(150, 150))
    print("  ✅ SCHEMA_2_PIPELINE_RAG.png")
    
    # Schéma 3
    print("  3/3 - Tableau comparatif...")
    img3 = create_comparison_table()
    img3.save("SCHEMA_3_COMPARAISON.png", "PNG", dpi=(150, 150))
    print("  ✅ SCHEMA_3_COMPARAISON.png")
    
    print("\n🎉 3 images PNG générées avec succès !")
    print("📁 Prêtes pour insertion dans PowerPoint")
    print("\n💡 Utilisation :")
    print("   - SCHEMA_1 : Slide architecture globale")
    print("   - SCHEMA_2 : Slide détails techniques pipeline")
    print("   - SCHEMA_3 : Slide comparaison et conclusion")

if __name__ == '__main__':
    generate_png_for_ppt()
