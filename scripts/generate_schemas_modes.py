"""Génère un PDF avec schémas visuels des 3 modes du chatbot.
Usage: python scripts/generate_schemas_modes.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line, Polygon
from reportlab.graphics import renderPDF
from datetime import datetime

def create_mode1_schema():
    """Schéma Mode 1 : Conversationnel"""
    d = Drawing(500, 300)
    
    # Titre
    d.add(String(250, 280, "MODE 1 : CONVERSATIONNEL (Sans PDF)", 
                fontSize=16, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    # User
    d.add(Rect(50, 200, 100, 40, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(String(100, 220, "👤 UTILISATEUR", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(100, 210, "📝 Texte seul", fontSize=8, textAnchor='middle'))
    d.add(String(100, 202, "(Pas de fichier)", fontSize=7, textAnchor='middle'))
    
    # Flèche 1
    d.add(Line(150, 220, 200, 220, strokeColor=colors.HexColor('#1a5490'), strokeWidth=3))
    d.add(Polygon([200, 225, 210, 220, 200, 215], 
                 fillColor=colors.HexColor('#1a5490'), strokeColor=None))
    
    # Gemini
    d.add(Rect(210, 200, 100, 40, fillColor=colors.HexColor('#ffd700'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(260, 220, "🤖 GEMINI", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(260, 205, "Répond directement", fontSize=9, textAnchor='middle'))
    
    # Flèche 2
    d.add(Line(310, 220, 360, 220, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([360, 225, 370, 220, 360, 215], 
                 fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # Réponse
    d.add(Rect(370, 200, 100, 40, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(420, 220, "💬 RÉPONSE", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(420, 205, "Générique", fontSize=9, textAnchor='middle'))
    
    # Caractéristiques
    d.add(Rect(50, 100, 420, 80, fillColor=colors.white, 
               strokeColor=colors.HexColor('#cccccc'), strokeWidth=1))
    
    d.add(String(70, 160, "✅ AVANTAGES :", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='start', 
                fillColor=colors.HexColor('#28a745')))
    d.add(String(70, 145, "• Réponse rapide (1-2s)", fontSize=9, textAnchor='start'))
    d.add(String(70, 130, "• Pas besoin de documents", fontSize=9, textAnchor='start'))
    d.add(String(70, 115, "• Questions générales", fontSize=9, textAnchor='start'))
    
    d.add(String(280, 160, "❌ LIMITES :", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='start', 
                fillColor=colors.HexColor('#dc3545')))
    d.add(String(280, 145, "• Pas de sources", fontSize=9, textAnchor='start'))
    d.add(String(280, 130, "• Info générique", fontSize=9, textAnchor='start'))
    d.add(String(280, 115, "• Peut halluciner", fontSize=9, textAnchor='start'))
    
    # Exemple
    d.add(String(250, 40, "💡 EXEMPLE : \"C'est quoi le rétinol ?\"", 
                fontSize=10, fontName='Helvetica-Oblique', 
                textAnchor='middle', fillColor=colors.HexColor('#666666')))
    d.add(String(250, 25, "→ Définition générale sans source spécifique", 
                fontSize=9, textAnchor='middle', fillColor=colors.HexColor('#888888')))
    
    return d

def create_mode2_schema():
    """Schéma Mode 2 : RAG"""
    d = Drawing(500, 400)
    
    # Titre
    d.add(String(250, 380, "MODE 2 : RAG (AVEC PDF)", 
                fontSize=14, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    # USER - REQUÊTE UNIQUE
    d.add(Rect(30, 305, 110, 50, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=3))
    d.add(String(85, 345, "👤 USER", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(85, 332, "📄 Upload PDF +", fontSize=8, textAnchor='middle'))
    d.add(String(85, 322, "📝 Question texte", fontSize=8, textAnchor='middle'))
    d.add(String(85, 312, "MÊME REQUÊTE", fontSize=7, 
                fontName='Helvetica-Bold', textAnchor='middle',
                fillColor=colors.red))
    
    # Flèche vers processing
    d.add(Line(140, 330, 165, 330, strokeColor=colors.red, strokeWidth=3))
    d.add(Polygon([165, 334, 173, 330, 165, 326], 
                 fillColor=colors.red, strokeColor=None))
    
    # PROCESSING
    d.add(Rect(173, 305, 130, 55, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(238, 350, "⚙️ INDEXATION", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(238, 336, "1. Chunking (500 tokens)", fontSize=7, textAnchor='middle'))
    d.add(String(238, 326, "2. Embeddings (384d)", fontSize=7, textAnchor='middle'))
    d.add(String(238, 316, "3. Index FAISS", fontSize=7, textAnchor='middle'))
    d.add(String(238, 308, "⏱️ 3.5s", fontSize=7, 
                fontName='Helvetica-Bold', textAnchor='middle',
                fillColor=colors.red))
    
    # Flèche vers base vectorielle
    d.add(Line(238, 305, 238, 280, strokeColor=colors.red, strokeWidth=2))
    d.add(Polygon([234, 280, 238, 270, 242, 280], 
                 fillColor=colors.red, strokeColor=None))
    
    # BASE VECTORIELLE
    d.add(Rect(173, 230, 130, 40, fillColor=colors.HexColor('#d1ecf1'), 
               strokeColor=colors.HexColor('#17a2b8'), strokeWidth=2))
    d.add(String(238, 255, "🗄️ BASE VECTORIELLE", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(238, 240, "FAISS Index (67 chunks)", fontSize=8, textAnchor='middle'))
    
    # QUESTION (stockée)
    d.add(Rect(330, 305, 140, 30, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(400, 325, "💾 QUESTION STOCKÉE", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(400, 313, '"Rétinol + acide compatible?"', fontSize=7, 
                fontName='Helvetica-Oblique', textAnchor='middle'))
    
    # Flèche déclenchement (Question + Index prêt)
    d.add(Line(330, 250, 238, 230, strokeColor=colors.HexColor('#28a745'), 
              strokeWidth=2, strokeDashArray=[3, 3]))
    d.add(String(285, 242, "Déclenche", fontSize=7, textAnchor='middle',
                fillColor=colors.HexColor('#28a745')))
    
    # Flèche vers RAG Pipeline
    d.add(Line(238, 230, 238, 200, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([234, 200, 238, 190, 242, 200], 
                 fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # RAG PIPELINE
    d.add(Rect(168, 80, 140, 110, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(String(238, 182, "🔥 PIPELINE RAG", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.HexColor('#28a745')))
    
    # Sous-étapes
    d.add(String(238, 168, "4. RAG Fusion (3 variantes)", fontSize=7, textAnchor='middle'))
    d.add(Line(168, 163, 308, 163, strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    
    d.add(String(238, 153, "5. FAISS Search (15 chunks)", fontSize=7, textAnchor='middle'))
    d.add(Line(168, 148, 308, 148, strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    
    d.add(String(238, 138, "6. CrossEncoder (Top 3)", fontSize=7, textAnchor='middle'))
    d.add(Line(168, 133, 308, 133, strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    
    d.add(String(238, 123, "7. Build Prompt", fontSize=7, textAnchor='middle'))
    d.add(Line(168, 118, 308, 118, strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    
    d.add(String(238, 108, "8. Gemini Generate", fontSize=7, textAnchor='middle'))
    d.add(Line(168, 103, 308, 103, strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    
    d.add(String(238, 93, "9. Attach Sources", fontSize=7, textAnchor='middle'))
    d.add(Line(168, 88, 308, 88, strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    
    d.add(String(238, 85, "⏱️ Temps : 2.65s", fontSize=7, 
                fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.red))
    
    # Flèche vers réponse
    d.add(Line(308, 135, 345, 135, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([345, 139, 353, 135, 345, 131], 
                 fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # RÉPONSE FINALE
    d.add(Rect(353, 110, 117, 50, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(411, 145, "✅ RÉPONSE", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(411, 132, "+ 📎 SOURCES", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.HexColor('#ff8c00')))
    d.add(String(411, 118, "PDF + Page + §", fontSize=7, textAnchor='middle'))
    
    # TEMPS TOTAL
    d.add(Rect(330, 75, 140, 20, fillColor=colors.HexColor('#ffe6e6'), 
               strokeColor=colors.red, strokeWidth=2))
    d.add(String(400, 82, "⏱️ TOTAL : 6.15s (3.5s + 2.65s)", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='middle',
                fillColor=colors.red))
    
    # Caractéristiques
    d.add(Rect(30, 10, 220, 55, fillColor=colors.white, 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(50, 55, "✅ AVANTAGES :", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='start', 
                fillColor=colors.HexColor('#28a745')))
    d.add(String(50, 43, "• Upload + Question simultané", fontSize=7, textAnchor='start'))
    d.add(String(50, 33, "• Cite sources (100%)", fontSize=7, textAnchor='start'))
    d.add(String(50, 23, "• Précision 92%", fontSize=7, textAnchor='start'))
    d.add(String(50, 13, "• Une seule requête HTTP", fontSize=7, textAnchor='start'))
    
    d.add(Rect(270, 10, 200, 55, fillColor=colors.white, 
               strokeColor=colors.HexColor('#dc3545'), strokeWidth=2))
    d.add(String(290, 55, "⏱️ TIMING :", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='start', 
                fillColor=colors.HexColor('#dc3545')))
    d.add(String(290, 43, "• Indexation : 3.5s (unique)", fontSize=7, textAnchor='start'))
    d.add(String(290, 33, "• Pipeline RAG : 2.65s", fontSize=7, textAnchor='start'))
    d.add(String(290, 23, "• TOTAL : ~6 secondes", fontSize=7, textAnchor='start'))
    d.add(String(290, 13, "• Questions suivantes : 2.65s", fontSize=7, textAnchor='start'))
    
    return d

def create_mode3_schema():
    """Schéma Mode 3 : Multimodal"""
    d = Drawing(500, 350)
    
    # Titre
    d.add(String(250, 330, "MODE 3 : MULTIMODAL", 
                fontSize=16, fontName='Helvetica-Bold', 
                textAnchor='middle', fillColor=colors.HexColor('#1a5490')))
    
    # INPUTS multiples
    input_y = 250
    
    # Texte
    d.add(Rect(30, input_y, 80, 35, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(String(70, input_y+20, "📝 TEXTE", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(70, input_y+8, "Écrit/Collé", fontSize=7, textAnchor='middle'))
    
    # Audio
    d.add(Rect(120, input_y, 80, 35, fillColor=colors.HexColor('#fff3cd'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=2))
    d.add(String(160, input_y+20, "🎤 AUDIO", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(160, input_y+8, "Whisper STT", fontSize=7, textAnchor='middle'))
    
    # PDF
    d.add(Rect(210, input_y, 80, 35, fillColor=colors.HexColor('#f8d7da'), 
               strokeColor=colors.HexColor('#dc3545'), strokeWidth=2))
    d.add(String(250, input_y+20, "📄 PDF", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(250, input_y+8, "PyPDF2", fontSize=7, textAnchor='middle'))
    
    # DOCX
    d.add(Rect(300, input_y, 80, 35, fillColor=colors.HexColor('#d1ecf1'), 
               strokeColor=colors.HexColor('#17a2b8'), strokeWidth=2))
    d.add(String(340, input_y+20, "📑 DOCX", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(340, input_y+8, "docx lib", fontSize=7, textAnchor='middle'))
    
    # Image
    d.add(Rect(390, input_y, 80, 35, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(430, input_y+20, "🖼️ IMAGE", fontSize=9, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(430, input_y+8, "OCR Tesseract", fontSize=7, textAnchor='middle'))
    
    # Flèches convergentes vers processor
    for x_pos in [70, 160, 250, 340, 430]:
        d.add(Line(x_pos, input_y, 250, 200, strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    
    # UNIFIED PROCESSOR
    d.add(Rect(150, 170, 200, 50, fillColor=colors.HexColor('#ffd700'), 
               strokeColor=colors.HexColor('#ff8c00'), strokeWidth=3))
    d.add(String(250, 205, "⚙️ UNIFIED PROCESSOR", fontSize=11, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(250, 190, "Normalise tous inputs → Texte", fontSize=8, textAnchor='middle'))
    d.add(String(250, 177, "File detection → Handler adapté", fontSize=7, textAnchor='middle'))
    
    # Flèche vers choix mode
    d.add(Line(250, 170, 250, 145, strokeColor=colors.HexColor('#28a745'), strokeWidth=3))
    d.add(Polygon([246, 145, 250, 135, 254, 145], 
                 fillColor=colors.HexColor('#28a745'), strokeColor=None))
    
    # CHOIX MODE
    d.add(Rect(150, 95, 200, 40, fillColor=colors.HexColor('#e8f5e9'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(250, 120, "🔀 ROUTER", fontSize=10, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(250, 105, "Fichier uploadé? → RAG", fontSize=8, textAnchor='middle'))
    d.add(String(250, 97, "Texte seul? → Conversationnel", fontSize=8, textAnchor='middle'))
    
    # Flèches vers 2 modes
    # Vers conversationnel
    d.add(Line(150, 115, 90, 60, strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(Rect(30, 40, 120, 30, fillColor=colors.HexColor('#e7f3ff'), 
               strokeColor=colors.HexColor('#1a5490'), strokeWidth=2))
    d.add(String(90, 58, "MODE 1", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(90, 47, "Conversationnel", fontSize=7, textAnchor='middle'))
    
    # Vers RAG
    d.add(Line(350, 115, 410, 60, strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(Rect(350, 40, 120, 30, fillColor=colors.HexColor('#d4edda'), 
               strokeColor=colors.HexColor('#28a745'), strokeWidth=2))
    d.add(String(410, 58, "MODE 2", fontSize=8, 
                fontName='Helvetica-Bold', textAnchor='middle'))
    d.add(String(410, 47, "RAG Pipeline", fontSize=7, textAnchor='middle'))
    
    # Caractéristiques
    d.add(String(250, 20, "✅ Flexibilité totale : Parle, écris, upload docs, envoie photo → Même interface", 
                fontSize=9, fontName='Helvetica-Bold', textAnchor='middle', 
                fillColor=colors.HexColor('#28a745')))
    d.add(String(250, 8, "🎯 Use case : Photo d'étiquette cosmétique → OCR → RAG → Analyse ingrédients", 
                fontSize=8, fontName='Helvetica-Oblique', textAnchor='middle', 
                fillColor=colors.HexColor('#666666')))
    
    return d

def generate_schemas_pdf():
    filename = "SCHEMAS_3_MODES_CHATBOT.pdf"
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
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2e75b5'),
        spaceAfter=10,
        spaceBefore=10,
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
    story.append(Paragraph("SCHÉMAS VISUELS", title_style))
    story.append(Paragraph("Les 3 Modes du Chatbot RAG", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                       fontSize=14, alignment=TA_CENTER, 
                                       textColor=colors.HexColor('#666666'))))
    
    story.append(Spacer(1, 2*cm))
    
    # Table de comparaison
    comparison_data = [
        ['', 'Mode 1\nConversationnel', 'Mode 2\nRAG ⭐', 'Mode 3\nMultimodal'],
        ['Input', 'Texte seul', 'Texte + PDF\n(même requête)', 'Tout (Audio,\nImage, DOCX)'],
        ['Sources', '❌ Non', '✅ Oui (100%)', '✅ Oui (si PDF)'],
        ['Précision', '~70%', '92%', 'Dépend du mode'],
        ['Vitesse', '1-2s', '6.15s (1ère fois)\n2.65s (suivantes)', 'Variable'],
        ['Use Case', 'Questions\ngénérales', 'Analyse PDF\navec citations', 'Flexibilité\nmaximale']
    ]
    
    comparison_table = Table(comparison_data, colWidths=[3.5*cm, 4*cm, 4*cm, 4.5*cm])
    comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e7f3ff')),
        ('BACKGROUND', (2, 1), (2, -1), colors.HexColor('#fff3cd')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    story.append(comparison_table)
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("📄 Schémas détaillés ci-dessous ↓", 
                          ParagraphStyle('Note', parent=normal_style, 
                                       alignment=TA_CENTER, fontSize=11,
                                       textColor=colors.HexColor('#666666'),
                                       fontName='Helvetica-Oblique')))
    
    story.append(PageBreak())
    
    # Mode 1
    story.append(Paragraph("MODE 1 : CONVERSATIONNEL", heading_style))
    story.append(create_mode1_schema())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Le mode conversationnel classique : l'utilisateur pose une question, "
        "Gemini répond directement sans consulter de documents. Idéal pour "
        "des questions générales comme \"C'est quoi le rétinol ?\". Rapide (1-2s) "
        "mais sans garantie de sources.",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Mode 2
    story.append(Paragraph("MODE 2 : RAG (RETRIEVAL-AUGMENTED GENERATION) ⭐", heading_style))
    story.append(create_mode2_schema())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "<b>Le cœur de notre innovation :</b> L'utilisateur upload un PDF, le système "
        "l'indexe en 3.5s (chunking → embeddings → FAISS). Ensuite, chaque question "
        "déclenche un pipeline en 7 étapes (RAG Fusion, recherche vectorielle, "
        "reranking, génération) qui produit une réponse précise (92%) avec citations "
        "de sources (PDF, page, paragraphe). Temps de réponse : 2.65s. "
        "C'est ce mode qui nous différencie.",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Mode 3
    story.append(Paragraph("MODE 3 : MULTIMODAL", heading_style))
    story.append(create_mode3_schema())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Le mode flexible : accepte TOUS les types d'input (texte écrit, audio avec "
        "Whisper, PDF, DOCX, images avec OCR Tesseract). Un processeur unifié détecte "
        "le type de fichier et applique le handler approprié. Si un document est uploadé, "
        "le router active automatiquement le mode RAG. Si c'est juste du texte, il utilise "
        "le mode conversationnel. Idéal pour une expérience utilisateur fluide : "
        "parle, écris, upload photo d'étiquette → même interface.",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # Workflow complet
    story.append(Paragraph("WORKFLOW COMPLET : DE L'INPUT À LA RÉPONSE", heading_style))
    
    workflow_text = """
📱 ÉTAPE 1 : Utilisateur envoie requête
  → Texte seul : "C'est quoi le rétinol ?"
  → Texte + PDF : "Le rétinol est-il sûr ?" + Guide_Retinol.pdf
  → Audio / Image / DOCX (Mode 3)

⚙️ ÉTAPE 2 : Backend détecte le type
  → Fichier PDF présent ? → Traitement spécial
  → Texte seul ? → Direct à Gemini

🔀 ÉTAPE 3 : Routing automatique
  → PDF détecté → MODE 2 (RAG)
    • Indexation : 3.5s (unique)
    • Pipeline RAG : 2.65s
  → Texte seul → MODE 1 (Conversationnel)
    • Génération directe : 1-2s

🔥 ÉTAPE 4 : Traitement (MODE 2 si PDF)
  4.1. Chunking (500 tokens, overlap 100)
  4.2. Embeddings (384d Sentence-Transformers)
  4.3. FAISS Indexation (exhaustive L2)
  4.4. RAG Fusion (3 variantes de question)
  4.5. FAISS Search (Top 15 chunks)
  4.6. CrossEncoder Rerank (Top 3)
  4.7. Build Prompt (Contexte + Instructions)
  4.8. Gemini Generate (temp=0.3)
  4.9. Attach Sources (PDF + Page + §)

✅ ÉTAPE 5 : Réponse unique
  → Texte généré
  → Sources cliquables (si PDF)
  → Chunks surlignés visibles
  → UNE SEULE requête HTTP
"""
    
    story.append(Paragraph(
        workflow_text.replace('\n', '<br/>'),
        ParagraphStyle('Workflow', parent=normal_style, fontSize=9, 
                      fontName='Courier', leftIndent=20,
                      backColor=colors.HexColor('#f9f9f9'),
                      borderColor=colors.HexColor('#cccccc'),
                      borderWidth=1, borderPadding=10)
    ))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Comparaison performance
    story.append(Paragraph("COMPARAISON PERFORMANCES", heading_style))
    
    perf_data = [
        ['Critère', 'Mode 1', 'Mode 2 (RAG)', 'Mode 3'],
        ['Temps réponse', '1-2s ⚡', '2.65s', 'Variable'],
        ['Précision', '~70%', '92% ⭐', 'Dépend'],
        ['Sources citées', '0%', '100% ✅', '100% (si doc)'],
        ['Transparence', 'Faible', 'Totale ⭐', 'Totale (si doc)'],
        ['Coût compute', 'Bas', 'Moyen', 'Variable'],
        ['Setup requis', 'Aucun', 'Upload PDF', 'Aucun'],
        ['Use case idéal', 'Info générale', 'Analyse docs ⭐', 'Flexibilité']
    ]
    
    perf_table = Table(perf_data, colWidths=[4.5*cm, 3.5*cm, 4*cm, 4*cm])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e7f3ff')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    story.append(perf_table)
    
    story.append(Spacer(1, 1*cm))
    
    # Conclusion
    story.append(Paragraph(
        "🎯 <b>CONCLUSION :</b> Le Mode 2 (RAG) est notre innovation principale. "
        "Les Modes 1 et 3 offrent flexibilité et expérience utilisateur, mais "
        "c'est le pipeline RAG qui apporte précision (92%), transparence (100% sources), "
        "et confiance pour un usage médical/cosmétique.",
        ParagraphStyle('Conclusion', parent=normal_style, fontSize=11,
                      backColor=colors.HexColor('#fff3cd'),
                      borderColor=colors.HexColor('#ff8c00'),
                      borderWidth=2, borderPadding=10,
                      fontName='Helvetica')
    ))
    
    # Footer
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("_______________________________________________", 
                          ParagraphStyle('Line', parent=styles['Normal'], alignment=TA_CENTER)))
    story.append(Paragraph(
        f"<i>Schémas générés le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                      alignment=TA_CENTER, textColor=colors.grey)
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Schémas des 3 modes générés : {filename}")
    return filename

if __name__ == '__main__':
    generate_schemas_pdf()
