import sys
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()


"""
import subprocess

def parse_pdf(filename):
    try:
        content = subprocess.check_output(["pdftotext", '-enc', 'UTF-8', filename, "-"])
    except subprocess.CalledProcessError as e:
        print('Skipping {} (pdftotext returned status {})'.format(filename, e.returncode))
        return None
    return content.decode('utf-8')
"""


import logging
logging.getLogger().setLevel(logging.DEBUG)
import io
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
 
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            print('procesando página : {}'.format(page))
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
        logging.info('texto obtenido : {}'.format(text))
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text


from ocrmypdf import __main__


if __name__ == '__main__':
    #pdf = sys.argv[1]

    __main__.run_pipeline(args=['-l', 'spa', 'Disp 9-2018.pdf', '/tmp/o2.pdf'])

    t = extract_text_from_pdf('/tmp/o2.pdf')
    logging.info(t)

