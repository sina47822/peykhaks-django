import os
from django.core.management.base import BaseCommand
from PIL import Image
from website.models import Post  # مدل مربوطه را وارد کنید


class Command(BaseCommand):
    help = "Convert existing images to WebP and AVIF formats"

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        for post in posts:
            if not post.image:
                continue

            img_path = post.image.path
            self.convert_image(img_path)

        self.stdout.write(self.style.SUCCESS("Image conversion completed!"))

    def convert_image(self, img_path):
        base, ext = os.path.splitext(img_path)
        webp_path = f"{base}.webp"
        avif_path = f"{base}.avif"

        try:
            with Image.open(img_path) as img:
                # تبدیل به WebP
                img.save(webp_path, format="WEBP", quality=85)
                self.stdout.write(f"Converted to WebP: {webp_path}")

                # تبدیل به AVIF
                img.save(avif_path, format="AVIF", quality=85)
                self.stdout.write(f"Converted to AVIF: {avif_path}")
        except Exception as e:
            self.stderr.write(f"Error converting {img_path}: {e}")