# Remote_Sensing_Indices

### Finding some common remote sensing indices with python.
The reflectance of surfaces are different, this can be utilized to study an area using satellite image. Various indices can be calcualted using reflectance of different wavelength of light on differnt surfaces.

_______________________________________________________________________________________________
#### Normalised Difference Vegetation Index (NDVI):
It quantifies vegetation by computing the difference between near-infrared and red light.
#### NDV I = NIR − Red/NIR + Red

#### Modified Normalised Difference Water Index (MNDWI):
The Modified Normalized Difference Water Index (MNDWI) uses green and SWIR bands for the enhancement of open water features.
#### MNDWI = (Green–SWIR)/(Green + SWIR)

#### Normalised Difference Water Index (NDWI):
Normalized Difference Moisture Index (NDMI) is used to determine vegetation water content.
#### NDMI = (NIR–SWIR1)/(NIR + SWIR1)

#### Automated Water Extraction Index (AWEI)
AutomatedWater Extraction Index (AWEI) have high in detecting water even in areas that include shadow and dark surfaces.
#### AWEI = 4 ∗ (Green − SWIR2) − (0.25 ∗ NIR + 2.75 ∗ SWIR1)
_______________________________________________________________________________________________

### Data source
The data used are landsat 8 L2(level 2: Images with atmospheric correction done on them) images.
Landsat images can be downloaded for free using the website: https://earthexplorer.usgs.gov/
after signing in their website.

### Packages Used

• GDAL(Geo-spatial Data Abstraction Library): For reading and writing raster and vector files.

• Numpy :For calculation using Array.

• Matplotlib : For plotting.

• Geopanda : For working with geo-spatial data.

It recomended that the packages are installed in a new environment. Conda can be used to create the env using the command below on anaconda prompt.

'conda install -n myenv numpy gdal geopandas matplotlib' (myenv is the name of your environment)

This can help to avoid dependancy issues.

