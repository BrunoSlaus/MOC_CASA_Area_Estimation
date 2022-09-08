
import numpy as np
import datetime
import sys
#sys.setrecursionlimit(200)

##########################################################
Input  = 'Input/'  
Output = 'Output/'  
Field_1_Name = 'XXL-N_GMRT610.FITS'
Field_2_Name = 'mask_inner.fits'              
##########################################################
Field_1 = Input + Field_1_Name 
Field_2 = Input + Field_2_Name 

#CREATING A [0,1] MASK FROM IMAGE_1
immath(imagename=Field_1 ,mode='evalexpr',expr = ' iif( IM0 >=-10e99, 1.0, 0.0)' ,outfile=Output+'Mask_F1.image')
exportfits(imagename= Output + 'Mask_F1.image', fitsimage = Output+'Mask_F1.fits', overwrite = True)
os.system('rm -rf ' + Output + 'Mask_F1.image')

#CREATING A [0,1] MASK FROM IMAGE_2
immath(imagename=Field_2 ,mode='evalexpr',expr = ' iif( IM0 >=-10e99, 1.0, 0.0)' ,outfile=Output+'Mask_F2.image')
exportfits(imagename= Output + 'Mask_F2.image', fitsimage = Output+'Mask_F2.fits', overwrite = True)
os.system('rm -rf ' + Output + 'Mask_F2.image')

#ADDING THE FIELDS i.e. CREATING A [0,1,2] MASK: 2 IS THE INTERSECTION
immath(imagename=[Output+'Mask_F1.fits', Output+'Mask_F2.fits'] ,mode='evalexpr',expr = 'IM0 + IM1' ,outfile=Output+'Mask_Sum.image')   
immath(imagename=Output+'Mask_Sum.image' ,mode='evalexpr',expr = ' iif( IM0 >=1.5, 1.0, 0.0)' ,outfile=Output+'Mask_Intersection.image')
exportfits(imagename= Output+'Mask_Intersection.image', fitsimage = Output+'Mask_Intersection.fits', overwrite = True)
os.system('rm -rf ' + Output+'Mask_Sum.image')
os.system('rm -rf ' + Output+'Mask_Intersection.image')

#CALCULATING THE AREA OF INTERSECTION
Statistic  = imstat(imagename = Output+'Mask_Intersection.fits')
Area_Pixel = Statistic['sum']
print('The area of intersection is: ', Area_Pixel[0], ' in pixels.')
Header = imhead(imagename= Output+'Mask_Intersection.fits', mode='list')
X_Pixel = Header['cdelt1']    #cdeltn == Pixel size, nth axis. n is one-based
Y_Pixel = Header['cdelt2']    #cdeltn == Pixel size, nth axis. n is one-based
Area    = Area_Pixel * X_Pixel * Y_Pixel
Area    = Area * 57.295779513 * 57.295779513 #Radians to degrees
Area    = np.absolute(Area[0])               #Absolute value
print('The area of intersection is: ', Area, ' in sq. deg.')

##########################################################
#END OF CODE
#Modification History:
#1) Added the area calculations
#2) Do I need datetaime? I think i don't...
#3) 
##########################################################



