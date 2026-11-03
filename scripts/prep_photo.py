import sys, cv2
import numpy as np
from PIL import Image

def prep_photo(input_path="Teal Painterly Suit Portrait.png", output_path="source-prepped.png"):
    print(f"[*] Processing {input_path}...")
    img = Image.open(input_path).convert("RGBA")
    
    # White background composite
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, img).convert("L")
    
    # Boost local contrast with CLAHE
    img_np = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(img_np)
    
    cv2.imwrite(output_path, enhanced)
    print(f"[+] Saved to {output_path}")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "Teal Painterly Suit Portrait.png"
    prep_photo(path)
