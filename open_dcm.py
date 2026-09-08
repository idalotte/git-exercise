# Load and display an example DICOM image

import matplotlib
matplotlib.use('TkAgg')  # fixes some freezes?
import matplotlib.pyplot as plt
import pydicom 

file_path = "/Users/ida-lotte/git-exercise/Dataset_Skills_01/CT/1.3.12.2.1107.5.1.4.105055.30000018070216565044500079806/1.3.12.2.1107.5.1.4.105055.30000018070216565044500079807.dcm"

def display_dicom_image(path):
    # Load the DICOM file
    dicom_data = pydicom.dcmread(path)
    
    # Extract the pixel array
    image_array = dicom_data.pixel_array

    #show the image
    plt.imshow(image_array, cmap='gray')
    plt.title('DICOM Image')
    plt.show()

display_dicom_image(file_path)