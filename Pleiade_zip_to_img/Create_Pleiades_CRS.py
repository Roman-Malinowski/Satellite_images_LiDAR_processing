import os
import xml.etree.ElementTree as ET

from osgeo import gdal

root_folder = "/work/CAMPUS/etudes/3D/Development/malinoro/Pleiades/Bogota/2016-01-09_15h25m110/IMG_PHR1A_P_001"
input_img = "IMG_PHR1A_P_201601091525110_SEN_PWH-8334_2024-04-09_15-23-49_986-001_R1C1.TIF"
dim_xml = "DIM_PHR1A_P_201601091525110_SEN_PWH-8334_2024-04-09_15-23-49_986-001.XML"

output_img = "/work/CAMPUS/etudes/3D/Development/malinoro/Pleiades/Bogota/2016-01-09_15h25m110/Georeferenced_201601091525110.TIF"

tree = ET.parse(os.path.join(root_folder, dim_xml))
root_xml = tree.getroot()

vertices = root_xml.find("Dataset_Content").find("Dataset_Extent").findall("Vertex")
list_gcp = []
for vertex in vertices:
    lat = float(vertex.find("LAT").text)
    lon = float(vertex.find("LON").text)
    row = int(vertex.find("ROW").text) - 1
    col = int(vertex.find("COL").text) - 1
    
    z = 0
    gcp = gdal.GCP(lon, lat, z, col, row)
    print(gcp)
    list_gcp += [gcp]

src_img = gdal.Open(os.path.join(root_folder, input_img))

tmp = gdal.Translate(os.path.join(os.path.dirname(output_img), "tmp.tif"), src_img, GCPs=list_gcp, format="GTiff")

gdal.Warp(output_img, tmp, format="GTiff", dstSRS="EPSG:4326", resampleAlg="near")
os.remove(os.path.join(os.path.dirname(output_img), "tmp.tif"))

Image = gdal.Open(output_img, 0)  # 0 = read-only, 1 = read-write.
gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
Image.BuildOverviews('NEAREST', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048], gdal.TermProgress_nocb)
del Image  # close the dataset (Python object and pointers)