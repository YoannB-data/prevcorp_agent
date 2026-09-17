"""
Script de génération du corpus de documents synthétiques PrevCorp
38 documents PDF : conditions générales, fiches paramétrage, FAQ, notes techniques, circulaires
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUTPUT_DIR = "corpus"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Styles ───────────────────────────────────────────────────────────────────

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=16,
    spaceAfter=20,
    textColor=colors.HexColor("#1a3a5c"),
    alignment=TA_CENTER,
)
H1 = ParagraphStyle(
    "H1",
    parent=styles["Heading1"],
    fontSize=13,
    spaceBefore=14,
    spaceAfter=6,
    textColor=colors.HexColor("#1a3a5c"),
)
H2 = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontSize=11,
    spaceBefore=10,
    spaceAfter=4,
    textColor=colors.HexColor("#2e6da4"),
)
BODY = ParagraphStyle(
    "Body", parent=styles["Normal"], fontSize=9, spaceAfter=6, leading=14, alignment=TA_JUSTIFY
)
SMALL = ParagraphStyle(
    "Small", parent=styles["Normal"], fontSize=8, spaceAfter=4, textColor=colors.grey
)
HEADER_STYLE = ParagraphStyle("Header", parent=styles["Normal"], fontSize=8, textColor=colors.white)

TABLE_HEADER = colors.HexColor("#1a3a5c")
TABLE_ALT = colors.HexColor("#eef3f8")


def table_style(has_header=True):
    base = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TABLE_ALT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    if has_header:
        base += [
            ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
        ]
    return TableStyle(base)


def build_pdf(path, story):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )
    doc.build(story)


def header_block(doc_type, ref, date):
    data = [
        [
            Paragraph(
                "<b>PrevCorp Assurances</b>",
                ParagraphStyle("hb", fontSize=9, textColor=colors.HexColor("#1a3a5c")),
            ),
            Paragraph(
                f"{doc_type}<br/>Réf. {ref} — {date}",
                ParagraphStyle("hr", fontSize=8, textColor=colors.grey, alignment=2),
            ),
        ]
    ]
    t = Table(data, colWidths=[9 * cm, 9 * cm])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.8, colors.HexColor("#1a3a5c")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CONDITIONS GÉNÉRALES (10 docs)
# ═══════════════════════════════════════════════════════════════════════════════

PRODUITS = [
    (
        "PRV-IND-001",
        "Prévoyance Individuelle Essentiel",
        "Décès, Invalidité Permanente Totale, Incapacité Temporaire de Travail",
    ),
    (
        "PRV-IND-002",
        "Prévoyance Individuelle Confort",
        "Décès toutes causes, IPT, IPP, ITT, Rente Éducation",
    ),
    ("PRV-COL-001", "Prévoyance Collective Salariés", "Décès, IPT, ITT — conformité loi ANI"),
    (
        "PRV-COL-002",
        "Prévoyance Collective Cadres",
        "Décès toutes causes, IPT, ITT, maintien de salaire, Rente Conjoint",
    ),
    (
        "SAN-IND-001",
        "Complémentaire Santé Individuelle Essentiel",
        "Soins courants, Hospitalisation, Optique, Dentaire",
    ),
    (
        "SAN-IND-002",
        "Complémentaire Santé Individuelle Confort+",
        "Soins courants, Hospitalisation, Optique, Dentaire, Médecines douces",
    ),
    (
        "SAN-COL-001",
        "Complémentaire Santé Collective",
        "Panier de soins minimum ANI + options modulaires",
    ),
    ("DEP-001", "Dépendance Sérénité", "Perte d'autonomie partielle et totale — rente mensuelle"),
    ("OBQ-001", "Obsèques Premium", "Capital obsèques garanti, assistance rapatriement"),
    (
        "ACC-001",
        "Accidents de la Vie Garantie Famille",
        "Invalidité accidentelle, Décès accidentel, PTIA accidentelle",
    ),
]


def generate_cg(ref, nom_produit, garanties_principales, idx):
    story = []
    story.append(header_block("Conditions Générales", ref, "01/01/2024"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Conditions Générales", TITLE_STYLE))
    story.append(
        Paragraph(
            nom_produit,
            ParagraphStyle(
                "sous_titre",
                fontSize=13,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2e6da4"),
                spaceAfter=6,
            ),
        )
    )
    story.append(Paragraph(f"Référence produit : {ref}", SMALL))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("Article 1 — Objet du contrat", H1))
    story.append(
        Paragraph(
            f"Le présent contrat a pour objet de garantir l'assuré contre les risques liés à {garanties_principales.lower()}. "
            f"Il est régi par le Code des assurances et les dispositions des présentes Conditions Générales. "
            f"PrevCorp Assurances, ci-après dénommé « l'Assureur », s'engage à verser les prestations définies "
            f"aux présentes en contrepartie du paiement des cotisations par le souscripteur.",
            BODY,
        )
    )

    story.append(Paragraph("Article 2 — Définitions", H1))
    definitions = [
        ["Terme", "Définition"],
        ["Assuré", "Personne physique dont la vie ou l'état de santé est garanti par le contrat."],
        [
            "Souscripteur",
            "Personne physique ou morale qui adhère au contrat et en paie les cotisations.",
        ],
        [
            "Bénéficiaire",
            "Personne désignée pour recevoir les prestations en cas de réalisation du risque.",
        ],
        [
            "Sinistre",
            "Réalisation du risque garanti entraînant l'obligation de prestation de l'Assureur.",
        ],
        ["Cotisation", "Somme due par le souscripteur en contrepartie des garanties accordées."],
        [
            "Délai de carence",
            "Période suivant la prise d'effet du contrat pendant laquelle certaines garanties ne s'appliquent pas.",
        ],
        [
            "Franchise",
            "Période ou montant restant à la charge de l'assuré avant intervention de la garantie.",
        ],
    ]
    t = Table(definitions, colWidths=[4.5 * cm, 13.5 * cm])
    t.setStyle(table_style())
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("Article 3 — Garanties incluses", H1))
    story.append(
        Paragraph(
            f"Le présent contrat couvre les risques suivants : {garanties_principales}. "
            "Les montants de garantie, taux et franchises applicables sont définis dans les Conditions Particulières "
            "et les fiches de paramétrage associées à chaque garantie.",
            BODY,
        )
    )

    story.append(Paragraph("Article 4 — Exclusions générales", H1))
    exclusions = [
        "• Suicide au cours de la première année d'assurance.",
        "• Faits de guerre civile ou étrangère, émeutes et mouvements populaires.",
        "• Sinistres résultant de la pratique d'activités aériennes non commerciales.",
        "• Fraude ou fausse déclaration intentionnelle de l'assuré.",
        "• Sinistres survenus sous l'emprise d'alcool (taux légal dépassé) ou de stupéfiants.",
        "• Accidents survenus lors d'activités sportives à risque non déclarées (liste en annexe).",
    ]
    for ex in exclusions:
        story.append(Paragraph(ex, BODY))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("Article 5 — Prise d'effet et durée", H1))
    story.append(
        Paragraph(
            "Le contrat prend effet à la date indiquée aux Conditions Particulières, sous réserve du paiement "
            "de la première cotisation. Il est conclu pour une durée d'un an et se renouvelle tacitement, "
            "sauf résiliation dans les conditions prévues à l'article 9.",
            BODY,
        )
    )

    story.append(Paragraph("Article 6 — Cotisations", H1))
    story.append(
        Paragraph(
            "Les cotisations sont calculées selon les tarifs en vigueur à la date de souscription, "
            "en fonction de l'âge de l'assuré, des garanties choisies et de la situation professionnelle. "
            "Elles sont révisables chaque année à l'échéance anniversaire du contrat. "
            "En cas de non-paiement, les garanties sont suspendues après mise en demeure restée infructueuse "
            "pendant 30 jours.",
            BODY,
        )
    )

    story.append(Paragraph("Article 7 — Déclaration de sinistre", H1))
    story.append(
        Paragraph(
            "Tout sinistre doit être déclaré à l'Assureur dans les délais suivants à compter de sa survenance : "
            "5 jours ouvrés pour les sinistres décès, 30 jours pour les sinistres incapacité et invalidité. "
            "La déclaration doit être accompagnée des pièces justificatives listées à l'article 12.",
            BODY,
        )
    )

    story.append(Paragraph("Article 8 — Prescription", H1))
    story.append(
        Paragraph(
            "Toute action dérivant du présent contrat est prescrite par deux ans à compter de l'événement "
            "qui y donne naissance, conformément à l'article L. 114-1 du Code des assurances.",
            BODY,
        )
    )

    story.append(Paragraph("Article 9 — Résiliation", H1))
    story.append(
        Paragraph(
            "Le souscripteur peut résilier le contrat à l'échéance annuelle, avec un préavis de deux mois, "
            "ou dans les cas prévus par la loi Hamon (dans les 12 premiers mois) et la loi Châtel "
            "(en cas de hausse de cotisation). La résiliation prend effet à minuit le jour de l'échéance.",
            BODY,
        )
    )

    story.append(Paragraph("Article 10 — Loi applicable et juridiction", H1))
    story.append(
        Paragraph(
            "Le présent contrat est soumis au droit français. Tout litige relatif à son interprétation "
            "ou à son exécution sera soumis, à défaut d'accord amiable, à la compétence des tribunaux français.",
            BODY,
        )
    )

    build_pdf(os.path.join(OUTPUT_DIR, f"CG_{ref}.pdf"), story)
    print(f"  ✓ CG_{ref}.pdf")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FICHES PARAMÉTRAGE GARANTIES (12 docs)
# ═══════════════════════════════════════════════════════════════════════════════

GARANTIES = [
    {
        "ref": "GAR-DEC-001",
        "nom": "Garantie Décès Toutes Causes",
        "description": "Versement d'un capital au bénéficiaire désigné en cas de décès de l'assuré, quelle qu'en soit la cause.",
        "taux": [
            [
                "Tranche d'âge",
                "Capital minimum (€)",
                "Capital maximum (€)",
                "Taux de cotisation (% salaire)",
                "Délai de carence",
            ],
            ["18 – 29 ans", "10 000", "300 000", "0,08%", "Aucun"],
            ["30 – 39 ans", "10 000", "300 000", "0,12%", "Aucun"],
            ["40 – 49 ans", "10 000", "250 000", "0,19%", "Aucun"],
            ["50 – 59 ans", "10 000", "200 000", "0,31%", "Aucun"],
            ["60 – 65 ans", "10 000", "150 000", "0,52%", "Aucun"],
        ],
        "options": [
            ["Option", "Surprime", "Condition d'accès"],
            ["Double capital accidentel", "+0,04%", "Âge ≤ 60 ans"],
            ["Rente éducation incluse", "+0,06%", "Enfants à charge ≤ 25 ans"],
            ["Rente conjoint incluse", "+0,05%", "Conjoint non actif"],
        ],
    },
    {
        "ref": "GAR-IPT-001",
        "nom": "Garantie Invalidité Permanente Totale (IPT)",
        "description": "Versement d'un capital ou d'une rente lorsque l'assuré est reconnu invalide au taux de 66% ou plus par la Sécurité Sociale (2e ou 3e catégorie).",
        "taux": [
            [
                "Catégorie SS",
                "Taux d'invalidité",
                "Prestation",
                "Taux de cotisation (% salaire)",
                "Délai de carence",
            ],
            ["2e catégorie", "66% – 99%", "Capital = 80% du capital décès", "0,10%", "3 mois"],
            ["3e catégorie (PTIA)", "100%", "Capital = 100% du capital décès", "0,10%", "3 mois"],
        ],
        "options": [
            ["Option", "Surprime", "Condition"],
            ["Rente de remplacement de revenu", "+0,08%", "Âge ≤ 58 ans"],
            ["Exonération des cotisations", "Incluse", "Sur option PTIA uniquement"],
        ],
    },
    {
        "ref": "GAR-IPP-001",
        "nom": "Garantie Invalidité Permanente Partielle (IPP)",
        "description": "Versement d'un capital réduit pour les taux d'invalidité compris entre 33% et 66%.",
        "taux": [
            [
                "Taux d'invalidité",
                "Fraction du capital IPT versée",
                "Taux de cotisation (% salaire)",
                "Délai de carence",
            ],
            ["33% – 49%", "25% du capital IPT", "0,04%", "3 mois"],
            ["50% – 65%", "50% du capital IPT", "0,04%", "3 mois"],
        ],
        "options": [
            ["Option", "Surprime", "Condition"],
            ["Palier 25% dès 25% d'invalidité", "+0,02%", "Sur devis"],
        ],
    },
    {
        "ref": "GAR-ITT-001",
        "nom": "Garantie Incapacité Temporaire de Travail (ITT)",
        "description": "Versement d'indemnités journalières en cas d'arrêt de travail pour maladie ou accident, après épuisement des IJSS.",
        "taux": [
            [
                "Franchise",
                "IJ maximum (€/jour)",
                "Durée maximale (jours)",
                "Taux de cotisation (% salaire)",
                "Délai de carence",
            ],
            ["30 jours", "150", "1 095", "0,15%", "3 mois (maladie)"],
            ["60 jours", "200", "1 095", "0,11%", "3 mois (maladie)"],
            ["90 jours", "250", "1 095", "0,08%", "3 mois (maladie)"],
            ["180 jours", "300", "730", "0,05%", "3 mois (maladie)"],
        ],
        "options": [
            ["Option", "Surprime", "Condition"],
            ["Franchise 0 jour (accident uniquement)", "+0,03%", "Tous contrats"],
            ["Extension mi-temps thérapeutique", "+0,02%", "Tous contrats"],
            ["IJ maternité / paternité", "+0,01%", "Âge ≤ 45 ans"],
        ],
    },
    {
        "ref": "GAR-REN-001",
        "nom": "Garantie Rente Éducation",
        "description": "Versement d'une rente annuelle aux enfants à charge en cas de décès ou PTIA de l'assuré.",
        "taux": [
            [
                "Âge de l'enfant",
                "Rente annuelle (% du capital décès)",
                "Rente minimale (€/an)",
                "Rente maximale (€/an)",
                "Taux cotisation",
            ],
            ["0 – 10 ans", "5%", "600", "6 000", "0,05%"],
            ["11 – 17 ans", "7%", "900", "8 400", "0,05%"],
            ["18 – 25 ans (études)", "9%", "1 200", "10 800", "0,05%"],
        ],
        "options": [
            ["Option", "Surprime", "Condition"],
            ["Doublement rente orphelin de père et mère", "+0,02%", "Tous contrats"],
            ["Extension enfant handicapé (rente viagère)", "+0,04%", "Sur justificatif MDPH"],
        ],
    },
    {
        "ref": "GAR-RCJ-001",
        "nom": "Garantie Rente Conjoint",
        "description": "Versement d'une rente viagère au conjoint survivant en cas de décès de l'assuré.",
        "taux": [
            [
                "Tranche d'âge assuré",
                "Rente (% du salaire annuel brut)",
                "Taux cotisation (% salaire)",
                "Réversion possible",
            ],
            ["18 – 39 ans", "20%", "0,07%", "Oui (60%)"],
            ["40 – 54 ans", "20%", "0,11%", "Oui (60%)"],
            ["55 – 65 ans", "15%", "0,17%", "Oui (60%)"],
        ],
        "options": [
            ["Option", "Surprime", "Condition"],
            ["Réversion à 80%", "+0,03%", "Tous contrats"],
            ["Annuités garanties (10 ans minimum)", "+0,02%", "Tous contrats"],
        ],
    },
    {
        "ref": "GAR-OPT-001",
        "nom": "Garantie Optique",
        "description": "Prise en charge des frais optiques (montures, verres correcteurs, lentilles) en complément de la Sécurité Sociale.",
        "taux": [
            [
                "Formule",
                "Monture (€)",
                "Verres simples (€/verre)",
                "Verres complexes (€/verre)",
                "Lentilles (€/an)",
                "Fréquence",
            ],
            ["Essentiel", "30", "70", "120", "100", "1 équipement / 2 ans"],
            ["Confort", "60", "100", "180", "200", "1 équipement / 2 ans"],
            ["Confort+", "90", "140", "250", "300", "1 équipement / an"],
            ["Premium", "150", "200", "350", "400", "1 équipement / an"],
        ],
        "options": [
            ["Option", "Surprime mensuelle", "Condition"],
            ["Chirurgie réfractive (LASIK)", "+2,00 €/mois", "Tous contrats"],
            ["Verres progressifs remboursés à 100%", "+1,50 €/mois", "Formules Confort+/Premium"],
        ],
    },
    {
        "ref": "GAR-DEN-001",
        "nom": "Garantie Dentaire",
        "description": "Prise en charge des soins dentaires en complément de la Sécurité Sociale, dans le cadre du dispositif 100% Santé.",
        "taux": [
            [
                "Type de soin",
                "Remboursement SS (%)",
                "Remboursement complémentaire",
                "Reste à charge 100% Santé",
            ],
            ["Soins conservateurs", "70%", "30%", "0 €"],
            ["Prothèses panier 100% Santé", "70%", "30%", "0 €"],
            ["Prothèses hors panier — Classe I", "70%", "Jusqu'au plafond Classe I", "Variable"],
            ["Prothèses hors panier — Classe II", "70%", "Jusqu'au plafond Classe II", "Variable"],
            ["Orthodontie enfant (avant 16 ans)", "100% (6 semestres)", "Selon devis", "Variable"],
            ["Implants dentaires", "Non remboursé SS", "100 € – 400 € par implant", "Variable"],
        ],
        "options": [
            ["Option", "Surprime mensuelle", "Condition"],
            [
                "Implants : remboursement étendu (800 €)",
                "+3,00 €/mois",
                "Formules Confort+/Premium",
            ],
            ["Orthodontie adulte (jusqu'à 150 €/semestre)", "+2,50 €/mois", "Tous contrats"],
        ],
    },
    {
        "ref": "GAR-HOS-001",
        "nom": "Garantie Hospitalisation",
        "description": "Prise en charge du ticket modérateur, du forfait journalier hospitalier et des dépassements d'honoraires en cas d'hospitalisation.",
        "taux": [
            [
                "Poste",
                "Formule Essentiel",
                "Formule Confort",
                "Formule Confort+",
                "Formule Premium",
            ],
            ["Ticket modérateur", "100%", "100%", "100%", "100%"],
            ["Forfait journalier (23 €/j)", "100%", "100%", "100%", "100%"],
            ["Dépassements honoraires secteur 2", "0%", "100% BRSS", "200% BRSS", "300% BRSS"],
            ["Chambre particulière (€/nuit)", "0 €", "40 €", "70 €", "100 €"],
            ["Lit accompagnant (€/nuit)", "0 €", "20 €", "40 €", "60 €"],
            ["Transport médicalisé", "Légal", "100%", "100%", "100%"],
        ],
        "options": [
            ["Option", "Surprime mensuelle", "Condition"],
            ["Assistance retour domicile après hospit.", "Incluse", "Tous contrats"],
            ["Médecine douce (acupuncture, ostéo…)", "+4,00 €/mois", "Formules Confort+/Premium"],
        ],
    },
    {
        "ref": "GAR-DEP-001",
        "nom": "Garantie Dépendance",
        "description": "Versement d'une rente mensuelle en cas de perte d'autonomie partielle (GIR 3-4) ou totale (GIR 1-2).",
        "taux": [
            [
                "Niveau de dépendance",
                "GIR",
                "Rente mensuelle (% de la rente totale)",
                "Taux cotisation (€/mois)",
                "Délai de carence",
            ],
            ["Dépendance partielle", "GIR 3 – 4", "50%", "15 – 45 €", "3 ans"],
            ["Dépendance totale", "GIR 1 – 2", "100%", "25 – 80 €", "3 ans"],
        ],
        "options": [
            ["Option", "Surprime mensuelle", "Condition"],
            ["Revalorisation rente (2%/an)", "+10% de la cotisation", "Tous contrats"],
            ["Aide à domicile incluse (20h/mois)", "+8,00 €/mois", "Dépendance totale uniquement"],
            ["Aménagement logement (capital 3 000 €)", "+5,00 €/mois", "Tous contrats"],
        ],
    },
    {
        "ref": "GAR-OBQ-001",
        "nom": "Garantie Obsèques",
        "description": "Versement d'un capital garanti destiné à couvrir les frais d'obsèques, avec assistance rapatriement de corps.",
        "taux": [
            [
                "Formule",
                "Capital garanti (€)",
                "Cotisation mensuelle (< 60 ans)",
                "Cotisation mensuelle (60 – 75 ans)",
                "Franchise",
            ],
            ["Essentiel", "3 000", "8,00 €", "15,00 €", "Aucune"],
            ["Confort", "5 000", "12,00 €", "23,00 €", "Aucune"],
            ["Premium", "8 000", "18,00 €", "36,00 €", "Aucune"],
            ["Premium+", "12 000", "25,00 €", "52,00 €", "Aucune"],
        ],
        "options": [
            ["Option", "Surprime", "Condition"],
            ["Rapatriement international inclus", "+2,00 €/mois", "Tous contrats"],
            ["Aide aux démarches administratives", "Incluse", "Tous contrats"],
        ],
    },
    {
        "ref": "GAR-ACC-001",
        "nom": "Garantie Accidents de la Vie",
        "description": "Indemnisation des accidents de la vie privée ayant entraîné une incapacité permanente d'au moins 5%.",
        "taux": [
            [
                "Taux d'incapacité permanente",
                "Indemnisation (€)",
                "Délai de règlement",
                "Taux cotisation mensuelle",
            ],
            ["5% – 14%", "Barème progressif (min. 500 €)", "30 jours", "4,00 €"],
            ["15% – 29%", "Barème progressif", "30 jours", "4,00 €"],
            ["30% – 65%", "Jusqu'à 500 000 €", "45 jours", "4,00 €"],
            ["> 66% (PTIA)", "1 000 000 €", "45 jours", "4,00 €"],
            ["Décès accidentel", "Capital décès doublé", "30 jours", "Inclus"],
        ],
        "options": [
            ["Option", "Surprime mensuelle", "Condition"],
            [
                "Extension accidents sportifs à risque",
                "+2,50 €/mois",
                "Liste d'activités éligibles",
            ],
            ["Assistance psychologique (10 séances)", "Incluse", "Tous contrats"],
        ],
    },
]


def generate_fiche_garantie(g):
    story = []
    story.append(header_block("Fiche de Paramétrage Garantie", g["ref"], "01/01/2024"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Fiche de Paramétrage Garantie", TITLE_STYLE))
    story.append(
        Paragraph(
            g["nom"],
            ParagraphStyle(
                "sous_titre",
                fontSize=13,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2e6da4"),
                spaceAfter=6,
            ),
        )
    )
    story.append(Paragraph(f"Référence : {g['ref']} — Version 2024.1", SMALL))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("1. Description de la garantie", H1))
    story.append(Paragraph(g["description"], BODY))

    story.append(Paragraph("2. Barème de cotisations et de prestations", H1))
    t = Table(g["taux"], repeatRows=1)
    col_count = len(g["taux"][0])
    col_w = 18 * cm / col_count
    t._argW = [col_w] * col_count
    t.setStyle(table_style())
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("3. Options et surprimes", H1))
    t2 = Table(g["options"], repeatRows=1)
    col_count2 = len(g["options"][0])
    col_w2 = 18 * cm / col_count2
    t2._argW = [col_w2] * col_count2
    t2.setStyle(table_style())
    story.append(t2)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("4. Règles de cumul et exclusions spécifiques", H1))
    story.append(
        Paragraph(
            f"La garantie {g['nom']} ne peut être souscrite qu'en complément d'une garantie Décès de base. "
            "Elle ne se cumule pas avec une couverture équivalente souscrite dans le cadre d'un autre contrat "
            "PrevCorp couvrant le même risque. En cas de sinistre, l'assuré doit fournir les pièces justificatives "
            "requises dans les délais prévus aux Conditions Générales.",
            BODY,
        )
    )

    story.append(Paragraph("5. Tarification individuelle — facteurs de modulation", H1))
    modulation_data = [
        ["Facteur", "Impact sur la cotisation", "Condition d'application"],
        ["Âge > 55 ans", "+20% à +50%", "Automatique"],
        ["Profession à risque (liste A)", "+15%", "Sur questionnaire médical"],
        ["Profession à risque (liste B)", "+30%", "Sur questionnaire médical"],
        ["Antécédents médicaux déclarés", "Sur devis médical", "Questionnaire de santé"],
        ["Franchise élevée choisie", "-5% à -20%", "Selon franchise retenue"],
        ["Multi-contrats PrevCorp (≥ 2)", "-5%", "Automatique si adhésion simultanée"],
    ]
    t3 = Table(modulation_data, colWidths=[5 * cm, 5 * cm, 8 * cm])
    t3.setStyle(table_style())
    story.append(t3)

    build_pdf(os.path.join(OUTPUT_DIR, f"FICHE_{g['ref']}.pdf"), story)
    print(f"  ✓ FICHE_{g['ref']}.pdf")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. FAQ GESTIONNAIRE (6 docs)
# ═══════════════════════════════════════════════════════════════════════════════

FAQS = [
    {
        "ref": "FAQ-GES-001",
        "titre": "FAQ Gestion des Sinistres Décès",
        "questions": [
            (
                "Quels documents sont nécessaires pour déclarer un sinistre décès ?",
                "Le dossier de décès doit comporter : (1) l'acte de décès original, (2) le certificat médical indiquant la cause du décès, "
                "(3) une copie de la carte d'identité du défunt, (4) le RIB du bénéficiaire désigné, (5) le contrat d'assurance. "
                "En cas de décès accidentel, joindre le procès-verbal de police ou le rapport d'accident.",
            ),
            (
                "Dans quel délai doit-on déclarer un sinistre décès ?",
                "Le sinistre décès doit être déclaré dans un délai de 5 jours ouvrés à compter du décès. "
                "Ce délai peut être porté à 10 jours ouvrés en cas de difficultés dûment justifiées "
                "(éloignement géographique, situation d'urgence familiale). Passé ce délai, l'Assureur peut appliquer "
                "une pénalité de 10% sur le capital versé.",
            ),
            (
                "Comment est calculé le capital décès si l'assuré avait plusieurs bénéficiaires désignés ?",
                "Le capital décès est réparti entre les bénéficiaires selon les quotités indiquées dans la clause bénéficiaire. "
                "Si aucune quotité n'est précisée, le capital est réparti à parts égales. "
                "En l'absence de bénéficiaire désigné vivant, le capital revient aux héritiers selon les règles légales de dévolution.",
            ),
            (
                "Que se passe-t-il si le bénéficiaire désigné est décédé avant l'assuré ?",
                "Si le bénéficiaire de premier rang est décédé, le capital est versé au bénéficiaire de second rang "
                "si la clause bénéficiaire en prévoit un. À défaut, le capital intègre la succession de l'assuré. "
                "Il est fortement recommandé de mettre à jour la clause bénéficiaire régulièrement.",
            ),
            (
                "Le sinistre peut-il être refusé en cas de fausse déclaration médicale à la souscription ?",
                "Oui. En cas de fausse déclaration intentionnelle lors de la souscription (art. L. 113-8 du Code des assurances), "
                "le contrat est nul et aucune prestation n'est due. En cas d'omission non intentionnelle, "
                "l'indemnité est réduite en proportion des cotisations payées par rapport à celles qui auraient dû être perçues.",
            ),
        ],
    },
    {
        "ref": "FAQ-GES-002",
        "titre": "FAQ Gestion des Arrêts de Travail (ITT)",
        "questions": [
            (
                "Quelles pièces faut-il fournir pour déclencher les indemnités journalières ITT ?",
                "Pour la première déclaration : (1) certificat médical d'arrêt de travail signé par le médecin, "
                "(2) décompte CPAM attestant la date de début des IJSS, (3) attestation employeur (salaire de référence), "
                "(4) RIB. Pour les prolongations : uniquement le certificat médical de prolongation.",
            ),
            (
                "À partir de quand les indemnités journalières sont-elles versées ?",
                "Les IJ sont versées après épuisement de la franchise contractuelle (30, 60, 90 ou 180 jours selon contrat). "
                "La franchise est comptée en jours calendaires consécutifs d'arrêt. "
                "Attention : la franchise repart à zéro si l'arrêt est interrompu plus de 30 jours.",
            ),
            (
                "Comment est calculée l'indemnité journalière en cas de temps partiel thérapeutique ?",
                "En cas de mi-temps thérapeutique, l'IJ versée est réduite proportionnellement à la reprise d'activité. "
                "Exemple : reprise à 50% = IJ réduite de 50%. Cette réduction s'applique uniquement si l'option "
                "mi-temps thérapeutique a été souscrite. Sans cette option, aucune IJ n'est versée pendant la reprise partielle.",
            ),
            (
                "Quelle est la durée maximale d'indemnisation ITT ?",
                "La durée maximale d'indemnisation est de 1 095 jours (3 ans) pour les franchises 30, 60 et 90 jours, "
                "et de 730 jours (2 ans) pour la franchise 180 jours. Au-delà, si l'incapacité persiste, "
                "un examen d'invalidité est déclenché automatiquement.",
            ),
        ],
    },
    {
        "ref": "FAQ-GES-003",
        "titre": "FAQ Gestion des Contrats Collectifs",
        "questions": [
            (
                "Comment gérer l'adhésion d'un nouveau salarié à un contrat collectif ?",
                "L'adhésion d'un nouveau salarié doit être déclarée dans les 30 jours suivant l'embauche. "
                "Au-delà, une déclaration tardive entraîne l'application d'un délai de carence spécifique de 3 mois. "
                "La déclaration se fait via l'espace employeur en ligne ou par envoi du bulletin d'affiliation.",
            ),
            (
                "Comment procéder à la radiation d'un salarié (départ de l'entreprise) ?",
                "La radiation doit être déclarée dans les 15 jours suivant le départ (démission, licenciement, retraite). "
                "L'assuré conserve le bénéfice de la portabilité prévue par l'ANI pendant une durée égale à la durée "
                "du dernier contrat de travail, dans la limite de 12 mois.",
            ),
            (
                "La portabilité s'applique-t-elle en cas de rupture de période d'essai ?",
                "Non. La portabilité ne s'applique qu'aux contrats de travail d'une durée minimale d'un mois. "
                "Une rupture de période d'essai, quelle qu'en soit la durée, n'ouvre pas droit à la portabilité.",
            ),
            (
                "Comment est gérée la hausse de cotisation annuelle pour un contrat collectif ?",
                "La hausse de cotisation est notifiée à l'employeur 2 mois avant l'échéance annuelle. "
                "L'employeur dispose de 30 jours pour accepter ou contester. En cas de contestation non résolue, "
                "le contrat est résilié à l'échéance dans les conditions de l'article 9 des CG.",
            ),
        ],
    },
    {
        "ref": "FAQ-GES-004",
        "titre": "FAQ Gestion des Cotisations et Paiements",
        "questions": [
            (
                "Quels sont les modes de paiement acceptés ?",
                "Les cotisations peuvent être réglées par prélèvement automatique (SEPA), virement bancaire, "
                "ou chèque (pour les contrats individuels uniquement). Le prélèvement automatique est fortement recommandé "
                "pour éviter les risques de suspension de garanties.",
            ),
            (
                "Que se passe-t-il en cas de rejet de prélèvement ?",
                "En cas de premier rejet, une relance automatique est effectuée sous 5 jours ouvrés. "
                "Si le second prélèvement échoue, une mise en demeure est adressée. Sans régularisation sous 30 jours, "
                "les garanties sont suspendues. Un second rejet entraîne des frais de rejet de 7,50 €.",
            ),
            (
                "Comment modifier les coordonnées bancaires pour le prélèvement ?",
                "La modification des coordonnées bancaires s'effectue via l'espace assuré en ligne ou par courrier "
                "avec un nouveau RIB original. La modification prend effet sur le prélèvement suivant, "
                "à condition d'être reçue au moins 10 jours avant la date d'échéance.",
            ),
        ],
    },
    {
        "ref": "FAQ-GES-005",
        "titre": "FAQ Gestion des Invalides et Rentes",
        "questions": [
            (
                "Comment est calculée la rente d'invalidité ?",
                "La rente d'invalidité est calculée sur la base du salaire annuel brut de référence (moyenne des 12 derniers mois), "
                "multipliée par le taux de rente prévu aux Conditions Particulières. "
                "Elle est versée mensuellement et revalorisée chaque année selon l'indice prévu au contrat.",
            ),
            (
                "La rente d'invalidité est-elle imposable ?",
                "Les rentes d'invalidité versées dans le cadre d'un contrat de prévoyance collectif (art. 83 CGI) "
                "sont imposables au titre des pensions et rentes. Pour les contrats individuels, "
                "le régime fiscal dépend de la nature des cotisations (déductibles ou non). Conseiller l'assuré de "
                "se rapprocher de son conseiller fiscal.",
            ),
            (
                "Que se passe-t-il si l'invalide reprend une activité professionnelle ?",
                "En cas de reprise d'activité, l'assuré doit en informer l'Assureur dans les 15 jours. "
                "La rente est alors suspendue ou réduite proportionnellement aux revenus perçus, "
                "selon les modalités prévues aux CG. Le taux d'invalidité est réévalué annuellement.",
            ),
        ],
    },
    {
        "ref": "FAQ-GES-006",
        "titre": "FAQ Gestion des Réclamations et Litiges",
        "questions": [
            (
                "Comment un assuré peut-il contester une décision de refus ?",
                "Toute contestation doit être adressée par écrit au Service Réclamations de PrevCorp. "
                "Un accusé de réception est envoyé sous 10 jours et une réponse définitive sous 60 jours. "
                "Si le litige persiste, l'assuré peut saisir le Médiateur de l'Assurance (gratuit et indépendant).",
            ),
            (
                "Quelles sont les voies de recours après la médiation ?",
                "Si la médiation n'aboutit pas, l'assuré peut saisir les tribunaux compétents. "
                "Pour les contrats individuels : Tribunal Judiciaire du domicile de l'assuré. "
                "Pour les contrats collectifs : Tribunal de Grande Instance du siège social de l'employeur.",
            ),
            (
                "Comment éviter les prescriptions lors d'un litige en cours ?",
                "La prescription biennale (art. L. 114-1 Code des assurances) est interrompue par toute lettre "
                "recommandée adressée à l'Assureur, ou par la saisine du médiateur. "
                "Il est fortement conseillé d'envoyer les courriers en LRAR et de conserver les accusés de réception.",
            ),
        ],
    },
]


def generate_faq(faq):
    story = []
    story.append(header_block("FAQ Gestionnaire", faq["ref"], "Mise à jour : 01/03/2024"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("FAQ Gestionnaire", TITLE_STYLE))
    story.append(
        Paragraph(
            faq["titre"],
            ParagraphStyle(
                "sous_titre",
                fontSize=13,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2e6da4"),
                spaceAfter=6,
            ),
        )
    )
    story.append(Paragraph(f"Référence : {faq['ref']}", SMALL))
    story.append(Spacer(1, 0.3 * cm))

    for i, (q, a) in enumerate(faq["questions"], 1):
        story.append(Paragraph(f"Q{i}. {q}", H2))
        story.append(Paragraph(a, BODY))
        story.append(Spacer(1, 0.2 * cm))

    build_pdf(os.path.join(OUTPUT_DIR, f"FAQ_{faq['ref']}.pdf"), story)
    print(f"  ✓ FAQ_{faq['ref']}.pdf")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. NOTES TECHNIQUES (6 docs)
# ═══════════════════════════════════════════════════════════════════════════════

NOTES_TECHNIQUES = [
    {
        "ref": "NT-001",
        "titre": "Règles de calcul des cotisations prévoyance collective",
        "objet": "Définir les règles de calcul applicables aux cotisations des contrats de prévoyance collective ANI.",
        "contenu": [
            (
                "Base de calcul",
                "La cotisation est calculée sur la Tranche A (TA) et la Tranche B (TB) du salaire brut. "
                "Tranche A : de 0 à 1 PASS (46 368 € en 2024). Tranche B : de 1 à 4 PASS. "
                "Tranche C (au-delà de 4 PASS) : applicable uniquement aux contrats Cadres+.",
            ),
            (
                "Formule de cotisation",
                "Cotisation mensuelle = (Salaire TA × Taux TA) + (Salaire TB × Taux TB). "
                "Les taux TA et TB sont définis dans les Conditions Particulières selon la formule choisie. "
                "Exemple : Taux TA = 0,50%, Taux TB = 0,75%, salaire = 4 000 € (TA entière) → cotisation = 20,00 €/mois.",
            ),
            (
                "Répartition employeur/salarié",
                "La répartition légale minimale est 50% employeur / 50% salarié pour les non-cadres "
                "et 1,5% PMSS employeur pour les cadres (AGIRC). La répartition effective est précisée en Conditions Particulières.",
            ),
            (
                "Régularisation annuelle",
                "En fin d'année, une régularisation des cotisations est effectuée sur la base "
                "du salaire réel annuel définitif. Les écarts < 5 € par salarié sont absorbés sans régularisation.",
            ),
        ],
    },
    {
        "ref": "NT-002",
        "titre": "Délais de carence — règles d'application",
        "objet": "Préciser les règles d'application des délais de carence pour chaque type de garantie.",
        "contenu": [
            (
                "Définition",
                "Le délai de carence est la période qui suit la prise d'effet du contrat pendant laquelle "
                "certaines garanties ne couvrent pas les sinistres survenus ou déclarés. Il ne s'applique pas aux accidents.",
            ),
            (
                "Délais par garantie",
                "Décès : aucun délai de carence sauf suicide (1 an). "
                "ITT pour maladie : 3 mois de carence standard. IPT/IPP : 3 mois. Dépendance : 3 ans. "
                "Maternité : 10 mois à compter de la souscription.",
            ),
            (
                "Exceptions",
                "Le délai de carence est supprimé en cas de souscription dans les 30 jours suivant "
                "un déménagement, une naissance ou un mariage. Il est également supprimé pour les contrats collectifs "
                "lors de la première adhésion de l'entreprise si 75% des salariés éligibles adhèrent.",
            ),
            (
                "Cas du sinistre en cours de carence",
                "Si un arrêt de travail débute pendant le délai de carence, "
                "aucune indemnité n'est versée, même si l'arrêt se prolonge au-delà. La date de survenance "
                "du sinistre fait foi, pas la date de fin du délai de carence.",
            ),
        ],
    },
    {
        "ref": "NT-003",
        "titre": "Calcul du taux d'invalidité — méthode PrevCorp",
        "objet": "Décrire la méthode de calcul du taux d'invalidité fonctionnelle utilisée par PrevCorp pour la gestion des sinistres IPT/IPP.",
        "contenu": [
            (
                "Référence médicale",
                "PrevCorp utilise le Barème Indicatif d'Invalidité des Accidents du Droit Commun "
                "(BIIADC) pour les contrats accidents, et le taux d'invalidité de la Sécurité Sociale pour les contrats maladie. "
                "En cas de divergence > 10 points entre les deux évaluations, un médecin arbitre est nommé.",
            ),
            (
                "Taux fonctionnel vs professionnel",
                "Le taux d'invalidité contractuel est le taux fonctionnel "
                "(capacité physique globale), non le taux professionnel. Exception : contrats 'invalidité professionnelle' "
                "spécifiques qui couvrent l'impossibilité d'exercer la profession habituelle.",
            ),
            (
                "Invalidité partielle — calcul de la prestation",
                "Pour les taux compris entre 33% et 66% : "
                "Prestation = Capital IPT × (Taux_invalidité − 33%) / 33%. "
                "Exemple : taux 50% → Prestation = Capital × (50−33)/33 = 51,5% du capital IPT.",
            ),
            (
                "Révision du taux",
                "Le taux d'invalidité est révisable à la demande de l'Assureur ou de l'assuré "
                "tous les 2 ans, jusqu'à l'âge de 60 ans. Au-delà, le taux est figé sauf aggravation déclarée.",
            ),
        ],
    },
    {
        "ref": "NT-004",
        "titre": "Règles de revalorisation des rentes et capitaux",
        "objet": "Définir les modalités de revalorisation annuelle des prestations versées sous forme de rentes.",
        "contenu": [
            (
                "Indice de référence",
                "Les rentes viagères (rente conjoint, rente éducation, rente dépendance) "
                "sont revalorisées chaque 1er janvier selon l'évolution de l'Indice des Prix à la Consommation (IPC) "
                "hors tabac publié par l'INSEE, tel que constaté en novembre de l'année précédente.",
            ),
            (
                "Plafonnement",
                "La revalorisation annuelle est plafonnée à 3% par an pour les rentes inférieures à 500 €/mois, "
                "et à 2% par an pour les rentes supérieures à 500 €/mois. "
                "En cas d'IPC négatif, aucune revalorisation n'est appliquée (plancher à 0%).",
            ),
            (
                "Revalorisation des capitaux",
                "Les capitaux décès et invalidité ne sont pas revalorisés entre la souscription "
                "et le sinistre. La garantie est fixe, sauf avenant modificatif souscrit par l'assuré.",
            ),
            (
                "Option revalorisation contractuelle",
                "Pour les contrats avec l'option 'revalorisation garantie de 2%/an', "
                "la revalorisation s'applique indépendamment de l'IPC, y compris en cas d'IPC négatif.",
            ),
        ],
    },
    {
        "ref": "NT-005",
        "titre": "Portabilité ANI — conditions et durée",
        "objet": "Préciser les règles de portabilité de la couverture prévoyance et santé collective en cas de cessation du contrat de travail.",
        "contenu": [
            (
                "Bénéficiaires",
                "La portabilité bénéficie aux anciens salariés dont la cessation du contrat de travail "
                "ouvre droit à l'assurance chômage (ARE). Sont exclus : démissions sauf cas légaux, ruptures de période d'essai, "
                "fins de CDD < 1 mois, départs à la retraite volontaires.",
            ),
            (
                "Durée",
                "La durée de la portabilité est égale à la durée du dernier contrat de travail, "
                "dans la limite de 12 mois. Exemple : CDI de 3 ans rompu → portabilité 12 mois maximum. "
                "CDD de 8 mois → portabilité 8 mois.",
            ),
            (
                "Financement",
                "La portabilité est financée par mutualisation sur l'ensemble des cotisants actifs du contrat. "
                "Aucune cotisation supplémentaire n'est due par l'ancien salarié ni par l'ancien employeur.",
            ),
            (
                "Fin de portabilité",
                "La portabilité cesse automatiquement à la reprise d'un emploi "
                "(avec ou sans nouvelle couverture collective), à la fin des droits à l'ARE, ou à l'issue de la durée maximale.",
            ),
        ],
    },
    {
        "ref": "NT-006",
        "titre": "Traitement des questionnaires médicaux",
        "objet": "Décrire les règles d'acceptation, de sélection médicale et de tarification médicale applicables aux contrats individuels.",
        "contenu": [
            (
                "Seuils de franchise médicale",
                "Un questionnaire médical simplifié est requis pour tout capital décès > 150 000 €. "
                "Un questionnaire médical complet est requis au-delà de 300 000 €. "
                "En dessous de 150 000 €, la souscription est simplifiée (déclaration sur l'honneur uniquement).",
            ),
            (
                "Délai de traitement",
                "Les dossiers avec questionnaire simplifié sont traités sous 48h. "
                "Les dossiers avec questionnaire médical complet sont soumis au médecin-conseil dans un délai de 10 jours ouvrés. "
                "Passé 30 jours sans réponse, le dossier est automatiquement accepté aux conditions standard.",
            ),
            (
                "Exclusions et surprimes médicales",
                "En cas de risque aggravé, l'Assureur peut : "
                "(1) appliquer une surprime (maximum 200% de la prime standard), "
                "(2) exclure spécifiquement un risque (maladie préexistante), "
                "(3) refuser la souscription. Le refus doit être motivé par écrit.",
            ),
            (
                "Confidentialité",
                "Les données médicales sont traitées dans le strict respect du secret médical. "
                "Elles ne sont accessibles qu'au médecin-conseil de l'Assureur et ne sont jamais transmises aux gestionnaires non-médicaux.",
            ),
        ],
    },
]


def generate_note_technique(nt):
    story = []
    story.append(header_block("Note Technique Interne", nt["ref"], "01/01/2024"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Note Technique Interne", TITLE_STYLE))
    story.append(
        Paragraph(
            nt["titre"],
            ParagraphStyle(
                "sous_titre",
                fontSize=13,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2e6da4"),
                spaceAfter=6,
            ),
        )
    )
    story.append(
        Paragraph(f"Référence : {nt['ref']} — Usage interne — Diffusion restreinte", SMALL)
    )
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("Objet", H1))
    story.append(Paragraph(nt["objet"], BODY))
    story.append(Spacer(1, 0.2 * cm))

    for titre_section, texte in nt["contenu"]:
        story.append(Paragraph(titre_section, H2))
        story.append(Paragraph(texte, BODY))

    build_pdf(os.path.join(OUTPUT_DIR, f"NT_{nt['ref']}.pdf"), story)
    print(f"  ✓ NT_{nt['ref']}.pdf")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. CIRCULAIRES (4 docs)
# ═══════════════════════════════════════════════════════════════════════════════

CIRCULAIRES = [
    {
        "ref": "CIRC-2024-001",
        "titre": "Revalorisation des barèmes de cotisations — Exercice 2024",
        "destinataires": "Tous gestionnaires de contrats individuels et collectifs",
        "objet": "Informer les équipes des nouvelles grilles tarifaires applicables au 1er janvier 2024.",
        "corps": [
            (
                "Contexte",
                "Suite à la revue actuarielle annuelle et à l'évolution de la sinistralité observée "
                "sur l'exercice 2023, PrevCorp procède à une révision de ses barèmes de cotisations. "
                "Cette révision s'inscrit dans le cadre de la politique de tarification prudente définie "
                "par la Direction Technique.",
            ),
            (
                "Modifications tarifaires principales",
                "Garantie Décès (toutes formules) : +3,5% en moyenne. "
                "Garantie ITT franchise 30 jours : +5,0% (sinistralité ITT en hausse de 8% sur 2023). "
                "Garantie Dépendance : +2,0%. Garantie Obsèques : stable. "
                "Complémentaire Santé (optique et dentaire) : +4,2%.",
            ),
            (
                "Application",
                "Les nouveaux tarifs s'appliquent aux nouvelles souscriptions à compter du 01/01/2024 "
                "et aux contrats existants à leur prochaine échéance annuelle. "
                "Les assurés sont informés par courrier avec un préavis de 2 mois.",
            ),
            (
                "Procédure de résiliation",
                "Les assurés dont la hausse dépasse 5% peuvent résilier dans les 30 jours "
                "suivant la notification. Les gestionnaires doivent traiter ces résiliations en priorité "
                "et proposer une offre de remplacement adaptée avant la résiliation effective.",
            ),
        ],
    },
    {
        "ref": "CIRC-2024-002",
        "titre": "Nouveau produit : Prévoyance Collective PME+",
        "destinataires": "Équipes commerciales et gestionnaires grands comptes",
        "objet": "Présentation du nouveau produit Prévoyance Collective PME+ disponible à la commercialisation depuis le 01/03/2024.",
        "corps": [
            (
                "Description produit",
                "PrevCorp lance la gamme 'PME+' dédiée aux entreprises de 10 à 249 salariés. "
                "Ce produit propose une couverture prévoyance collective modulaire avec 4 niveaux : "
                "Essentiel, Confort, Confort+ et Premium. Il intègre nativement la conformité ANI et AGIRC-ARRCO.",
            ),
            (
                "Garanties incluses dans la formule de base",
                "Décès toutes causes (capital 200% PASS), "
                "Rente éducation (10% du capital décès par enfant à charge), "
                "ITT avec franchise 90 jours (IJ = 75% du salaire net de référence), "
                "IPT (capital = 150% PASS). Portabilité ANI incluse automatiquement.",
            ),
            (
                "Tarification",
                "Tarification simplifiée : questionnaire médical unique pour les contrats < 500 000 € de capital. "
                "Taux de cotisation moyen : entre 0,80% et 1,40% du salaire brut selon la formule. "
                "Participation employeur recommandée : 60% minimum pour optimisation fiscale (Loi Fillon).",
            ),
            (
                "Formation",
                "Une session de formation obligatoire est organisée le 15/03/2024 pour toutes les équipes commerciales. "
                "Support de vente disponible sur l'intranet PrevCorp à partir du 01/03/2024.",
            ),
        ],
    },
    {
        "ref": "CIRC-2024-003",
        "titre": "Évolution réglementaire — Dispositif 100% Santé 2024",
        "destinataires": "Gestionnaires santé collectifs et individuels",
        "objet": "Rappeler les obligations liées au dispositif 100% Santé et les modifications applicables en 2024.",
        "corps": [
            (
                "Rappel du dispositif",
                "Le dispositif 100% Santé, issu de la réforme de 2019, garantit un reste à charge nul "
                "pour certains équipements optiques, prothèses auditives et soins dentaires prothétiques. "
                "Tous les contrats de complémentaire santé responsables doivent couvrir intégralement le panier 100% Santé.",
            ),
            (
                "Modifications 2024",
                "Optique : extension du panier 100% Santé à 2 nouvelles références de montures. "
                "Dentaire : révision des plafonds de remboursement pour les prothèses Classe I (+8%). "
                "Audiologie : renouvellement des aides auditives désormais possible tous les 4 ans (au lieu de 5).",
            ),
            (
                "Impact sur les contrats PrevCorp",
                "Les contrats Complémentaire Santé Individuelle et Collective "
                "sont automatiquement mis à jour au 01/01/2024 sans avenant. "
                "Les tableaux de garanties mis à jour sont disponibles sur l'espace assuré.",
            ),
            (
                "Communication assurés",
                "Un email d'information est envoyé automatiquement à tous les assurés concernés. "
                "En cas de questions, orienter vers la FAQ dédiée 100% Santé (disponible sur le portail).",
            ),
        ],
    },
    {
        "ref": "CIRC-2024-004",
        "titre": "Mise à jour des délais de traitement des sinistres — Objectifs 2024",
        "destinataires": "Tous gestionnaires sinistres",
        "objet": "Fixer les nouveaux délais cibles de traitement des sinistres pour l'exercice 2024.",
        "corps": [
            (
                "Contexte",
                "L'analyse des réclamations 2023 a mis en évidence des délais de traitement trop longs "
                "sur les dossiers ITT complexes et les dossiers décès avec bénéficiaires multiples. "
                "Ces résultats ont conduit la Direction à revoir les objectifs de traitement.",
            ),
            (
                "Nouveaux délais cibles",
                "Décès (dossier complet) : 15 jours ouvrés (contre 20 en 2023). "
                "ITT (première déclaration) : 5 jours ouvrés. ITT (prolongation) : 3 jours ouvrés. "
                "IPT/IPP (expertise médicale incluse) : 45 jours ouvrés. Dépendance (instruction complète) : 60 jours ouvrés.",
            ),
            (
                "Indicateurs de suivi",
                "Un tableau de bord mensuel sera communiqué à chaque responsable d'équipe. "
                "Les dossiers dépassant les délais cibles seront automatiquement escaladés au N+1. "
                "Un indicateur de satisfaction assuré sera mesuré trimestriellement.",
            ),
            (
                "Ressources",
                "2 ETP supplémentaires sont alloués au service sinistres à partir du 01/02/2024. "
                "La formation 'Traitement accéléré des dossiers ITT complexes' est programmée pour mars 2024.",
            ),
        ],
    },
]


def generate_circulaire(circ):
    story = []
    story.append(header_block("Circulaire Interne", circ["ref"], "PrevCorp — 2024"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Circulaire Interne", TITLE_STYLE))
    story.append(
        Paragraph(
            circ["titre"],
            ParagraphStyle(
                "sous_titre",
                fontSize=13,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2e6da4"),
                spaceAfter=6,
            ),
        )
    )
    story.append(Spacer(1, 0.2 * cm))

    meta = [
        ["Référence :", circ["ref"]],
        ["Destinataires :", circ["destinataires"]],
        ["Objet :", circ["objet"]],
    ]
    t = Table(meta, colWidths=[3.5 * cm, 14.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 0.4 * cm))

    for titre_section, texte in circ["corps"]:
        story.append(Paragraph(titre_section, H2))
        story.append(Paragraph(texte, BODY))

    build_pdf(os.path.join(OUTPUT_DIR, f"CIRC_{circ['ref']}.pdf"), story)
    print(f"  ✓ CIRC_{circ['ref']}.pdf")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🏗  Génération du corpus PrevCorp\n")

    print("📄 Conditions Générales (10 docs)...")
    for ref, nom, garanties in PRODUITS:
        generate_cg(ref, nom, garanties, 0)

    print("\n📊 Fiches Paramétrage Garanties (12 docs)...")
    for g in GARANTIES:
        generate_fiche_garantie(g)

    print("\n❓ FAQ Gestionnaire (6 docs)...")
    for faq in FAQS:
        generate_faq(faq)

    print("\n🔧 Notes Techniques (6 docs)...")
    for nt in NOTES_TECHNIQUES:
        generate_note_technique(nt)

    print("\n📢 Circulaires (4 docs)...")
    for circ in CIRCULAIRES:
        generate_circulaire(circ)

    total = len(PRODUITS) + len(GARANTIES) + len(FAQS) + len(NOTES_TECHNIQUES) + len(CIRCULAIRES)
    print(f"\n✅ Corpus généré : {total} documents dans ./{OUTPUT_DIR}/")
