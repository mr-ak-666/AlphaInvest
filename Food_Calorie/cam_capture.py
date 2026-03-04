import cv2
import os
from datetime import datetime

class Camera:
    
    def __init__(self):
        self.camera = None
    
    def open(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Cannot open camera")
        print("Camera opened")
    
    
    def capture_with_preview(self, save_path="Food_Calorie/capture_save"):

        if self.camera is None:
            self.open()
        
        os.makedirs(save_path, exist_ok=True)
        
        print("Press SPACE to capture, ESC to cancel")
        
        while True:
            success, frame = self.camera.read()
            
            # f1 =  cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            f1 = frame
            if not success:
                break
            
            
            # Show live preview
            cv2.imshow('Camera' , f1)
            
            key = cv2.waitKey(1)

            # ESC to cancel
            if key == 27:
                cv2.destroyAllWindows()
                return None
            
            # SPACE to capture
            if key == 32:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{save_path}/photo_{timestamp}.jpg"
                cv2.imwrite(filename, f1)
                cv2.destroyAllWindows()
                print(f"Photo captured: {filename}")
                return filename
        
        cv2.destroyAllWindows()
        return None
    
    def close(self):
        """Close camera"""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
            print("Camera closed")

# Example usage
if __name__ == "__main__":
    cam = Camera()
    
    # Simple capture
    # photo = cam.capture()
    
    # Or with preview
    photo = cam.capture_with_preview()
    
    cam.close()