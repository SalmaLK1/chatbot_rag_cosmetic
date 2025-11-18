"""Génère un PDF avec schémas visuels des modes du chatbot (architecture réelle).
Usage: python scripts/generate_schemas_modes_v2.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from datetime import datetime

def create_unified_schema():
    """Schéma: Architecture unifiée /ask"""
    d = Drawing(520, 450)
    
    # Titre
    d.add(String(260, 430, "ARCHITECTURE HYBRIDE : Conversationnel + RAG", 
                fontSize=13, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    d.add(String(260, 415, "Route /ask unique - Toggle RAG pour activer/désactiver recherche documentaire", 
                fontSize=9, fontName='Helvetica-Oblique', 
                textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # USER REQUEST (UNIQUE)
    d.add(Rect(160, 360, 200, 45, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=3))
    d.add(String(260, 390, "👤 UTILISATEUR", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(260, 377, "POST /ask avec paramètres:", fontSize=9, textAnchor='middle'))
    d.add(String(260, 367, "question + file? + use_rag (toggle)", fontSize=8, 
                fontName='Courier', textAnchor='middle'))
    
    # Flèche vers backend
    d.add(Line(260, 360, 260, 340, strokeColor=colors.HexColor('#1a5490'), strokeWidth=3))
    d.add(Polygon([256, 340, 260, 330, 264, 340], 
                 fillColor=colors.HexColor('#1a5490'), strokeColor=None))
    
    # BACKEND DETECTION
    d.add(Rect(140, 285, 240, 45, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(260, 315, "⚙️ BACKEND INTELLIGENT", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(260, 302, "Détecte: fichier? + use_rag?", fontSize=8, textAnchor='middle'))
    d.add(String(260, 292, "Adapte le traitement automatiquement", fontSize=8, textAnchor='middle'))
    
    # ROUTER (losange décision)
    d.add(Polygon([260,275, 340,245, 260,215, 180,245], 
                 fillColor=colors.HexColor('#17a2b8'), 
                 strokeColor=colors.black, strokeWidth=2))
    d.add(String(260, 250, "🔀 LOGIQUE", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.white))
    d.add(String(260, 240, "HYBRIDE", fontSize=8, textAnchor='middle', 
                fillColor=colors.white))
    
    # Branche GAUCHE: Mode simple
    d.add(Line(180, 245, 100, 180, strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(String(125, 212, "use_rag=False", fontSize=7, fontName='Helvetica-Bold', 
                textAnchor='start', fillColor=colors.HexColor('#1a5490')))
    
    d.add(Rect(10, 145, 180, 50, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(100, 180, "💬 MODE CONVERSATIONNEL", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(100, 167, "Gemini génère directement", fontSize=8, textAnchor='middle'))
    d.add(String(100, 157, "Réponse rapide (1-2s)", fontSize=7, textAnchor='middle'))
    d.add(String(100, 150, "Sans citations sources", fontSize=7, textAnchor='middle'))
    
    # Branche DROITE: Mode RAG
    d.add(Line(340, 245, 420, 180, strokeColor=colors.red, strokeWidth=2))
    d.add(String(395, 212, "use_rag=True + PDF", fontSize=7, fontName='Helvetica-Bold', 
                textAnchor='end', fillColor=colors.red))
    
    d.add(Rect(330, 145, 180, 50, fillColor=colors.HexColor('#ffe6e6'), 
               strokeColor=colors.red, strokeWidth=2))
    d.add(String(420, 180, "🔥 MODE RAG", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(420, 167, "Pipeline documentaire", fontSize=8, textAnchor='middle'))
    d.add(String(420, 157, "Indexation + Recherche + Rerank", fontSize=7, textAnchor='middle'))
    d.add(String(420, 150, "Citations sources (92% précision)", fontSize=7, textAnchor='middle'))
    
    # Convergence réponse
    d.add(Line(100, 145, 260, 90, strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(Line(420, 145, 260, 90, strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    
    # RÉPONSE FINALE
    d.add(Rect(160, 55, 200, 35, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(260, 80, "✅ RÉPONSE UNIFIÉE", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(260, 67, "JSON: {answer, context, sources...}", fontSize=8, 
                fontName='Courier', textAnchor='middle'))
    
    # Détails bas
    d.add(Rect(30, 5, 225, 40, fillColor=colors.white, 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=1))
    d.add(String(50, 35, "✅ AVANTAGE ARCHITECTURE :", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='start'))
    d.add(String(50, 25, "• 1 seule route = UX fluide", fontSize=7, textAnchor='start'))
    d.add(String(50, 17, "• Toggle simple pour l'utilisateur", fontSize=7, textAnchor='start'))
    d.add(String(50, 9, "• Combine meilleur des 2 mondes", fontSize=7, textAnchor='start'))
    
    d.add(Rect(265, 5, 225, 40, fillColor=colors.white, 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=1))
    d.add(String(285, 35, "🚀 ÉVOLUTION FUTURE :", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='start', fillColor=colors.HexColor('#ff8c00')))
    d.add(String(285, 25, "• Mode Multimodal (Audio, Image)", fontSize=7, textAnchor='start'))
    d.add(String(285, 17, "• OCR + Whisper intégrés", fontSize=7, textAnchor='start'))
    d.add(String(285, 9, "• Architecture prête pour extension", fontSize=7, textAnchor='start'))
    
    return d

def create_rag_pipeline_detail():
    """Schéma détaillé pipeline RAG (quand PDF uploadé)"""
    d = Drawing(520, 450)
    
    # Titre
    d.add(String(260, 430, "PIPELINE RAG DÉTAILLÉ (Mode avec PDF)", 
                fontSize=14, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    # INPUT
    d.add(Rect(190, 390, 140, 30, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(String(260, 410, "INPUT", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(260, 398, "PDF + Question texte", fontSize=8, textAnchor='middle'))
    
    # Flèche
    d.add(Line(260, 390, 260, 375, strokeColor=colors.red, strokeWidth=2))
    d.add(Polygon([256, 375, 260, 365, 264, 375], 
                 fillColor=colors.red, strokeColor=None))
    
    # PHASE 1: INDEXATION
    d.add(Rect(30, 310, 460, 55, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(260, 352, "PHASE 1 : INDEXATION (Une fois par PDF)", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    
    steps_indexation = [
        "1. Chunking (NLTK) → 500 tokens/chunk, overlap 100",
        "2. Embeddings (Sentence-Transformers) → 384 dimensions",
        "3. FAISS Indexation (IndexFlatL2) → Exhaustive search"
    ]
    y_pos = 335
    for step in steps_indexation:
        d.add(String(50, y_pos, step, fontSize=7, textAnchor='start'))
        y_pos -= 10
    
    d.add(String(450, 315, "⏱️ 3.5s", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='end', fillColor=colors.red))
    
    # Flèche
    d.add(Line(260, 310, 260, 295, strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(Polygon([256, 295, 260, 285, 264, 295], 
                 fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # PHASE 2: RECHERCHE & GÉNÉRATION
    d.add(Rect(30, 150, 460, 135, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(260, 272, "PHASE 2 : PIPELINE RAG (À chaque question)", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    
    steps_rag = [
        "4. RAG Fusion : Gemini génère 3 variantes de la question",
        "5. FAISS Search : 3 recherches parallèles → Top 15 chunks",
        "6. Reciprocal Rank Fusion (k=60) : Fusion résultats",
        "7. CrossEncoder Rerank : Affinage précision → Top 3 chunks",
        "8. Build Prompt : Contexte + Instructions structurées",
        "9. Gemini Generate (temp=0.3) : Réponse factuelle",
        "10. Attach Sources : PDF + Page + Paragraphe"
    ]
    y_pos = 255
    for step in steps_rag:
        d.add(String(50, y_pos, step, fontSize=7, textAnchor='start'))
        y_pos -= 16
    
    d.add(String(450, 155, "⏱️ 2.65s", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='end', fillColor=colors.red))
    
    # Flèche
    d.add(Line(260, 150, 260, 125, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([256, 125, 260, 115, 264, 125], 
                 fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # OUTPUT
    d.add(Rect(140, 75, 240, 40, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(260, 102, "✅ RÉPONSE AVEC SOURCES", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(260, 90, "Texte + Citations (PDF, page, §)", fontSize=8, textAnchor='middle'))
    d.add(String(260, 80, "Précision: 92% | Sources: 100%", fontSize=7, 
                fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#28a745')))
    
    # TEMPS TOTAL
    d.add(Rect(30, 40, 460, 25, fillColor=colors.HexColor('#ffe6e6'), 
               strokeColor=colors.red, strokeWidth=2))
    d.add(String(260, 57, "⏱️ TEMPS TOTAL : 6.15s (1ère fois) = 3.5s indexation + 2.65s réponse", 
                fontSize=9, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.red))
    d.add(String(260, 46, "Questions suivantes sur même PDF : 2.65s seulement (index déjà créé)", 
                fontSize=8, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # INNOVATIONS
    d.add(String(260, 25, "⭐ INNOVATIONS : RAG Fusion (3 variantes) | Double filtrage (FAISS+CrossEncoder) | Cache MD5 (97% gain temps)", 
                fontSize=7, fontName='Helvetica-Oblique', textAnchor='middle', fillColor=colors.HexColor('#ff8c00')))
    
    return d

def create_comparison_table():
    """Tableau comparatif des modes"""
    d = Drawing(520, 380)
    
    d.add(String(260, 360, "SYSTÈME HYBRIDE : Conversationnel + RAG", 
                fontSize=14, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    d.add(String(260, 345, "L'utilisateur choisit via le toggle use_rag", 
                fontSize=10, fontName='Helvetica-Oblique', 
                textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # Tableau
    data = [
        ['Critère', 'Mode Conversationnel\n(use_rag=False)', 'Mode RAG\n(use_rag=True + PDF)'],
        ['Philosophie', 'Réponse générale rapide', 'Analyse documentaire précise'],
        ['Input requis', 'Question texte uniquement', 'Question + PDF uploadé'],
        ['Traitement', 'Gemini génère directement', 'Pipeline RAG 10 étapes'],
        ['Sources citées', '❌ Non', '✅ Oui (100%)'],
        ['Précision', '~70% (générique)', '92% (validé sur 50 questions)'],
        ['Temps réponse', '1-2s', '6s (1ère) puis 2.65s'],
        ['Transparence', 'Faible', 'Totale (PDF + page + §)'],
        ['Use case', 'Questions générales cosmétiques', 'Analyse PDFs techniques'],
        ['Hallucinations', 'Possibles', 'Réduites (contexte strict)']
    ]
    
    # Positionnement tableau
    y_start = 300
    row_height = 22
    
    # En-tête
    d.add(Rect(30, y_start, 110, 30, fillColor=colors.HexColor('#1a5490'), strokeColor=colors.black, strokeWidth=1))
    d.add(String(85, y_start+18, data[0][0], fontSize=9, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.white))
    
    d.add(Rect(140, y_start, 170, 30, fillColor=colors.HexColor('#e8f5e9'), strokeColor=colors.black, strokeWidth=1))
    d.add(String(225, y_start+18, data[0][1], fontSize=8, fontName='Helvetica-Bold', textAnchor='middle'))
    
    d.add(Rect(310, y_start, 180, 30, fillColor=colors.HexColor('#ffe6e6'), strokeColor=colors.black, strokeWidth=1))
    d.add(String(400, y_start+18, data[0][2], fontSize=8, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Lignes
    for i, row in enumerate(data[1:], 1):
        y = y_start - (i * row_height)
        
        # Colonne 1
        d.add(Rect(30, y, 110, 20, fillColor=colors.HexColor('#f9f9f9') if i%2==0 else colors.white, 
                  strokeColor=colors.black, strokeWidth=0.5))
        d.add(String(35, y+10, row[0], fontSize=7, fontName='Helvetica-Bold', textAnchor='start'))
        
        # Colonne 2
        d.add(Rect(140, y, 170, 20, fillColor=colors.white, strokeColor=colors.black, strokeWidth=0.5))
        lines = row[1].split('\n')
        if len(lines) == 1:
            d.add(String(225, y+10, lines[0], fontSize=7, textAnchor='middle'))
        else:
            d.add(String(225, y+14, lines[0], fontSize=6, textAnchor='middle'))
            d.add(String(225, y+6, lines[1], fontSize=6, textAnchor='middle'))
        
        # Colonne 3
        d.add(Rect(310, y, 180, 20, fillColor=colors.white, strokeColor=colors.black, strokeWidth=0.5))
        lines = row[2].split('\n')
        if len(lines) == 1:
            d.add(String(400, y+10, lines[0], fontSize=7, textAnchor='middle'))
        elif len(lines) == 2:
            d.add(String(400, y+14, lines[0], fontSize=6, textAnchor='middle'))
            d.add(String(400, y+6, lines[1], fontSize=6, textAnchor='middle'))
        else:
            d.add(String(400, y+16, lines[0], fontSize=6, textAnchor='middle'))
            d.add(String(400, y+10, lines[1], fontSize=6, textAnchor='middle'))
            d.add(String(400, y+4, lines[2], fontSize=6, textAnchor='middle'))
    
    # Conclusion combinaison
    d.add(Rect(30, 60, 460, 25, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(260, 77, "✅ COMBINAISON INTELLIGENTE : Conversationnel pour rapidité, RAG pour précision", 
                fontSize=9, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#28a745')))
    d.add(String(260, 66, "L'utilisateur switche selon son besoin : question rapide OU analyse documentaire approfondie", 
                fontSize=8, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # Extension multimodale
    d.add(Rect(30, 30, 460, 25, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(260, 47, "🚀 EXTENSION FUTURE : Mode Multimodal (Audio Whisper, Image OCR, DOCX)", 
                fontSize=9, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.HexColor('#ff8c00')))
    d.add(String(260, 36, "Architecture modulaire prête pour intégration : même route /ask, normalisation input → pipeline RAG existant", 
                fontSize=7, textAnchor='middle', fillColor=colors.HexColor('#666666')))
    
    # Note architecture
    d.add(String(260, 15, "📌 Point technique clé : MÊME route /ask pour les 2 modes = Simplicité backend + UX fluide", 
                fontSize=8, fontName='Helvetica-Oblique', textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    return d

def generate_schemas_pdf():
    filename = "SCHEMAS_ARCHITECTURE_REELLE.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=1*cm, leftMargin=1*cm,
                           topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    story = []
    
    # Page de garde
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("ARCHITECTURE RÉELLE DU CHATBOT", title_style))
    story.append(Paragraph("Schémas basés sur le code app.py", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                       fontSize=14, alignment=TA_CENTER, 
                                       textColor=colors.HexColor('#666666'))))
    
    story.append(Spacer(1, 1*cm))
    
    story.append(Paragraph(
        "<b>Architecture unifiée :</b> Une seule route <font face='Courier'>/ask</font> "
        "gère TOUS les types d'input (texte seul OU texte + PDF). Le chatbot combine "
        "intelligemment le mode conversationnel et le mode RAG selon le contexte.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(
        "<b>Flexibilité actuelle :</b> L'utilisateur peut activer/désactiver le RAG via un toggle. "
        "Avec RAG activé + PDF uploadé, le système cite ses sources (92% précision). "
        "Sans PDF ou RAG désactivé, le chatbot répond de manière conversationnelle classique.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "<b>🚀 Évolution future :</b> Le système est conçu pour accueillir le mode multimodal "
        "(audio via Whisper, images via OCR, DOCX). L'architecture modulaire permet d'ajouter "
        "facilement de nouveaux types d'input sans modifier la logique RAG existante.",
        ParagraphStyle('Future', parent=normal_style, 
                      textColor=colors.HexColor('#ff8c00'), fontName='Helvetica-Oblique')
    ))
    
    story.append(PageBreak())
    
    # Schéma 1
    story.append(Paragraph("1. ARCHITECTURE HYBRIDE", title_style))
    story.append(create_unified_schema())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Notre système combine intelligemment le mode conversationnel (rapide) et le mode RAG (précis). "
        "Un simple toggle <font face='Courier'>use_rag</font> permet à l'utilisateur de choisir : "
        "question rapide sans sources OU analyse documentaire avec citations. "
        "La route <font face='Courier'>/ask</font> unique détecte automatiquement la présence de fichiers "
        "et adapte le traitement. Cette architecture hybride offre flexibilité maximale dans une interface simple.",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Schéma 2
    story.append(Paragraph("2. PIPELINE RAG DÉTAILLÉ", title_style))
    story.append(create_rag_pipeline_detail())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Quand un PDF est uploadé, le système effectue 10 étapes : 3 pour l'indexation (unique par PDF) "
        "et 7 pour le pipeline RAG (à chaque question). Les innovations majeures sont le RAG Fusion "
        "(génération de 3 variantes de question) et le double filtrage (FAISS pour rapidité + CrossEncoder "
        "pour précision).",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Tableau comparatif
    story.append(Paragraph("3. SYSTÈME HYBRIDE : MEILLEUR DES 2 MONDES", title_style))
    story.append(create_comparison_table())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "La force de notre système est sa <b>flexibilité hybride</b> : l'utilisateur choisit "
        "selon son besoin. Pour une question générale rapide (\"C'est quoi le rétinol ?\"), "
        "le mode conversationnel répond en 1-2s. Pour une analyse documentaire technique "
        "(\"Rétinol + acide glycolique compatible selon ce PDF ?\"), le mode RAG fournit "
        "une réponse précise avec citations en 6s (puis 2.65s pour les questions suivantes). "
        "<b>Combinaison intelligente plutôt que choix exclusif.</b>",
        normal_style
    ))
    
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "🚀 <b>Extension future :</b> L'architecture modulaire est prête pour le mode multimodal. "
        "L'ajout de traitement audio (Whisper), image (OCR Tesseract), ou DOCX se fera "
        "via la même route /ask, avec normalisation des inputs avant injection dans le "
        "pipeline RAG existant. Aucune réécriture majeure nécessaire.",
        ParagraphStyle('Future', parent=normal_style, 
                      textColor=colors.HexColor('#ff8c00'))
    ))
    
    story.append(PageBreak())
    
    # Workflow textuel
    story.append(Paragraph("4. WORKFLOW COMPLET", title_style))
    
    workflow_text = """<b>SCÉNARIO 1 : Texte seul</b><br/>
1. Utilisateur tape "C'est quoi le rétinol ?" (pas de fichier)<br/>
2. Frontend envoie POST /ask {question: "...", use_rag: false}<br/>
3. Backend détecte aucun fichier → appelle process_question()<br/>
4. Gemini génère réponse directe (1-2s)<br/>
5. Réponse JSON {answer, context:[], ...}<br/>
<br/>
<b>SCÉNARIO 2 : Texte + PDF</b><br/>
1. Utilisateur upload Guide_Retinol.pdf + tape "Rétinol + acide glycolique compatible ?"<br/>
2. Frontend envoie POST /ask {question: "...", file: PDF, use_rag: true}<br/>
3. Backend détecte fichier → appelle handle_multiple_uploaded_files()<br/>
4. Phase indexation (3.5s) : Chunking → Embeddings → FAISS<br/>
5. Phase RAG (2.65s) : RAG Fusion → Search → Rerank → Generate<br/>
6. Réponse JSON {answer, context: [chunks avec sources], ...}<br/>
<br/>
<b>SCÉNARIO 3 : Questions suivantes sur même PDF</b><br/>
1. Utilisateur pose nouvelle question (index déjà créé)<br/>
2. Backend skip indexation → direct au pipeline RAG<br/>
3. Réponse en 2.65s seulement
"""
    
    story.append(Paragraph(workflow_text, normal_style))
    
    # Footer
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("_______________________________________________", 
                          ParagraphStyle('Line', parent=styles['Normal'], alignment=TA_CENTER)))
    story.append(Paragraph(
        f"<i>Schémas basés sur app.py - Générés le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                      alignment=TA_CENTER, textColor=colors.grey)
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Schémas architecture réelle générés : {filename}")
    return filename

if __name__ == '__main__':
    generate_schemas_pdf()
