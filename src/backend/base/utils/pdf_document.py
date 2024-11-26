from io import StringIO, BytesIO
from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile
from xhtml2pdf import pisa
from django.template import Context
from django.http import HttpResponse
from django.template.loader import get_template


def html_to_pdf_convert(template, context):
    html = template.render(context)
    policy_document_file = NamedTemporaryFile()
    pdf = pisa.pisaDocument(StringIO(html), policy_document_file)
    if not pdf.err:
        return File(policy_document_file)
    else:
        return False


def convert_html_to_pdf(template, context, document_owner, filename):
    html = template.render(context)
    f = NamedTemporaryFile()
    f.name = '/'+document_owner.executive.code+'/'+str(filename)
    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), f)

    if not pdf.err:
        return File(f)
    else:
        return False


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors')