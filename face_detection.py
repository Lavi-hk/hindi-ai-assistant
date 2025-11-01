"""
Face Detection Module for Hindi AI Assistant
Detects faces using webcam with OpenCV
"""

try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False
import numpy as np
from typing import Tuple


class FaceDetector:
    """
    Face detection using OpenCV's Haar Cascade classifier
    """
    
    def __init__(self):
        """Initialize the face detector"""
        if not CV2_AVAILABLE:
            raise ImportError("OpenCV not available")
        # Load pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.camera = None
    
    def initialize_camera(self, camera_index: int = 0):
        """
        Initialize camera
        
        Args:
            camera_index: Index of camera to use (default: 0)
        """
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                raise Exception("Camera not accessible")
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False
    
    def detect_face(self, frame: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Detect face in a frame
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Tuple of (face_detected, annotated_frame)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        face_detected = len(faces) > 0
        annotated_frame = frame.copy()
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                annotated_frame,
                'Face Detected',
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )
        
        return face_detected, annotated_frame
    
    def get_frame(self) -> Tuple[bool, np.ndarray]:
        """
        Get frame from camera
        
        Returns:
            Tuple of (success, frame)
        """
        if self.camera is None:
            return False, np.zeros((480, 640, 3), dtype=np.uint8)
        
        ret, frame = self.camera.read()
        return ret, frame
    
    def release_camera(self):
        """Release camera resources"""
        if self.camera is not None:
            self.camera.release()
            cv2.destroyAllWindows()


def test_face_detection():
    """Test function for face detection"""
    detector = FaceDetector()
    
    if not detector.initialize_camera():
        print("Failed to initialize camera")
        return
    
    print("Face detection started. Press 'q' to quit.")
    
    while True:
        ret, frame = detector.get_frame()
        
        if ret:
            face_detected, annotated_frame = detector.detect_face(frame)
            
            # Display status
            status = "User Detected ✓" if face_detected else "No User Detected"
            print(status)
            
            # Show frame
            cv2.imshow('Face Detection', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    detector.release_camera()


if __name__ == "__main__":
    test_face_detection()

