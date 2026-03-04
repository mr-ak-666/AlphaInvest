import cv2
import numpy as np
import os

class ImageProcessor:
    
    def process(self, input_path, output_path=None):
        
        
        # Read image
        img = cv2.imread(input_path)
        if img is None:
            raise Exception(f"Cannot read image: {input_path}")
        
        print(f"Original size: {img.shape[1]}x{img.shape[0]}")
        
        # 1. Resize (max 1024px)
        img = self.resize(img, max_size=1024)
        print(f"Resized to: {img.shape[1]}x{img.shape[0]}")
        
        # # 2. Remove noise
        # img = self.denoise(img)
        # print("Noise removed")
        
        # 3. Make brighter and clearer
        img = self.enhance(img)
        print("Enhanced")
        
        # 4. Make sharper
        img = self.sharpen(img)
        print("Sharpened")
        
        # Save
        if output_path is None:
            output_path = input_path.replace('.jpg', '_processed.jpg')
        
        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"Saved to: {output_path}")
        
        return output_path
    
    def resize(self, img, max_size=1024):
        """Resize image to max_size while keeping aspect ratio"""
        height, width = img.shape[:2]
        
        # Skip if already small
        # if height <= max_size and width <= max_size:
        #     return img
        
        # Calculate new size
        # if width > height:
        #     new_width = max_size
        #     new_height = int(height * max_size / width)
        # else:
        #     new_height = max_size
        #     new_width = int(width * max_size / height)
        
        # Resize
        resized = cv2.resize(img, (1920, 1080))
        return resized
    
    def denoise(self, img):
        """Remove noise from image"""
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        return denoised
    
    def enhance(self, img):
        """Make image brighter and more clear"""
        # Convert to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Enhance brightness
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def sharpen(self, img):
        """Make image sharper"""
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(img, -1, kernel)
        return sharpened

# Example usage
if __name__ == "__main__":
    processor = ImageProcessor()
    
    # Process image
    result = processor.process(input("Enter the input file path:- "))
    print(f"Done! Processed image: {result}")