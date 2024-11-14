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
            'code': product.Code  # Include the code field if it exists
        }

        # Get categories as a comma-separated list of category names
        product_info['category'] = ", ".join([str(cat.id) for cat in product.category.all()])

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
        # Prepare fields for update, but only include them if they are not NaN
        product_data = {}
        
        if pd.notna(row.get('title')):
            product_data['title'] = row.get('title')
        if pd.notna(row.get('slug')):
            product_data['slug'] = row.get('slug')
        if pd.notna(row.get('description')):
            product_data['description'] = row.get('description')
        if pd.notna(row.get('summery')):
            product_data['summery'] = row.get('summery')
        # Set a default price if the price field is NaN, or skip it if necessary
        if pd.notna(row.get('price')):
            product_data['price'] = row.get('price')
        else:
            product_data['price'] = 0  # Set to 0 or any other default value

        if pd.notna(row.get('offer_price')):
            product_data['offer_price'] = row.get('offer_price')
        if pd.notna(row.get('is_active')):
            product_data['is_active'] = True if row.get('is_active') == 'active' else False
        if pd.notna(row.get('stock')):
            product_data['stock'] = row.get('stock')
        if pd.notna(row.get('size')):
            product_data['size'] = row.get('size')
        if pd.notna(row.get('guarantee')):
            product_data['guarantee'] = row.get('guarantee')
        if pd.notna(row.get('time_to_bring')):
            product_data['time_to_bring'] = row.get('time_to_bring')
        # Handle Code field specifically with uppercase "C"
        if pd.notna(row.get('Code')):
            product_data['Code'] = row.get('Code')
        # Create or update the product, updating only specified fields in product_data
        product, created = Product.objects.update_or_create(
            id=row.get('id'),
            defaults=product_data
        )

        # Handle category IDs from the Excel row
        category_ids = row.get('category')
        if pd.notna(category_ids):
            category_ids_list = [int(cat_id.strip()) for cat_id in str(category_ids).split(',') if cat_id.strip().isdigit()]
            product.category.set(category_ids_list)
            
        # Set translated fields for each language, only if they are not NaN
        for lang_code, _ in settings.LANGUAGES:
            title_column = f'title_{lang_code}'
            description_column = f'description_{lang_code}'
            summery_column = f'summery_{lang_code}'
            price_column = f'price_{lang_code}'
            offer_price_column = f'offer_price_{lang_code}'

            if title_column in row and pd.notna(row.get(title_column)):
                setattr(product, title_column, row.get(title_column))
            if description_column in row and pd.notna(row.get(description_column)):
                setattr(product, description_column, row.get(description_column))
            if summery_column in row and pd.notna(row.get(summery_column)):
                setattr(product, summery_column, row.get(summery_column))
            if price_column in row and pd.notna(row.get(price_column)):
                setattr(product, price_column, row.get(price_column))
            if offer_price_column in row and pd.notna(row.get(offer_price_column)):
                setattr(product, offer_price_column, row.get(offer_price_column))

        # Save the product only if any fields have been updated
        product.save()