from PIL import Image as PILImage
from io import BytesIO
import os

from rest_framework import serializers


def convert_image_to_web(file, quality=85, lossless=False):
    try:
        image = PILImage.open(file)

        # Convert RGBA to RGB if saving as JPEG-like WebP
        if image.mode in ("RGBA", "LA", "P") and not lossless:
            background = PILImage.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            background.paste(
                image, mask=image.split()[-1] if image.mode in ("RGBA", "LA") else None
            )
            image = background

        output = BytesIO()

        # Use method=6 for maximum compression (slower but smaller files)
        image.save(
            output,
            format="WEBP",
            quality=quality,
            method=6,  # 0-6, higher = better compression but slower
            lossless=lossless,
        )

        output.seek(0)
        filename = os.path.splitext(file.name)[0] + ".webp"
        file_content = output.getvalue()
    except Exception as e:
        raise serializers.ValidationError(f"Failed to convert image to WebP: {str(e)}")
    return filename, file_content
