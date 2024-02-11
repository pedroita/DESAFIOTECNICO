from bs4 import BeautifulSoup
import requests
import pandas as pd
import tabula


def downloadPDF(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))


count = 1
for link in pdf_links:
    if 'Anexo I' in link.text: 
        pdf_url = link['href']
        filename = f'Anexo {count}.pdf'  
        downloadPDF(pdf_url, filename)
        count += 1  
    
print ("Extração realizada com sucesso!")

def gettable(pdf_file):
    tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
    
    for i, table in enumerate(tables):
        print(f'Tabela {i+1}:')
        print(table.df)
    
    df_list = []
    for table in tables:
        df_list.append(table.df)
    df = pd.concat(df_list)
    
    return df

pdf_file_anexo1 = 'Anexo 1.pdf' 

anexo1_df = gettable(pdf_file_anexo1)
anexo1_df.rename(columns={'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}, inplace=True)
csv_filename = 'dados_anexo1.csv'
anexo1_df.to_csv(csv_filename, index=False)
print(f'Dados extraídos do Anexo I e salvos em {csv_filename}')





