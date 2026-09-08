# This lilcode loads and displays an example CT DICOM image + metadata

import matplotlib
import matplotlib.pyplot as plt
import pydicom 

#%% CT IMAGE
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
    # print(dicom_data) 
    
    # or more specifically: 
    print("Instance number:", dicom_data.InstanceNumber) # slice number in the series
    # print("Modality:", dicom_data.Modality)
    print("Image shape:", dicom_data.pixel_array.shape)
    # print("Rows:", dicom_data.Rows)
    # print("Columns:", dicom_data.Columns)
    print("Pixel spacing:", dicom_data.PixelSpacing)
    print("Slice thickness:", dicom_data.SliceThickness)
    # print("Min pixel value:", dicom_data.pixel_array.min())
    # print("Max pixel value:", dicom_data.pixel_array.max())
    print("Image position:", dicom_data.ImagePositionPatient)
    print("Image orientation:", dicom_data.ImageOrientationPatient)
    # print("Rescale slope:", dicom_data.RescaleSlope) #!!! used for HU conversion
    # print("Rescale intercept:", dicom_data.RescaleIntercept) #!!! used for HU conversion

#%% run the fuction to display the DICOM image
display_dicom_image(file_path)

#%% run function to display the DICOM metadata
display_dicom_metadata(file_path)


#%% RT DOSE

path_dose = "/Users/ida-lotte/Desktop/Dataset_Skills_01/RTDOSE/1.2.246.352.71.2.386771017546.4754743.20260707095012/1.2.246.352.71.7.386771017546.521623.20260707095440.dcm"
paht_dose_2 = "/Users/ida-lotte/Desktop/Dataset_Skills_01/RTDOSE/1.2.246.352.71.2.386771017546.4754743.20260707095012/1.2.246.352.71.7.386771017546.521623.20260707125603.dcm"


def display_dose_metadata(path):
    # Load the DICOM file
    dose_data = pydicom.dcmread(path)

    # Print the DICOM metadata
    # print(dose_data)
    
    # or more specifically: 
    # print("Modality:", dose_data.Modality)
    print("Image shape:", dose_data.pixel_array.shape)
    print(dose_data.get("DoseUnits"))
    print("Pixel spacing:", dose_data.PixelSpacing)
    print("Slice thickness:", dose_data.SliceThickness)
    # print("Min pixel value:", dose_data.pixel_array.min())
    # print("Max pixel value:", dose_data.pixel_array.max())
    print("Image position:", dose_data.ImagePositionPatient)
    print("Image orientation:", dose_data.ImageOrientationPatient)
    print("Dose grid scaling:",dose_data.get("DoseGridScaling"))
    print("Number of dose frames:", dose_data.NumberOfFrames)
    print("Dose frame offsets:", dose_data.GridFrameOffsetVector)



#%%
display_dose_metadata(path_dose)


#%% Select a specific slice from the dose distribution (path_dose)
ct_z = -638.5       # Z-coordinate of the CT slice
dose_Z0 = -673.5    # Z-coordinate of the first dose slice
slice_thickness = 1
dose_index = int((ct_z - dose_Z0) / slice_thickness) 
print("Dose slice index:", dose_index)


# %% correct z-direction dose slice extraction
dose_data = pydicom.dcmread(path_dose)
dose_GY = dose_data.pixel_array.astype(float)  # Convert to GY float for processing
scaling = dose_data.DoseGridScaling  # Get the dose grid scaling factordose_array *= scaling

dose_GY *= scaling

# so for the wanted slice index:
dose_slice = dose_GY[dose_index, :, :]

print("Dose slice shape:", dose_slice.shape)
print("Dose slice min:", dose_slice.min())
print("Dose slice max:", dose_slice.max())


# %% display the dose slice once before any overlaying etc
plt.imshow(dose_slice)
plt.title("Dose distribution")
plt.colorbar(label="Dose (Gy)")
plt.show()

# %% Starting with the physical coordinates
ct_data = pydicom.dcmread(file_path)
ct_image = ct_data.pixel_array.astype(float)
ct_image = ct_image * float(ct_data.RescaleSlope) + float(ct_data.RescaleIntercept) # Convert to HU

ct_x = ct_data.ImagePositionPatient[0]  
ct_y = ct_data.ImagePositionPatient[1]  

ct_row_spacing = ct_data.PixelSpacing[0]
ct_col_spacing = ct_data.PixelSpacing[1]

dose_x = dose_data.ImagePositionPatient[0]
dose_y = dose_data.ImagePositionPatient[1]

dose_row_spacing = dose_data.PixelSpacing[0]
dose_col_spacing = dose_data.PixelSpacing[1]

#%% how big each image is in physical space
ct_extent = [ # x_min, x_max, y_min, y_max
    ct_x, ct_x + ct_image.shape[1] * ct_col_spacing,
    ct_y, ct_y + ct_image.shape[0] * ct_row_spacing
]

dose_extent = [ # x_min, x_max, y_min, y_max
    dose_x, dose_x + dose_slice.shape[1] * dose_col_spacing,
    dose_y, dose_y + dose_slice.shape[0] * dose_row_spacing
]


# %% Display overlay

 dose_display = dose_slice.copy()
# dose_display[dose_display < 0.1] = float("nan")

plt.imshow(
    ct_image, cmap='gray', extent=ct_extent, origin='lower'
)
plt.imshow(
    dose_display, cmap='hot', alpha=0.3, extent=dose_extent, origin='lower'
)

# Show the full CT, not only the dose region
plt.xlim(ct_extent[0], ct_extent[1])
plt.ylim(ct_extent[2], ct_extent[3])

plt.colorbar(label="Dose (Gy)")
plt.xlabel("x position (mm)")
plt.ylabel("y position (mm)")
plt.title("CT + RT Dose")
plt.show()

# %%
