import mss 
import base64

def capture_screen():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
    result = base64.standard_b64encode(img_bytes).decode("utf-8")
    return result