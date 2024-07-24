import pandas as pd
from fpdf import FPDF
import requests

url = "https://case-1sbzivi17-henriques-projects-2cf452dc.vercel.app/"

response = requests.get(url)
if response.status_code == 200:
    products = response.json()
else:
    print("Falha ao obter os dados dos produtos")
    products = []

df_products = pd.DataFrame(products)
print(df_products.head())

def create_generators(df_products):
    generators = []
    generator_id = 10000 

    for panel in df_products[df_products['Categoria'] == 'Painel Solar'].itertuples():
        panels = df_products[(df_products['Categoria'] == 'Painel Solar') & (df_products['Potencia em W'] == panel._3)]
        inverters = df_products[(df_products['Categoria'] == 'Inversor') & (df_products['Potencia em W'] == panel._3)]
        controllers = df_products[(df_products['Categoria'] == 'Controlador de carga') & (df_products['Potencia em W'] == panel._3)]
        
        for inverter in inverters.itertuples():
            for controller in controllers.itertuples():
                generator = {
                    'ID Gerador': generator_id,
                    'Potência do Gerador (em W)': panel._3,
                    'ID Produto': [panel.Id, inverter.Id, controller.Id],
                    'Nome do Produto': [panel.Produto, inverter.Produto, controller.Produto],
                    'Quantidade Item': [1, 1, 1]
                }
                generators.append(generator)
                generator_id += 1

    return pd.DataFrame(generators)

df_generators = create_generators(df_products)
print(df_generators.head())

df_generators.to_csv('geradores_configurados.csv', index=False)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório Semanal de Geradores Configurados', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

pdf = PDF()
pdf.add_page()

pdf.chapter_title("Resumo Semanal")

body = f"Prezados,\n\nNesta semana, configuramos um total de {len(df_generators)} geradores.\n\nAtt,\nJoão Victor"
pdf.chapter_body(body)

pdf.output('email_marketing.pdf')