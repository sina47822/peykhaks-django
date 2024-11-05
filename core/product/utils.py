# product/utils.py

import pandas as pd
from django.http import HttpResponse
from .models import Product, Category, Tags, Standards
from django.conf import settings

def export_products_to_excel():
    # Select only the fields you want to export
    products_data = []

    # Loop through each product and add translations for specified languages
    for product in Product.objects.all():
        product_info = {
            'id': product.id,
            'title': product.title,
            'slug': product.slug,
            'description': product.description,
            'summery': product.summery,
            'price': product.price,
            'offer_price': product.offer_price,
            'category': product.category,
            'is_active': product.is_active,
            'stock': product.stock,
            'size': product.size,
            'guarantee': product.guarantee,
            'time_to_bring': product.time_to_bring,
        }
        # Add translations for each language in settings.LANGUAGES
        for lang_code, _ in settings.LANGUAGES:
            product_info[f'title_{lang_code}'] = getattr(product, f'title_{lang_code}', '')
            product_info[f'description_{lang_code}'] = getattr(product, f'description_{lang_code}', '')
            product_info[f'summery_{lang_code}'] = getattr(product, f'summery_{lang_code}', '')
            product_info[f'price_{lang_code}'] = getattr(product, f'price_{lang_code}', '')
            product_info[f'offer_price_{lang_code}'] = getattr(product, f'offer_price_{lang_code}', '')

        products_data.append(product_info)


    # Create DataFrame and response for Excel export
    df = pd.DataFrame(products_data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products_export.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Products')

    return response

# product/utils.py

def import_products_from_excel(file):
    # Read the Excel file
    df = pd.read_excel(file, engine='openpyxl')

    # Iterate through DataFrame and create or update Product objects
    for _, row in df.iterrows():
        product_data = {
            'title': row.get('title'),
            'slug': row.get('slug'),
            'description': row.get('description'),
            'summery': row.get('summery'),
            'price': row.get('price'),
            'offer_price': row.get('offer_price'),
            'category': row.get('category'),            
            'is_active': row.get('is_active'),
            'stock': row.get('stock'),
            'size': row.get('size'),
            'guarantee': row.get('guarantee'),
            'time_to_bring': row.get('time_to_bring')
        }

        # Create or update the product
        product, created = Product.objects.update_or_create(
            id=row.get('id'),
            defaults=product_data
        )
        # Set translated fields for each language
        for lang_code, _ in settings.LANGUAGES:
            setattr(product, f'title_{lang_code}', row.get(f'title_{lang_code}', ''))
            setattr(product, f'description_{lang_code}', row.get(f'description_{lang_code}', ''))
            setattr(product, f'summery_{lang_code}', row.get(f'summery_{lang_code}', ''))
            setattr(product, f'price_{lang_code}', row.get(f'price_{lang_code}', ''))
            setattr(product, f'offer_price_{lang_code}', row.get(f'price_{lang_code}', ''))


        product.save()