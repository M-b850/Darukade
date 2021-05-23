import json
import pandas as pd


def export_json(result):
    """ Serializing json """
    with open('src/sample/output.json', 'w') as f:
        # json_object = json.dumps(result, ensure_ascii=False, indent=4)
        json.dump(result, f, ensure_ascii=False, indent=4)


def export_exel(result):
    """ Export exel with new format """ 
    excel_result = []
    for r in result:
        for comment in r['Comments']:
            r_dict = {
                'ProductPageLink': r['ProductPageLink'],
                'ProductName': r['ProductName'],
                'Productcode': r['Productcode'],
                'BrandNameFa': r['BrandNameFa'],
                'BrandNameEn': r['BrandNameEn'],
                'Group': r['Group'],
                'CommentOwnerId': comment['CommentOwnerId'],
                'CommentDate': comment['CommentDate'],
                'CommentDescription': comment['CommentDescription'],
            }
            excel_result.append(r_dict)
    df = pd.DataFrame.from_dict(excel_result)
    print(df)
    df.to_excel('src/sample/sample.xlsx')
