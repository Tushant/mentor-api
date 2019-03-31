# from xhtml2pdf import pisa
from weasyprint import HTML
from django.template.loader import get_template
from django.http import HttpResponse


def pdf_generation(request):
    template = get_template('templates/accounts/index.html')
    context = {}
    html_template = template.render(context)
    pdf = HTML(string=html_template.encode()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="tushant_tyalent_resume.pdf"'
    return response


# def pdf_generation(request):
#     template = get_template('templates/accounts/index.html')
#     context = {'pagesize': 'A4'}
#     html = template.render(context)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         response = HttpResponse(result.getvalue(), content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="tushant_tyalent_resume.pdf"'
#     else:
#         response = HttpResponse('errors')
#     return response
