"""Build-time check for the production NumPy/OpenCV startup regression."""

import cv2
import numpy as np

from app import app

assert np.__version__ == "1.24.3", np.__version__
# Exercise the binary interface as well as importing the packages.
encoded, _ = cv2.imencode(".jpg", np.zeros((8, 8, 3), dtype=np.uint8))
assert encoded, "OpenCV failed to encode a NumPy image"
with app.test_client() as client:
    response = client.post("/detect")
    assert response.status_code == 200, response.status_code
    assert response.get_json() == {"error": "no image found"}, response.get_json()

print(f"Image startup check passed: NumPy {np.__version__}, OpenCV {cv2.__version__}")
