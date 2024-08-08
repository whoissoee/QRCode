import matplotlib.pyplot as plt
import numpy as np
import qrcode
from PIL import Image


class QRCodeWithBackground:
    def __init__(
        self, text, background_image_path=None, alpha=0.4, with_background=True
    ):
        """
        Initializes a new instance of the QRCodeWithBackground class.

        Args:
            text (str): The text to be encoded in the QR code.
            background_image_path (str, optional): The path to the background image file. Defaults to None.
            alpha (float, optional): The transparency level of the QR code overlay on the background image. Defaults to 0.4.
            with_background (bool, optional): Whether to use a background image. Defaults to True.

        Raises:
            FileNotFoundError: If the background_image_path is provided but the file does not exist.

        Returns:
            None
        """
        self.text = text
        self.alpha = alpha
        self.with_background = with_background
        self.qr_image = None
        self.background_image = None
        self.qr_array = None
        self.background_array = None
        self.result_image = None

        if self.with_background and background_image_path:
            self.background_image = Image.open(background_image_path).convert("RGBA")

    def generate_qr_code(self):
        """
        Generates a QR code based on the input text.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.text)
        qr.make(fit=True)
        self.qr_image = qr.make_image(fill_color="black", back_color="white").convert(
            "RGBA"
        )

    def resize_background_image(self):
        """
        Resizes the background image to match the size of the QR image using Lanczos resampling.
        """
        if self.background_image:
            self.background_image = self.background_image.resize(
                self.qr_image.size, Image.LANCZOS
            )

    def blend_images(self):
        """
        Blend the QR code image with the background image if specified.

        This method checks if the `with_background` attribute is True and if the `background_image` attribute is not None. If both conditions are met, it converts the `qr_image` and `background_image` into numpy arrays. It then creates a mask based on the alpha channel of the QR code image. The QR code image is then blended with the background image using the specified alpha value. The resulting image is stored in the `result_image` attribute.

        If the `with_background` attribute is False or the `background_image` attribute is None, the `qr_image` is converted to RGB format and stored in the `result_image` attribute.

        Parameters:
            None

        Returns:
            None
        """
        if self.with_background and self.background_image:
            self.qr_array = np.array(self.qr_image)
            self.background_array = np.array(self.background_image)
            #тут проебано 2 часа, так что лучше ничего не трогать.
            mask = self.qr_array[:, :, 3] > 0

            result_image = self.qr_array.copy()
            result_image[mask] = (
                self.qr_array[mask] * (1 - self.alpha)
                + self.background_array[mask] * self.alpha
            ).astype(np.uint8)

            self.result_image = Image.fromarray(result_image)
        else:
            self.result_image = self.qr_image.convert("RGB")

    def save_image(self, output_path):
        """
        Saves the result image to the specified output path.

        Args:
            output_path (str): The path where the image will be saved.

        Returns:
            None
        """
        self.result_image.save(output_path)

    def show_image(self):
        """
        Display the result image using matplotlib.pyplot.
        """
        plt.imshow(self.result_image)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    qr_with_background = QRCodeWithBackground("test", "assets/qrcode-bg.jpg", alpha=0.4)
    qr_with_background.generate_qr_code()
    qr_with_background.resize_background_image()
    qr_with_background.blend_images()
    qr_with_background.save_image("qr_code_with_background.png")
    qr_with_background.show_image()

    qr_without_background = QRCodeWithBackground("test", with_background=False)
    qr_without_background.generate_qr_code()
    qr_without_background.blend_images()
    qr_without_background.save_image("qr_code_without_background.png")
    qr_without_background.show_image()
