import pandas as pd
import pdfplumber
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

def Extract_Tabledata(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            page_tables = page.extract_tables()
            if page_tables:
                for table_num, table in enumerate(page_tables):
                    tables.append({
                        "table": table_num,
                        "page": page_num + 1,
                        "data": table
                    })
            else:
                #logging.info(f"No tables found on page {page_num + 1}")
                pass
    return tables


def generate_html_from_table(tables):
    html_output = ""
    for entry in tables:
        page = entry['page']
        table_index = entry['table']
        data = entry['data']

        # Start HTML table for this table entry
        html_output += f"<h3>Page {page}, Table {table_index}</h3>\n"
        html_output += "<table border='1' style='border-collapse: collapse;'>\n"


        for row in data:
            html_output += "<tr>\n"
            for cell in row:
                cell_content = cell if cell is not None else ""
                html_output += f"<td>{cell_content}</td>\n"
            html_output += "</tr>\n"

        html_output += "</table>\n\n"
    return html_output


pdf_path = r"C:\Users\Radhakrishnan\PycharmProjects\job\data\Test_pdf.pdf"
output_path = r"C:\Users\Radhakrishnan\PycharmProjects\job\data\output.html"

tables = Extract_Tabledata(pdf_path)
html_output = generate_html_from_table(tables)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

dt_Tables=pd.read_html(output_path)

dt_Tables #list of data frame

print(dt_Tables[1])



