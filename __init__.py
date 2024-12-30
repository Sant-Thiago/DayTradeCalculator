import csv
import os

def write_file(filename):
    header = ['data', 'c', 'qtd_c', 'v', 'qtd_v', 'total']
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)        
        writer.writeheader()

def read_file(filename):
    if not os.path.exists(filename):
        print("O arquivo não existe!")
        return

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        
        return list(reader)
    
def treatment(matriz):
    calendar = {}

    for row in matriz:

        date = row['data']
        
    
        buy = float(row['c']) * int(row['qtd_c'])
        sell = float(row['v']) * int(row['qtd_v'])
        contracts = int(row['qtd_c']) + int(row['qtd_v'])

        total = (sell - buy) * 0.2
        
        emolumentos = contracts * 0.25
        
        total_com_desconto = total - emolumentos
        
        ir = total_com_desconto * 0.2
        
        total_com_desconto -= ir

        if date not in calendar:
            calendar[date] = {}
            calendar[date]['total'] = total_com_desconto
        else:
            calendar[date]['total'] += total_com_desconto

    return calendar

def show_desc(data):
    for date, value in data.items():
        total_formatado = f'{value['total']:.2f}'.replace('.', ',')
        print(f'Data:: {date} - Total:: R${total_formatado}')

filename = 'dados_day_trade.csv'

if not os.path.exists(filename):
    write_file(filename)

if os.path.exists(filename):
    data = read_file(filename)
    calendar = treatment(data)
    show_desc(calendar)

