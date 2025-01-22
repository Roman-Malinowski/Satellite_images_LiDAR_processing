# README

Repo for versioning various utility code. 
This repo is mainly used for the tutorial here : https://confluence.cnes.fr/pages/viewpage.action?pageId=469637529
## arXiv
This notebook is used to extract relevant arXiv article from their daily mail, based on a selection of keywords.

## Pleiade_zip_to_img
Contains scripts to process Airbus Pleiade products: unzipping, extracting to .TIF, pansharpening.
Also contains a script to georeference the Pleiade images in case QGIS can't do it on its own. It does what the QGIS Georeferencer does, so you can directly use QGIS to do it. 

## Pleiade_DEM_and_ROI_extractor
Small notebook to extract the correct SRTM or COPERNICUS DEM given a Pleiade image. This DEM is to be used as `initial_elevation` for CARS.
The second part is used to extract a ROI from Pleiade images that are not georeferenced based on a polygone .shp. It gives the image coordinates (row, col) to be used for `otbcli_ExtractROI` 

## Download_and_Rasterize_LiDAR_HD
Handy scripts for getting LiDAR HD. Contains its own `README.md`

## Reprojection
Small notebook for reprojecting a DSM into the correct geometry and resampling it and its mask. Usefull for comparing LiDAR DSM with CARS DSM.

## Interval investigation
Old notebook with Pandora interval processings. To be honest it is not maintained and probably is out of dated with the interval integration of Pandora
