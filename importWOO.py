from preCSV import csv_to_list
from amigo_graber import save_to_csv


file_src = 'results/total_results.csv'
source = csv_to_list(src=file_src)
path_to_save_results = 'results'
name_to_save_result = 'woocommerce_import.csv'
result = {}
import_wc_result = []
category = 'Рулонные жалюзи'
path_to_img = 'http://kubanzhalyuzi.ru/wp-content/uploads/shop/rulon/images/'
category_link = 'http://kubanzhalyuzi.ru/?p=934'
columns = [ 'ID',
            'Type',
            'Name',
            'Published',
            'Visibility in catalog',
            'Description',
            'Tax status',
            'Tax class',
            'In stock?',
            'Regular price',
            'Categories',
            'Images',
            'Parent',
            'Attribute 1 name',
            'Attribute 1 value(s)',
            'Attribute 1 visible',
            'Attribute 1 global',
            'Attribute 1 default',
            'Attribute 2 name',
            'Attribute 2 value(s)',
            'Attribute 2 visible',
            'Attribute 2 global',
            'Attribute 3 name',
            'Attribute 3 value(s)',
            'Attribute 3 visible',
            'Attribute 3 global',
            'Attribute 4 name',
            'Attribute 4 value(s)',
            'Attribute 4 visible',
            'Attribute 4 global',
            'Attribute 5 name',
            'Attribute 5 value(s)',
            'Attribute 5 visible',
            'Attribute 5 global',
            'Attribute 6 name',
            'Attribute 6 value(s)',
            'Attribute 6 visible',
            'Attribute 6 global',
            ]


def gen_id(prefix, num):
    return int(prefix)+int(num)


def group_color(arr, sel=3):
    result = []
    for item in arr:
        result.append(item[sel])
    return ', '.join(result)


def group_name(source:dict, limit=None):
    """
    ГРуппировка элементов по названию материала
    :param source: список маетриалов
    :return: группиованный список материалов
    """
    for num, row in enumerate(source[1:limit]):
        id = gen_id(2000, 2*num)
        name = row[0]
        code = row[1]
        color = row[2]
        height = int(row[3])/100
        image = row[4]
        price = row[5]
        country = row[6]
        tone = 'multitone'

        try:
            result[name]
        except KeyError:
            result[name] = []

        result[name].append([
            id,
            name,
            code,
            color,
            height,
            image,
            price,
            country,
            tone,
        ])
    return result


def add_wc_row(sub_item, variable:dict):
    """
    Добавление форматированной строки для импорта в woocommerce
    :param item:
    :param sub_item:
    :return:
    """
    _ID = variable['_ID']  # variable
    _Type = variable['_Type']  # variable
    _Name = variable['_Name']  # variable
    _Published = '1'
    _Visibility_in_catalog = 'visible'
    _Description = variable['_Description']  # variable
    _Tax_status = 'taxable'
    _Tax_class = variable['_Tax_class']  # variables
    _In_stock = variable['_In_stock']  # variable
    _Regular_price = variable['_Regular_price']  # variable
    _Categories = variable['_Categories']  # variable
    _Images = f'{path_to_img}{sub_item[5]}'
    _Parent = variable['_Parent']  # variable
    _Attribute_1_name = 'цвет'
    _Attribute_1_values = variable['_Attribute_1_values'] # variable
    _Attribute_1_visible = variable['_Attribute_1_visible'] # variable
    _Attribute_1_global = variable['_Attribute_1_global'] # variable
    _Attribute_1_default = variable['_Attribute_1_default'] # variable
    _Attribute_2_name = variable['_Attribute_2_name']  # variable
    _Attribute_2_values = variable['_Attribute_2_values']  # variable
    _Attribute_2_visible = variable['_Attribute_2_visible']  # variable
    _Attribute_2_global = variable['_Attribute_2_global']  # variable

    _Attribute_3_name = variable['_Attribute_3_name']  # variable
    _Attribute_3_values = variable['_Attribute_3_values']  # variable
    _Attribute_3_visible = variable['_Attribute_3_visible']  # variable
    _Attribute_3_global = variable['_Attribute_3_global']  # variable

    _Attribute_4_name = variable['_Attribute_4_name']  # variable
    _Attribute_4_values = variable['_Attribute_4_values']  # variable
    _Attribute_4_visible = variable['_Attribute_4_visible']  # variable
    _Attribute_4_global = variable['_Attribute_4_global']  # variable

    _Attribute_5_name = variable['_Attribute_5_name']  # variable
    _Attribute_5_values = variable['_Attribute_5_values']  # variable
    _Attribute_5_visible = variable['_Attribute_5_visible']  # variable
    _Attribute_5_global = variable['_Attribute_5_global']  # variable

    _Attribute_6_name = variable['_Attribute_6_name']  # variable
    _Attribute_6_values = variable['_Attribute_6_values']  # variable
    _Attribute_6_visible = variable['_Attribute_6_visible']  # variable
    _Attribute_6_global = variable['_Attribute_6_global']  # variable

    return [
        _ID,
        _Type,
        _Name,
        _Published,
        _Visibility_in_catalog,
        _Description,
        _Tax_status,
        _Tax_class,
        _In_stock,
        _Regular_price,
        _Categories,
        _Images,
        _Parent,
        _Attribute_1_name,
        _Attribute_1_values,
        _Attribute_1_visible,
        _Attribute_1_global,
        _Attribute_1_default,
        _Attribute_2_name,
        _Attribute_2_values,
        _Attribute_2_visible,
        _Attribute_2_global,
        _Attribute_3_name,
        _Attribute_3_values,
        _Attribute_3_visible,
        _Attribute_3_global,
        _Attribute_4_name,
        _Attribute_4_values,
        _Attribute_4_visible,
        _Attribute_4_global,
        _Attribute_5_name,
        _Attribute_5_values,
        _Attribute_5_visible,
        _Attribute_5_global,
        _Attribute_6_name,
        _Attribute_6_values,
        _Attribute_6_visible,
        _Attribute_6_global,
    ]


def set_parent_variables(item, sub_item, argws = {'_Type':'variable'}):
    """
    Установка переменных для родительского элемента сгруппированныъ материалов
    либо для единственного элемента ез группировки
    :param item:
    :param sub_item:
    :return:
    """

    return {
        '_ID': sub_item[0]-1,
        '_Type': argws['_Type'],
        '_Name': sub_item[1],
        '_Description': f'Рулонные жалюзи {sub_item[1]}',
        '_Tax_class': '',
        '_In_stock': '1',
        '_Regular_price': '',
        '_Categories': 'Рулонные жалюзи',
        '_Parent': '',
        '_Attribute_1_values': group_color(item, sel=3),
        '_Attribute_1_visible': '1',
        '_Attribute_1_global': '0',
        '_Attribute_1_default': sub_item[3],
        '_Attribute_2_name': 'Ширина рулона (м)',
        '_Attribute_2_values': sub_item[4],
        '_Attribute_2_visible': '1',
        '_Attribute_2_global': '0',
        '_Attribute_3_name': 'Страна',
        '_Attribute_3_values': sub_item[7],
        '_Attribute_3_visible': '1',
        '_Attribute_3_global': '0',
        '_Attribute_4_name': 'price',
        '_Attribute_4_values': sub_item[6],
        '_Attribute_4_visible': '0',
        '_Attribute_4_global': '0',
        '_Attribute_5_name': 'custom_category_link',
        '_Attribute_5_values': category_link,
        '_Attribute_5_visible': '0',
        '_Attribute_5_global': '0',
        '_Attribute_6_name': 'tone',
        '_Attribute_6_values': 'multitone',
        '_Attribute_6_visible': '0',
        '_Attribute_6_global': '0',
    }


def set_child_variables(item, sub_item):
    """
    Установка переменных для родительского элемента сгруппированныъ материалов
    :param item:
    :param sub_item:
    :return:
    """
    return {
            '_ID': sub_item[0],
            '_Type': 'variation',
            '_Name': f'{sub_item[1]} - {sub_item[3]}',
            '_Description': sub_item[2],
            '_Tax_class': 'parent',
            '_In_stock': '0',
            '_Regular_price': '1',
            '_Categories': '',
            '_Parent': f'id:{item[0][0]-1}',
            '_Attribute_1_values': sub_item[3],
            '_Attribute_1_visible': '',
            '_Attribute_1_global': '0',
            '_Attribute_1_default': '',
            '_Attribute_2_name': '',
            '_Attribute_2_values': '',
            '_Attribute_2_visible': '',
            '_Attribute_2_global': '',
            '_Attribute_3_name': '',
            '_Attribute_3_values': '',
            '_Attribute_3_visible': '',
            '_Attribute_3_global': '',
            '_Attribute_4_name': '',
            '_Attribute_4_values': '',
            '_Attribute_4_visible': '',
            '_Attribute_4_global': '',
            '_Attribute_5_name': '',
            '_Attribute_5_values': '',
            '_Attribute_5_visible': '',
            '_Attribute_5_global': '',
            '_Attribute_6_name': '',
            '_Attribute_6_values': '',
            '_Attribute_6_visible': '',
            '_Attribute_6_global': '',
            }


if __name__ == '__main__':
    group_name_list = group_name(source)
    total_error = 0
    for item in group_name_list:
        try:
            if group_name_list[item].__len__() > 1:  # if group material
                for i, sub_item in enumerate(group_name_list[item]):
                    if i == 0:
                        pass
                        # do for parent element
                        row = set_parent_variables(group_name_list[item], sub_item)
                        row_child = set_child_variables(group_name_list[item], sub_item)
                        import_wc_result.append(add_wc_row(sub_item, row))
                        import_wc_result.append(add_wc_row(sub_item, row_child))
                    else:
                        pass
                        # do for child element
                        row_child = set_child_variables(group_name_list[item], sub_item)
                        import_wc_result.append(add_wc_row(sub_item, row_child))
            else:
                # если в датасете нет сгруппированных элементов
                sub_item = group_name_list[item][0]
                row = set_parent_variables(group_name_list[item], sub_item, argws={'_Type': 'simple', })
                import_wc_result.append(add_wc_row(sub_item, row))
        except IndexError:
            total_error += 1

    save_to_csv(path_to_save_results, name_to_save_result, data=import_wc_result, columns=columns)
    if not total_error:
        print("Import success!", f"For import use file: {path_to_save_results}/{name_to_save_result}")
    else:
        print("Import failed :(", f"{total_error} - errors")