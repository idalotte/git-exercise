# This lilcode loads and displays an example CT DICOM image + metadata

import matplotlib
import matplotlib.pyplot as plt
import pydicom 

file_path = "/Users/ida-lotte/git-exercise/Dataset_Skills_01/CT/1.3.12.2.1107.5.1.4.105055.30000018070216565044500079806/1.3.12.2.1107.5.1.4.105055.30000018070216565044500079807.dcm"


# Function to display DICOM image in Hounsfield Units (HU)
def display_dicom_image(path):
    # Load the DICOM file
    dicom_data = pydicom.dcmread(path)

    # Display the image (in Hounsfield Units)
    image_array = dicom_data.pixel_array.astype(float) # pixel data in raw endoced bytes, convert to pixel array float for processing

    slope = getattr(dicom_data, 'RescaleSlope', 1) # default to 1 if not present
    intercept = getattr(dicom_data, 'RescaleIntercept', 0) # default to 0 if not present
    hu_image = image_array * slope + intercept # HU units conversion
    
    plt.imshow(hu_image, cmap='gray')
    plt.title('DICOM Image in Hounsfield Units')
    plt.colorbar(label='Hounsfield Units (HU)')
    plt.axis("off")  # Hide axis
    plt.show()


# Function to display DICOM metadata
def display_dicom_metadata(path):
    # Load the DICOM file
    dicom_data = pydicom.dcmread(path)

    # Print the DICOM metadata
    print(dicom_data) 
    
    # or more specifically: 
    # print("Modality:", dicom_data.Modality)
    # print("Rows:", dicom_data.Rows)
    # print("Columns:", dicom_data.Columns)
    # print("Pixel spacing:", dicom_data.PixelSpacing)
    # print("Slice thickness:", dicom_data.SliceThickness)
    # print("Min pixel value:", dicom_data.pixel_array.min())
    # print("Max pixel value:", dicom_data.pixel_array.max())
    # print("Image position:", dicom_data.ImagePositionPatient)
    # print("Image orientation:", dicom_data.ImageOrientationPatient)
    # print("Rescale slope:", dicom_data.RescaleSlope) #!!! used for HU conversion
    # print("Rescale intercept:", dicom_data.RescaleIntercept) #!!! used for HU conversion


#run the fuction to display the DICOM image
display_dicom_image(file_path)

#run function to display the DICOM metadata
display_dicom_metadata(file_path)
