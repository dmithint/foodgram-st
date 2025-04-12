from fpdf import FPDF


def create_pdf(ingredients):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', './recipes/fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=10)
    pdf.cell(200, 10, txt='Список покупок', ln=1, align='C')
    for ingredient in ingredients:
        name = ingredient['ingredient__name']
        unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['ingredient_amount']
        pdf_str = f'{name} - {amount} {unit}'
        pdf.cell(200, 10, txt=pdf_str, ln=1, align='L')
    file = pdf.output(name='shopping_cart.pdf', dest='S').encode('latin-1')
    return (file)
