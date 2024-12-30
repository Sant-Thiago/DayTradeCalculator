import csv
import os

def write_file(filename, data):
    header = ['data', 'c', 'qtd_c', 'v', 'qtd_v', 'total']
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        
        writer.writeheader()
        
        if data is not None:
            for date, values in data.items():
                row = {
                    'data': date,
                    'c': values.get('c', ''),
                    'qtd_c': values.get('qtd_c', ''),
                    'v': values.get('v', ''),
                    'qtd_v': values.get('qtd_v', ''),
                    'total': values.get('total', '')
                }
            writer.writerow(row)

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
        
        if date not in calendar:
            calendar[date] = {}

        if row['total']:
            calendar[date]['total'] = row['total']
        
        else:
            c = float(row['c']) 
            qtd_c = int(row['qtd_c'])

            v = float(row['v'])
            qtd_v = int(row['qtd_v'])

            contracts = int(row['qtd_c']) + int(row['qtd_v'])

            buy = c * qtd_c
            sell = v * qtd_v
        
            total = (sell - buy) * 0.2
            
            emolumentos = contracts * 0.25
            
            total_com_desconto = total - emolumentos
            
            ir = total_com_desconto * 0.2
            
            total_com_desconto -= ir

            if not calendar[date]:
                calendar[date]['total'] = total_com_desconto
                calendar[date]['c'] = c
                calendar[date]['v'] = v
                calendar[date]['qtd_c'] = qtd_c
                calendar[date]['qtd_v'] = qtd_v
            else:
                calendar[date]['total'] += total_com_desconto
                calendar[date]['c'] += c
                calendar[date]['v'] += v
                calendar[date]['qtd_c'] += qtd_c
                calendar[date]['qtd_v'] += qtd_v

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
    write_file(filename, calendar)

