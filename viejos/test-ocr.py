
if __name__ == '__main__':

    from pdf2image import convert_from_path
    pages = convert_from_path('Disp 9-2018.pdf', 500)

    for page in pages:
        print(type(page))