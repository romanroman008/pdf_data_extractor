import PyPDF2


class PDFUtilities:
    @staticmethod
    def merge_pdfs(pdf_paths, output_path):
        pdf_writer = PyPDF2.PdfFileWriter()

        for path in pdf_paths:
            pdf_reader = PyPDF2.PdfFileReader(path)
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

        with open(output_path, 'wb') as out_file:
            pdf_writer.write(out_file)
