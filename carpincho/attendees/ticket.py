import attr
from pdf2image import convert_from_path
import numpy as np
import cv2


@attr.s
class Ticket:

    code: str = attr.ib()
    _qr_box = (1140, 140, 1490, 490)
    _detector = cv2.QRCodeDetector()

    @classmethod
    def from_pdf(cls, pdf_path):
        images = convert_from_path(pdf_path)
        if not images:
            raise Exception("Can not find images")
        qr_img = images[0].crop(cls._qr_box)
        code, _, _ = cls._detector.detectAndDecode(np.array(qr_img))
        if len(code) != 21:
            raise ValueError(f"Wrong qr decoded: {code}")
        return cls(code)
