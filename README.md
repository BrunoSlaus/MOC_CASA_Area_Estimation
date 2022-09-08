# MOC_CASA_Area_Estimation
MOC (mocpy) and CASA codes for estimating field areas from maps or catalogues


This folder contains the codes use to calculate the area of
the given field. They need CASA and MOC (mocpy library for python3).
MOC is short for Multi Order Coverage, which is a special
way of pixelating the given image. It was useful because
of the "intersection" command which quickly finds the
intersection between the 2 fields. MOC can also find the
area of the catalogue, assuming it is dense enough not to
introduce large errors.

We also give the CASA codes that estimate the area
using not catalogues but maps.

IT SHOULD BE NOTED THAT THESE CODES ARE RATHER PARTICULAR IN
THEIR USE BUT THEY CAN BE USED AS A REFERENCE FOR FURTHER CODING.

Contents:
1) CASA_Intersection.py:      This is the CASA code
                              that can be used to create the intersection
                              (or actually the MASK of the intersection)
                              between 2 fields. It also returns the area.
                              THIS CODE WORKS ONLY ON IMAGES AND NOT ON
                              CATALOGUES.

2) MOC_Image_Area_Intersection_FromMask.py :     This is the MOC-code
                                                 which can calculate the intersection between THE IMAGE AND A CATALOGUE. That made it useful
                                                 because at the time we had only the IRAC catalogue
                                                 and not the image.
             

