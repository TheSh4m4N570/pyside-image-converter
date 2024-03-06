import os
from PIL import Image


class ImageConverter:
    """

    The `ImageConverter` class represents an image converter that can resize an image and save it to a specified folder.

    ## Initialization

    To create an instance of the `ImageConverter` class, you need to provide the path to the original image file. You can optionally specify the folder where the resized image should be
    * saved. If no folder is specified, the resized image will be saved in a folder named "resized" within the same directory as the original image.

    Example:

    ```python
    converter = ImageConverter('path/to/original/image.jpg', folder='resized')
    ```

    ## Methods

    ### resize_image

    The `resize_image` method resizes the image to the specified size and saves it to the specified folder. By default, it resizes the image to 50% of its original size and uses a quality
    * of 75 for the output JPEG file.

    Parameters:
    - `size` (float): The resize factor as a decimal value. Defaults to 0.5.
    - `quality` (int): The output JPEG quality as an integer between 1 and 100. Defaults to 75.

    Returns:
    - `bool`: True if the resized image was saved successfully, False otherwise.

    Example:

    ```python
    success = converter.resize_image(size=0.8, quality=90)
    if success:
        print("Resized image saved successfully.")
    else:
        print("Failed to save resized image.")
    ```

    """
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
