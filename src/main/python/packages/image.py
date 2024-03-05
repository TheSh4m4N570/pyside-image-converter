import os
from PIL import Image


class ImageConverter:
    def __init__(self, path, folder="resized"):
        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.path = path
        self.resized_path = os.path.join(os.path.dirname(self.path),
                                         folder,
                                         os.path.basename(self.path)
                                         )

    def resize_image(self, size=0.5, quality=75):
        new_width = round(self.width * size)
        new_height = round(self.height * size)
        self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        parent_dir = os.path.dirname(self.resized_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        self.image.save(self.resized_path, 'JPEG', quality=quality)
        return os.path.exists(self.resized_path)


if __name__ == '__main__':
    image = ImageConverter("/home/sh4m4n570/Pictures/ezzio.jpeg")
    image.resize_image(size=1, quality=50)
