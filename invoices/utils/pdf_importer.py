from pypdf import PdfReader
from invoices.models import Customer, Order, OrderItem
from datetime import datetime
import decimal
import glob


def hae_laskun_perustiedot(lines):
    laskunro = int(lines[0].split(' ')[1])
    laskupvm = datetime.strptime(lines[1].split(' ')[1], '%d.%m.%Y').date()
    asikas_id = int(lines[2].split(' ')[2])
    maksuehto = ' '.join(lines[3].split(' ')[1:])
    return laskunro, laskupvm, asikas_id, maksuehto

def hae_asiakas_tiedot(lines):
    line_index = 0
    while not lines[line_index].strip() == 'ASIAKAS':
        line_index += 1
    line_index += 1
    asiakas_nimi = lines[line_index]
    line_index += 1
    asiakas_yritys = lines[line_index]
    line_index += 1
    asiakas_osoite = lines[line_index]
    line_index += 1
    asiakas_postinumero = lines[line_index].split(' ')[0]
    if len(lines[line_index].split(' ')) > 1:
        asiakas_postitoimipaikka = lines[line_index].split(' ')[1]
    else:
        asiakas_postitoimipaikka = 'TUNTEMATON'
    return asiakas_nimi, asiakas_yritys, asiakas_osoite, asiakas_postinumero, asiakas_postitoimipaikka

def hae_nimikkeet_ja_puhelin(lines, laskurivit_kpl):
    line_index = 0
    while not lines[line_index].strip() == 'Palvelut':
        line_index += 1
    asiakas_puhelin = lines[line_index - 1]
    line_index += 1
    nimikkeet = []
    for i in range(laskurivit_kpl):
        nimikkeet.append(lines[line_index])
        line_index += 1
    return nimikkeet, asiakas_puhelin

def hae_laskurivit_ja_yhteensa(lines):
    line_index = 0
    while not lines[line_index].strip() == 'Tunnit a hinta SUMMA €':
        line_index += 1
    line_index += 1
    laskurivit = []
    yhteensa_rivi = False
    while not yhteensa_rivi:
        if lines[line_index].split(' ')[0] == 'YHTEENSÄ':
            yhteensa = decimal.Decimal(lines[line_index].split(' ')[1].replace(',', '.'))
            yhteensa_rivi = True
            line_index += 1
            continue
        else:
            if lines[line_index].strip() == '-':
                line_index += 1
                continue
            else:
                laskurivi_data = lines[line_index].replace(',', '.')
                laskurivit_string = laskurivi_data.split(' ')
                laskurivit.append([decimal.Decimal(x) for x in laskurivit_string])
        line_index += 1
    return laskurivit, yhteensa

def parse_and_import_pdfs(pdf_path):
    pdf_files = glob.glob(pdf_path + "*.pdf")
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        if len(reader.pages) != 1:
            continue
        page = reader.pages[0]
        lines = page.extract_text().split('\n')
        laskunro, laskupvm, asikas_id, maksuehto = hae_laskun_perustiedot(lines)
        asiakas_nimi, asiakas_yritys, asiakas_osoite, asiakas_postinumero, asiakas_postitoimipaikka = hae_asiakas_tiedot(lines)
        laskurivit, yhteensa = hae_laskurivit_ja_yhteensa(lines)
        nimikkeet, asiakas_puhelin = hae_nimikkeet_ja_puhelin(lines, len(laskurivit))

        # Save or get customer
        customer, _ = Customer.objects.get_or_create(
            customer_id=asikas_id,
            defaults={
                'name': asiakas_nimi,
                'company': asiakas_yritys,
                'address': asiakas_osoite,
                'postal_code': asiakas_postinumero,
                'city': asiakas_postitoimipaikka,
                'phone': asiakas_puhelin
            }
        )

        # Save or get order
        order, _ = Order.objects.get_or_create(
            invoice_number=laskunro,
            defaults={
                'date': laskupvm,
                'customer': customer,
                'payment_terms': maksuehto,
                'total': yhteensa
            }
        )

        # Save order items
        for i, rivi in enumerate(laskurivit):
            OrderItem.objects.get_or_create(
                order=order,
                item_name=nimikkeet[i],
                defaults={
                    'hours': rivi[0],
                    'price': rivi[1],
                    'sum': rivi[2]
                }
            )
