import csv

"""CSV cannot contain special characters '#', '&', etc"""

# Name of csv being imported without '.csv'
naming_config = '3_4_CHENG_TOCHA_OFFICE_STORAGE_copy'
# .bSolid file referenced by bNest for tooling information
# program_name =  'RECTparam.bSolid'
program_name =  'RECTparamCLEAF.bSolid'
# Adding .csv
opening_csv = naming_config + '.csv'
# Adding 'METRIC' to differentiate between csv in inches
csv_metric = naming_config + '_METRIC.csv'
# Stores csv as a list of lists; each row being a nested list
new_metric_csv = []

def imperial_to_metric(imp_num):
    """Converts inches to mm within three significant digits"""
    return round(imp_num * 25.4, 2)


def convert_to_float(frac_str):
    """Converts inch measurements that are strings to floats"""
    frac_str = frac_str[:-1]
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


"""Opens the csv that is in inches, converts data into list format.
Uses functions convert_to_float and imperial to metric to prep data
""" 
with open(opening_csv,newline='',encoding='utf-8') as csvfile:
    the_Reader = csv.reader(csvfile, delimiter=',')
    rows = list(the_Reader)
    new_metric_csv.append(rows[0])
    for row in rows[1:]:
        qty = row[2]
        length, width, thickness = row[6:9]
        length = convert_to_float(length)
        width = convert_to_float(width)
        thickness = convert_to_float(thickness)
        row[2] = int(qty)
        row[6] = imperial_to_metric(length)
        row[7] = imperial_to_metric(width)
        row[8] = imperial_to_metric(thickness)
        new_metric_csv.append(row)

    
with open(csv_metric, 'w', newline="",encoding='utf-8') as csvfile:
    fieldnames = ['QTY','CustomerName','JobOrder','Name','DESC','LENGTH',
    'WIDTH','THICK','WoodType','Grain','LabelImage','ProgramName','RotationStep',
    'ProgramParameters','AdditionalMargin','Priority','OverProduction'
    ]
    dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
    dict_writer.writeheader()
    for row in new_metric_csv[1:]:
        dict_writer.writerow({
            'QTY': row[2],
            'CustomerName': 'biesse',
            'JobOrder': 'bNest',
            'Name': row[1],
            'DESC': 'RECT_Param',
            'LENGTH': row[6],
            'WIDTH': row[7],
            'THICK': row[8],
            'WoodType': row[10],
            'Grain': 0,
            'LabelImage': row[1],
            'ProgramName': program_name,
            'RotationStep': 0,
            'ProgramParameters': 0,
            'AdditionalMargin': 0,
            'Priority': 0,
            'OverProduction': 0,
        })
