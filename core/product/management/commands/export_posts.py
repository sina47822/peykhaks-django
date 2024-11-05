import pandas as pd
from django.core.management.base import BaseCommand
from product.models import Product, ProductCategoryModel, Category, Tags, Standards

class Command(BaseCommand):
    help = 'Export data with translations to Excel'

    def handle(self, *args, **kwargs):
        # Exporting Product data with translations
        products = Product.objects.all()
        product_data = []
        for product in products:
            product_data.append({
                'ID': product.id,
                'Title': product.title,
                'Title (FA)': getattr(product, 'title_fa', ''),
                'Slug': product.slug,
                'Slug (FA)': getattr(product, 'slug_fa', ''),
                'Code': product.Code,
                'Description 1': product.desc_1,
                'Description 1 (FA)': getattr(product, 'desc_1_fa', ''),
                'Description 2': product.desc_2,
                'Description 2 (FA)': getattr(product, 'desc_2_fa', ''),
                'Summary': product.summery,
                'Summary (FA)': getattr(product, 'summery_fa', ''),
                'Price': product.price,
                'Offer Price': product.offer_price,
                'Image': product.image.url if product.image else None,
                'Stock': product.stock,
                'Size': product.size,
                'Guarantee': product.guarantee,
                'Total Views': product.total_views,
                'Is Active': product.is_active,
                'Update Date': product.update_date,
                'Create Date': product.create_date,
                'Publish Date': product.publish_date,
            })

        # Convert Product data to DataFrame and export to Excel
        product_df = pd.DataFrame(product_data)
        product_df.to_excel('products_export.xlsx', index=False, engine='openpyxl')

        # Exporting Standards data
        standards = Standards.objects.all()
        standards_data = []
        for standard in standards:
            standards_data.append({
                'ID': standard.id,
                'Title': standard.title,
                'Title (FA)': getattr(standard, 'title_fa', ''),
                'Slug': standard.slug,
                'Slug (FA)': getattr(standard, 'slug_fa', ''),
                'Standard ASTM': standard.standard_astm.name if standard.standard_astm else None,
                'Standard AASHTO': standard.standard_aashto.name if standard.standard_aashto else None,
                'Standard ISIRI': standard.standard_isiri.name if standard.standard_isiri else None,
            })

        # Convert Standards data to DataFrame and add to Excel file
        standards_df = pd.DataFrame(standards_data)
        with pd.ExcelWriter('products_export.xlsx', engine='openpyxl', mode='a') as writer:
            standards_df.to_excel(writer, sheet_name='Standards', index=False)

        # Exporting Product Categories data
        categories = ProductCategoryModel.objects.all()
        categories_data = []
        for category in categories:
            categories_data.append({
                'ID': category.id,
                'Title': category.title,
                'Title (FA)': getattr(category, 'title_fa', ''),
                'Slug': category.slug,
                'Created Date': category.created_date,
                'Updated Date': category.updated_date,
            })

        # Convert Categories data to DataFrame and add to Excel file
        categories_df = pd.DataFrame(categories_data)
        with pd.ExcelWriter('products_export.xlsx', engine='openpyxl', mode='a') as writer:
            categories_df.to_excel(writer, sheet_name='Product Categories', index=False)

        # Exporting Tags data
        tags = Tags.objects.all()
        tags_data = []
        for tag in tags:
            tags_data.append({
                'ID': tag.id,
                'Name': tag.name,
                'Name (FA)': getattr(tag, 'name_fa', ''),
                'Slug': tag.slug,
            })

        # Convert Tags data to DataFrame and add to Excel file
        tags_df = pd.DataFrame(tags_data)
        with pd.ExcelWriter('products_export.xlsx', engine='openpyxl', mode='a') as writer:
            tags_df.to_excel(writer, sheet_name='Tags', index=False)

        self.stdout.write(self.style.SUCCESS('Data exported successfully to products_export.xlsx'))
