import logging
import os
import re
import sys

from osgeo import gdal
import otbApplication

path_zip = sys.argv[1]
target_path = sys.argv[2]
ram = int(sys.argv[3])
job_id = sys.argv[4]

logging.basicConfig(filename=f'{job_id}.log', level=logging.INFO, format="%(levelname)s : %(asctime)s - %(message)s", datefmt="%H:%M:%S")


assert os.system(f"unzip -l {path_zip} > list_zip_{job_id}.txt") == 0
with open(f"list_zip_{job_id}.txt", "r") as f:
    lines = f.readlines()[3:-2]

if len(lines) < 7 : # Maximimum if you ordered 2 tri-stereo
    root_zip = os.path.dirname(path_zip)
    list_zips = [os.path.join(root_zip, k.split("   ")[-1].split("\n")[0]) for k in lines]
    
    logging.info("Unzipping order %s", path_zip)
    os.system(f"unzip -n {path_zip} -d {root_zip}")
else: 
    list_zips = [path_zip]

for zip_file in list_zips:
    logging.info("ZIP file: %s", zip_file)
    assert os.system(f"unzip -l {zip_file} > list_zip_{job_id}.txt") == 0
    with open(f"list_zip_{job_id}.txt", "r") as f:
        lines = f.readlines()[3:-2]
    list_files = [k.split("   ")[-1].split("\n")[0] for k in lines]
    
    tmp_zip_dir = os.path.commonpath(list_files) # PWH-8355_2024-04-22_14-49-16_1001
    
    list_dims = [os.path.basename(f) for f in list_files if "DIM_PHR" in f]  # ['DIM_PHR1B_MS_201908271102544_SEN_PWH-8355_2024-04-22_14-49-16_1001-001.XML']
    date_image = re.search("[0-9]{15}", list_dims[0]).group()  # '201908271102544'
    date_format = date_image[:4] + "-" + date_image[4:6] + "-" + date_image[6:8] + "_" + date_image[8:10] + "h" + date_image[10:12] + "m" + date_image[12:]  # '2019-08-27_11h02m544'

    assert tmp_zip_dir != ""

    if not os.path.exists(os.path.join(target_path, date_format)):
        os.system(f"unzip -n {zip_file} -d {target_path}")
        logging.info("Renaming to %s", date_format)
        os.system(f"mv {os.path.join(target_path, tmp_zip_dir)} {os.path.join(target_path, date_format)}")
        try:
            os.mkdir(os.path.join(target_path, date_format, "OTB_IMG"))
        except FileExistsError:
            logging.info("Directory already exists.")
        
    img_folders = [f.replace(tmp_zip_dir + "/", date_format + "/") for f in list_files if "DIM_PHR" in f]
    dim_p = os.path.join(target_path, [f for f in img_folders if "_P_" in f][0])
    dim_ms = os.path.join(target_path, [f for f in img_folders if "_MS_" in f][0])
    
    img_p = os.path.join(target_path, date_format, "OTB_IMG", os.path.basename(dim_p).replace("DIM_", "IMG_").replace(".XML", ".TIF"))
    img_ms = os.path.join(target_path, date_format, "OTB_IMG", os.path.basename(dim_ms).replace("DIM_", "IMG_").replace(".XML", ".TIF"))
    
    logging.info("otbcli_ExtractROI -in %s -out %s -ram %s", dim_p, img_p, ram)

    # If .geom is not written, you can force it adding "&writegeom=<(bool)true>" to the out file parameter
    ExtractROI = otbApplication.Registry.CreateApplication("ExtractROI")
    ExtractROI.SetParameterString("in", dim_p)
    ExtractROI.SetParameterString("out", img_p)
    ExtractROI.SetParameterInt("ram", ram)
    ExtractROI.ExecuteAndWriteOutput()
    
    pansharp = os.path.join(target_path, date_format, "OTB_IMG", "COLOR_" + os.path.basename(img_p))
    # If .geom is not written, you can force it adding "&writegeom=<(bool)true>" to the out file parameter
    logging.info("otbcli_BundleToPerfectSensor -inp %s -inxs %s -out %s -ram %s", dim_p, dim_ms, pansharp, ram)

    BundleToPerfectSensor = otbApplication.Registry.CreateApplication("BundleToPerfectSensor")

    BundleToPerfectSensor.SetParameterString("inp", dim_p)
    BundleToPerfectSensor.SetParameterString("inxs", dim_ms)
    BundleToPerfectSensor.SetParameterString("out", pansharp)
    BundleToPerfectSensor.SetParameterInt("ram", ram)
    BundleToPerfectSensor.ExecuteAndWriteOutput()

    logging.info("Overview %s", img_p)
    Image = gdal.Open(img_p, 0)  # 0 = read-only, 1 = read-write.
    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    Image.BuildOverviews('NEAREST', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048], gdal.TermProgress_nocb)
    del Image  # close the dataset (Python object and pointers)
    
    logging.info("Overview %s", pansharp)
    Image = gdal.Open(pansharp, 0)  # 0 = read-only, 1 = read-write.
    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    Image.BuildOverviews('NEAREST', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048], gdal.TermProgress_nocb)
    del Image  # close the dataset (Python object and pointers)


