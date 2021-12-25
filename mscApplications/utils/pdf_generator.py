from applicant.models import *
from msc.models import MscFlow
from reportlab.platypus import Table
import PyPDF2
from django.core.files import File
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import PyPDF2
import tempfile
from datetime import datetime
from reportlab.platypus import TableStyle


def generate_applicant_app(applicant,application):
    temp_base = tempfile.TemporaryFile()
    temp_final = tempfile.TemporaryFile()


    doc = SimpleDocTemplate(temp_base,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    sample_style_sheet = getSampleStyleSheet()
    logo = "static/img/xarokop_0.png"
    im = Image(logo, 4*inch, 2*inch)
    Story.append(im)
    Story.append(Spacer(1, 24))
    paragraph_1 = Paragraph("Application", sample_style_sheet['Title'])
    Story.append(paragraph_1)
    poTable = None
    appTable = None
    prefTable = None
    if applicant.gender == 'M':
        gen='Male'
    else:
        gen='Female'
    Width = 250
    # 1) Build Structure
    po_titleTable = Table([
        ["Personal Informations"]
    ], Width)

    first_name_table = Table([
        ['First Name:', applicant.user.first_name]
    ], [60, 190])
    last_name_table = Table([
        ['Last Name:', applicant.user.last_name]
    ], [60, 190])
    birth_date_table = Table([
        ['Birth Date:', applicant.birth_date.strftime('%d/%m/%Y')]
    ], [60, 190])
    country_table = Table([
        ['Country:', applicant.country]
    ], [60, 190])
    city_table = Table([
        ['City:', applicant.city]
    ], [60, 190])
    address_table = Table([
        ['Address:', applicant.address]
    ], [60, 190])
    phone_table = Table([
        ['Phone:', applicant.telephone]
    ], [60, 190])
    gender_table = Table([
        ['Gender:', gen]
    ], [60, 190])
    poTable = Table([
        [po_titleTable],
        [first_name_table,last_name_table],
        [birth_date_table,phone_table],
        [country_table,city_table],
        [address_table,gender_table]
    ], hAlign='LEFT')
    titleTableStyle = TableStyle([
        ('FONTSIZE', (1,0), (-1,0), 13),
        ('VALIGN',(0,0),(-1,0),'TOP'),
        ('FONTNAME', (0,0), (-1,-1),
            'Helvetica-Bold'
            ),

        ('TOPPADDING',(0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ])
    po_titleTable.setStyle(titleTableStyle)
    submission_date_table = Table([
        ['Submission Date:', datetime.today().strftime('%d/%m/%Y'),]
    ], [90, 190])
    call_table = Table([
        ['Call:', application.call]
    ], [60, 190])
    programme_table = Table([
        ['Msc Programme:', application.call.msc_programme]
    ], [100, 230])
    reference_table = Table([
        ['Reference:', application.reference]
    ], [60, 190])
    app_titleTable = Table([
        ["Application Informations"]
    ], Width)
    appTable = Table([
        [app_titleTable],
        [call_table],
        [programme_table],
        [submission_date_table],
        [reference_table],
    ], hAlign='LEFT')
    app_titleTable.setStyle(titleTableStyle)
    if application.preference_set.all():
        prefereces_titleTable = Table([
            ["Prefered Flows By order"]
        ], Width)
        flows_data=[]
        for flow in application.preference_set.all():
            flows_data.append([flow.priority,flow])
        flowTable = Table(flows_data)
        prefTable=Table([
            [prefereces_titleTable],
            [flowTable]
        ], hAlign='LEFT')
        prefereces_titleTable.setStyle(titleTableStyle)
        mainTable = Table([
        [poTable],
        [appTable],
        [prefTable]
        ], hAlign='LEFT')
    else:
        mainTable = Table([
        [poTable],
        [appTable],
        ], hAlign='LEFT')
    Story.append(Spacer(1, 24))
    Story.append(mainTable)
    doc.build(Story)
    merger = PyPDF2.PdfFileMerger()
    merger.append(temp_base)
    for ref in Reference.objects.filter(applicant=applicant):
        merger.append(ref.media_file)
    for phd in Phd.objects.filter(applicant=applicant):
        merger.append(phd.media_file)
    for diploma in Diploma.objects.filter(applicant=applicant):
        merger.append(diploma.media_file)
    for job in JobExperience.objects.filter(applicant=applicant):
        merger.append(job.media_file)
    merger.write(temp_final)
    return File(temp_final)

def generate_applicant_app_to_greek(applicant,application):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("Arial",'static/fonts/DejaVuSans.ttf')) # here i have my fonts for PDF's
    temp_base = tempfile.TemporaryFile()
    temp_final = tempfile.TemporaryFile()
    doc = SimpleDocTemplate(temp_base,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    sample_style_sheet = getSampleStyleSheet()
    logo = "static/img/xarokop_0.png"
    im = Image(logo, 4*inch, 2*inch)
    Story.append(im)
    Story.append(Spacer(1, 24))
    style = sample_style_sheet["Title"]  #Select the normal format in the default
    style.fontName = 'Arial'
    paragraph_1 = Paragraph("Aίτηση", style)
    Story.append(paragraph_1)
    poTable = None
    appTable = None
    prefTable = None
    gen=None
    if applicant.gender== 'M':
        gen='Αρσενικό'
    else:
        gen='Θηλυκό'
    Width = 250
    # 1) Build Structure
    po_titleTable = Table([
        ["Προσωπικά Στοιχεία"]
    ], Width)

    first_name_table = Table([
        ["Όνομα:", applicant.user.first_name]
    ], [60, 190])
    last_name_table = Table([
        ['Επώνυμο:', applicant.user.last_name]
    ], [60, 190])
    birth_date_table = Table([
        ['Ημ/νία Γέννησης:', applicant.birth_date.strftime('%d/%m/%Y')]
    ], [110, 140])
    country_table = Table([
        ['Χώρα:', applicant.country]
    ], [60, 190])
    city_table = Table([
        ['Πόλη:', applicant.city]
    ], [60, 190])
    address_table = Table([
        ['Διεύθυνση:', applicant.address]
    ], [60, 190])
    phone_table = Table([
        ['Τήλεφωνο:', applicant.telephone]
    ], [60, 190])
    gender_table = Table([
        ['Γένος:', gen]
    ], [60, 190])
    poTable = Table([
        [po_titleTable],
        [first_name_table,last_name_table],
        [birth_date_table,phone_table],
        [country_table,city_table],
        [address_table,gender_table]
    ], hAlign='LEFT')
    titleTableStyle = TableStyle([
        ('FONTSIZE', (1,0), (-1,0), 13),
        ('VALIGN',(0,0),(-1,0),'TOP'),
        ('FONTNAME', (0,0), (-1,-1),
            'Arial'
            ),

        ('TOPPADDING',(0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ])
    tableStyle = TableStyle([
        ('FONTNAME', (0,0), (-1,-1),
            'Arial'
            ),
    ])
    po_titleTable.setStyle(titleTableStyle)
    first_name_table.setStyle(tableStyle)
    last_name_table.setStyle(tableStyle)
    city_table.setStyle(tableStyle)
    country_table.setStyle(tableStyle)
    birth_date_table.setStyle(tableStyle)
    address_table.setStyle(tableStyle)
    phone_table.setStyle(tableStyle)
    gender_table.setStyle(tableStyle)
    submission_date_table = Table([
        ['Ημ/νία Υποβολής:', datetime.today().strftime('%d/%m/%Y'),]
    ], [90, 190])
    call_table = Table([
        ['Πρόσκληση:', application.call.title_el_GR]
    ], [60, 190])
    programme_table = Table([
        ['Πρόγραμμα ΠΜΣ:', application.call.msc_programme.title_el_GR]
    ], [100, 230])
    reference_table = Table([
        ['Συστ. Επιστολή:', application.reference]
    ], [100, 230])
    app_titleTable = Table([
        ["Στοιχεία της Αίτησης"]
    ], Width)
    appTable = Table([
        [app_titleTable],
        [call_table],
        [programme_table],
        [submission_date_table],
        [reference_table],
    ], hAlign='LEFT')
    app_titleTable.setStyle(titleTableStyle)
    reference_table.setStyle(tableStyle)
    programme_table.setStyle(tableStyle)
    call_table.setStyle(tableStyle)
    submission_date_table.setStyle(tableStyle)

    if application.preference_set.all():
        prefereces_titleTable = Table([
            ["Κατυεθύνσεις με σειρά προτίμησης"]
        ], Width)
        flows_data=[]
        for flow in application.preference_set.all():
            flows_data.append([flow.priority,flow.flow.title_el_GR])
        flowTable = Table(flows_data)
        prefTable=Table([
            [prefereces_titleTable],
            [flowTable]
        ], hAlign='LEFT')
        prefereces_titleTable.setStyle(titleTableStyle)
        flowTable.setStyle(tableStyle)
        mainTable = Table([
        [poTable],
        [appTable],
        [prefTable]
        ], hAlign='LEFT')
    else:
        mainTable = Table([
        [poTable],
        [appTable],
        ], hAlign='LEFT')
    Story.append(Spacer(1, 24))
    Story.append(mainTable)
    doc.build(Story)
    merger = PyPDF2.PdfFileMerger()
    merger.append(temp_base)
    for ref in Reference.objects.filter(applicant=applicant):
        merger.append(ref.media_file)
    for phd in Phd.objects.filter(applicant=applicant):
        merger.append(phd.media_file)
    for diploma in Diploma.objects.filter(applicant=applicant):
        merger.append(diploma.media_file)
    for job in JobExperience.objects.filter(applicant=applicant):
        merger.append(job.media_file)
    merger.write(temp_final)
    return File(temp_final)
