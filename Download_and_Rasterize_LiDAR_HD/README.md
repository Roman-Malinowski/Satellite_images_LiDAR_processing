# Turning LiDAR HD into a DSM

This projects helps downloading LiDAR HD data from IGN's website, aggregating the different point clouds and rasterizing it

## Requirements
The following packages must be installed
```
numpy
pandas
laspy
rasterio
cars-rasterize
```

## Downloading the data
Go to [IGN website](https://geoservices.ign.fr/lidarhd), and select the tiles you want to download. You should obtain a `list_dalles.txt` file containing download links.
You can either manually download all those tiles, or if there are too many, use the `lidar_hd_download.sh` SLURM script to do it faster.

#### lidar_hd_download.sh
To use this script, first open your proxy (`source ~/set_proxy.sh` or the name of your proxy script), so you can access the internet.
- Make sure to modify the number of parallel jobs in the scipt so it matches the number of tiles you want to download. For instance if you have 42 tiles, then the slurm file should have the following line
`#SBATCH --array=1-42:1%42`
- Select the output log file paths etc.
- Select the full path of the file `list_dalles.txt`, containing the download links
- Select the output folder where the .laz will be downloaded
- Select the venv with laspy, pandas etc. installed
- If you want to have statistics about acquisition dates, X and Y positions of the files, make sure that the path to `compute_laz_date.py` is correct at the end of the file. If you don't wan't the statistics, remove the path


## Rasterizing the data
`Laz_processing.ipynb` is a simple notebook used to process the data:
- The first cells allow to compute statistics on a .laz file (min/max X,Y, acquisition time)
- Then we fuse multiple .laz files on a single one.
- Finally, we rasterize the global .laz file using cars-rasterize. This step takes a bit of time and is quite greedy in memory depending on the size of your .laz file, so consider allocating more memory if it does not work.


