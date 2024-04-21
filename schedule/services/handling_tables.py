from pypdf import PdfReader
import pdfplumber

from config.settings import PATH_TO_DOWNLOAD

path_to_file = PATH_TO_DOWNLOAD
reader = PdfReader(
    f'{PATH_TO_DOWNLOAD}\schedule-1-kurs_14022024103759.pdf'
)
semester = ''
week = ''
group = 0
period = ''
teacher = 0
audience = 0
subject = 0
semester = ''

with pdfplumber.open(
        f'{path_to_file}\schedule-1-kurs_14022024103759.pdf'
) as f:
    semester = f.pages[0].extract_tables()[0][0][0]
    # for page in f.pages:
    #     print(page.extract_tables())

    not_handled_groups = f.pages[0].extract_tables()[0][1][7:]
    groups = [i for i in not_handled_groups if i is not None]
    print(groups)