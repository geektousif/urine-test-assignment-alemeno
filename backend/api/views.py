from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2
import numpy as np

from .serializers import UrineStripImageSerializer

class UrineStripImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = UrineStripImageSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            image_file_path = default_storage.save(image_file.name, ContentFile(image_file.read()))
            full_image_path = default_storage.path(image_file_path)
            
            # here goes the processing
            rgb_values = self.process_image(full_image_path)

            default_storage.delete(image_file_path)

            return Response(rgb_values, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def process_image(self, image_path):
        
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply GaussianBlur to reduce noise and improve edge detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Assuming the largest contour is the strip, sort by area and get the largest
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        strip_contour = contours[0]
        
        # Get bounding box of the strip
        x, y, w, h = cv2.boundingRect(strip_contour)
        
        # Extract the strip region
        strip_region = image[y:y+h, x:x+w]
        
        # Determine the height of each segment
        segment_height = h // 10
        
        # Dictionary to store the results
        result = {}
        labels = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
        
        for i in range(10):
            # Extract the segment
            segment = strip_region[i * segment_height:(i + 1) * segment_height, :]
            
            # Focus on the central area of the segment
            central_region = segment[:, w//4:w*3//4]
            
            # Calculate the average color of the central region
            avg_color_per_row = np.average(central_region, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            # Convert to integers
            avg_color = avg_color.astype(int)
            # Store the result
            result[labels[i]] = avg_color.tolist()
        
        return result