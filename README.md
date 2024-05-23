# Miscellaneous

Repo for versioning various utility code. 

## arXiv
This notebook is used to extract relevant arXiv article from their daily mail, based on a selection of keywords.

## Reprojection
Small notebook for reprojecting a DSM into the correct geometry and resampling it and its mask. Usefull for comparing LiDAR DSM with CARS DSM.

## Pleiade_DEM_and_ROI_extractor
Small notebook to extract the correct SRTM or COPERNICUS DEM given a Pleiade image. This DEM is to be used as `initial_elevation` for CARS.
The second part is used to extract a ROI from Pleiade images that are not georeferenced based on a ROI. It gives the image coordinates (row, col) to be used for `otbcli_ExtractROI` 

## Interval investigation
Old notebook with Pandora interval processings. To be honest it is not maintained and probably is out of dated with the interval integration of Pandora
