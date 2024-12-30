import os
from django.core.management.base import BaseCommand
from PIL import Image
from product.models import Product  # مدل مربوطه را وارد کنید


class Command(BaseCommand):
    help = "Convert existing images to WebP and AVIF formats"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            if not product.image:
                continue

            img_path = product.image.path
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