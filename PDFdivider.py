import glob
import shutil
import os
import PyPDF2


def split_pdf_pages(input_pdf_path, target_dir, file_name_fmt=u'{num_page:04d}.pdf'):
    """Function to split PDF file into sheets.
       Функция разбивающая PDF файл на листы."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    replace = input_pdf_path.split('\\')[-1].replace(' ', '_').replace('.pdf', '')

    with open(input_pdf_path, 'rb') as input_stream:
        input_pdf = PyPDF2.PdfFileReader(input_stream)

        if input_pdf.flattenedPages is None:
            input_pdf.getNumPages()

        for num_page, page in enumerate(input_pdf.flattenedPages):
            output = PyPDF2.PdfFileWriter()
            output.addPage(page)

            file_name = os.path.join(target_dir, replace + '_' + file_name_fmt.format(num_page=num_page + 1))
            with open(file_name, 'wb') as output_stream:
                output.write(output_stream)


def main():
    """Main function
       Главня функция"""

    if not os.path.exists('download'):
        os.mkdir('download')
        print(f'INFO: Создана папка "download".\n'
              f'INFO: Сложите в неё PDF файлы, которые необходимо разделить.')
        print()
        input('Нажмите любую клавишу для выхода...')
    else:

        if os.path.exists('divide_pages'):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'divide_pages')

            try:
                shutil.rmtree(path)
                print(f'INFO: Очистили папку > {path}')
            except FileExistsError as e:
                print(f'WARNING: {path} ошибка > {e}')

        pdf_path = glob.glob(r'download/*{}'.format('.pdf'))
        for path in pdf_path:
            split_pdf_pages(path, 'divide_pages')

        files = [item for item in glob.glob(r'divide_pages/*{}'.format('.pdf'))]

        print(f'INFO: Нарезали PDF на: {len(files)} шт.\n'
              f'INFO: Готовые файлы в папке "divide_pages"')
        print()
        input('Нажмите любую клавишу для выхода...')


if __name__ == '__main__':
    main()
