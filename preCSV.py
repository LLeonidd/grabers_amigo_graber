import csv
import logging
from amigo_graber import save_to_csv


file_src = 'results/results.csv'
file_with_price = 'results/price.csv'
path_to_save_results = 'results'
name_to_save = 'total_results.csv'

logging.basicConfig(filename=f'{path_to_save_results}/precsv.log', level=logging.INFO)

def csv_to_dict(src: str = None, delimiter: str = ',', quotechar: str = '"'):
    result = {}
    with open(src, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in csvreader:
            result[row[0]] = row
    return result


def csv_to_list(src: str = None, delimiter: str = ',', quotechar: str = '"'):
    result = []
    with open(src, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in csvreader:
            result.append(row)
    return result



def merge_csv(): pass

if __name__ == '__main__':
    materials = csv_to_list(src=file_src)
    price = csv_to_dict(src=file_with_price)
    results = []
    errors  = 0
    # Merge price, country columns with materials data
    for material in materials:
        try:
            material[5] = price[material[0]][8].replace(u'\xa0', u'').replace(',', '.')
            material[6] = price[material[0]][3]
            results.append(material)
        except KeyError:
            errors+=1
            print('Error merge: ', material)
            logging.info(f'Error merge: {material}')
            continue

    data_columns = ['name', 'code', 'color', 'height', 'img_name', 'price', 'country']

    save_to_csv(path_to_save_results, name_to_save, data=results, columns=data_columns)
    print('Total errors: ', errors)
