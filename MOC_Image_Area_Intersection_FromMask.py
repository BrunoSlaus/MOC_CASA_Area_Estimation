from astropy.io import fits
import numpy as np
from mocpy import MOC
import matplotlib.pyplot as plt
from math import pi

##################################################
Input_Folder  = 'Input/'
Output_Folder = 'Output/'

Field_1_Name  = 'Mask_IN.fits'  #Image
#Field_1_Name  = 'XXL-N_GMRT610.FITS'  #Image
Field_2_Name  = 'XXL-N_irac_ch1.fits' #Table

h_path     = Input_Folder + 'mask_inner.fits'

##################################################
image_path = Input_Folder + Field_1_Name

hdulist_init = fits.open(image_path)
data_init = fits.getdata(image_path)
header = hdulist_init[0].header

data_init  = data_init[0,0,:,:]
N_XPixels = len(data_init[:,0]) 
N_YPixels = len(data_init[0,:])

print('\n#############################################')
print('Starting the pixel counting area calculation: ')
print('X-Pixels == ', N_XPixels)
print('Y-Pixels == ', N_YPixels)
print('Total number of pixels == X-Pixels * Y-Pixels')
print('                       == ', N_XPixels * N_YPixels)

XPixel_Length = np.absolute(header['CDELT1'])
YPixel_Length = np.absolute(header['CDELT2'])
print('X-Pixel_Length == ', XPixel_Length)
print('Y-Pixel_Length == ', YPixel_Length)

print('\nNumber of pixels within field i.e. not NaN:')
N_Pixels_Field = np.count_nonzero(data_init==1)  #CHANGED IN THIS CODE!!!
print(N_Pixels_Field)

Area_total = XPixel_Length * YPixel_Length * N_XPixels * N_YPixels
Area_Field = XPixel_Length * YPixel_Length * N_Pixels_Field 
print('\nArea_total == ', Area_total)
print('Area_Field == ', Area_Field)
print('#############################################\n')



#data_init[data_init>-10e99] = 1       #Creating the mask CHANGED IN THIS CODE!!!
data_init = np.nan_to_num(data_init)   #Creating the mask 
print('Walues in the mask data: ', np.unique(data_init))

#Creating a new fits-image i.e. the MASK
hdu = fits.PrimaryHDU()
hdu.data = data_init
hdulist_h = fits.open(h_path)
header = hdulist_h[0].header
header.remove('CTYPE3')
header.remove('CRVAL3')
header.remove('CDELT3')
header.remove('CRPIX3')
header.remove('CROTA3')
header.remove('CTYPE4')
header.remove('CRVAL4')
header.remove('CDELT4')
header.remove('CRPIX4')
header.remove('CROTA4')
header.remove('NAXIS3')
header.remove('NAXIS4')
header['NAXIS'] = 2
hdu.header = header
hdu.writeto(Output_Folder + 'SIMPLE.fits', overwrite = 'True')


#The MOC-area calculation
print('\n#############################################')
print('Starting the MOC area calculation: ')
with fits.open(Output_Folder + 'SIMPLE.fits') as Simple_hdulist:
    plt.imshow(Simple_hdulist[0].data, origin='lower', cmap='gray')
    plt.show()
    print(Simple_hdulist[0].data)
    moc = MOC.from_image(header=Simple_hdulist[0].header,
                         moc_order=15,
                         mask_arr=Simple_hdulist[0].data)

moc.plot(title="MOC created from a fits image a mask")

square_degrees_sphere = (360.0**2)/pi
area_sq2 = round( ( moc.sky_fraction * square_degrees_sphere ), 1 )
print ('MOC calculation area == ', area_sq2, ' sq. deg' )


Table = fits.open(Input_Folder + Field_2_Name)[1].data
moc2 = MOC.from_table(Table, 'RA', 'DEC', 12)
area_sq2 = round( ( moc2.sky_fraction * square_degrees_sphere ), 1 )
print ('MOC Table area == ', area_sq2, ' sq. deg' )
moc2.plot(title="MOC from Table")

moc_intersection = moc.intersection(moc2)
moc_intersection.plot(title="MOC intersection")
area_sq2 = round( ( moc_intersection.sky_fraction * square_degrees_sphere ), 1 )
print ('MOC inersection area == ', area_sq2, ' sq. deg' )






