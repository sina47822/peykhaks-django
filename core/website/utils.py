# product/utils.py

import pandas as pd
from django.http import HttpResponse
from .models import Post, Category, Tags
from django.conf import settings

def export_posts_to_excel():
    # Select only the fields you want to export
    posts_data = []

    # Loop through each product and add translations for specified languages
    for post in Post.objects.all():
        # Get category IDs as a comma-separated string
        category_ids = ",".join(str(cat.id) for cat in post.categories.all())
        
        post_info = {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'desc_1': post.desc_1,
            'desc_2': post.desc_2,
            'post_summery': post.post_summery,
            'categories': post.category_ids,
            'blog_status': post.blog_status,
        }
        # Add translations for each language in settings.LANGUAGES
        for lang_code, _ in settings.LANGUAGES:
            post_info[f'title_{lang_code}'] = getattr(post, f'title_{lang_code}', '')
            post_info[f'desc_1_{lang_code}'] = getattr(post, f'desc_1_{lang_code}', '')
            post_info[f'desc_2_{lang_code}'] = getattr(post, f'desc_2_{lang_code}', '')
            post_info[f'post_summery_{lang_code}'] = getattr(post, f'post_summery_{lang_code}', '')

        posts_data.append(post_info)


    # Create DataFrame and response for Excel export
    df = pd.DataFrame(posts_data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=posts_export.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Posts')

    return response

# post/utils.py

def import_posts_from_excel(file):
    # Read the Excel file
    df = pd.read_excel(file, engine='openpyxl')

    # Iterate through DataFrame and create or update Post objects
    for _, row in df.iterrows():
        post_data = {
            'title': row.get('title'),
            'slug': row.get('slug'),
            'desc_1': row.get('desc_1'),
            'desc_2': row.get('desc_2'),
            'post_summery': row.get('post_summery'),
            'blog_status': row.get('blog_status')
        }

        # Create or update the post
        post, created = Post.objects.update_or_create(
            id=row.get('id'),
            defaults=post_data
        )

        # Get category ID from the row and assign it to the post
        category_id = row.get('categories')
        if category_id and Category.objects.filter(id=category_id).exists():
            post.categories_id = category_id  # Assign directly if ForeignKey
            post.save()
            
        # Set translated fields for each language
        for lang_code, _ in settings.LANGUAGES:
            setattr(post, f'title_{lang_code}', row.get(f'title_{lang_code}', ''))
            setattr(post, f'desc_1_{lang_code}', row.get(f'desc_1_{lang_code}', ''))
            setattr(post, f'desc_2_{lang_code}', row.get(f'desc_2_{lang_code}', ''))
            setattr(post, f'post_summery_{lang_code}', row.get(f'post_summery_{lang_code}', ''))
        post.save()