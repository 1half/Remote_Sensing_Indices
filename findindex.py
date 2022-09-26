import numpy as np
from osgeo import gdal, ogr,osr
import matplotlib.pyplot as plt
import glob,os,pathlib


def ToRasterArray(band):
    """
    Create list of raster array
    """
    
    Rast_Band=[]
    for b in band:
        Rast_Band.append(b.GetRasterBand(1).ReadAsArray().astype(np.float32))
    return Rast_Band

def saveRaster(dataset,datasetPath,cols,rows,projection,geotransform):
    rasterSet = gdal.GetDriverByName('GTiff').Create(datasetPath,cols, rows,1,gdal.GDT_Float32)
    rasterSet.SetProjection(projection)
    rasterSet.SetGeoTransform(geotransform)
    rasterSet.GetRasterBand(1).WriteArray(dataset)
    rasterSet.GetRasterBand(1).SetNoDataValue(-999)
    rasterSet = None

#INDICIES

def get_ndvi(B_5,B_4):
    ndvi = np.divide(B_5 - B_4, B_4+ B_5,where=(B_5 - B_4)!=0)
    return ndvi

def get_ndwi(B_5,B_3):
    ndwi = np.divide(B_3 - B_5, B_3+ B_5,where=(B_3 - B_5)!=0)
    return ndwi

def get_mndwi(B_6,B_3):
    mndwi = np.divide(B_3 - B_6, B_3+ B_6,where=(B_3 - B_6)!=0)
    return mndwi


def get_ndmi(B_5,B_6):
    ndmi = np.divide(B_5 - B_6, B_5+ B_6,where=(B_5 - B_6)!=0)
    return ndmi

def get_awei(B_5,B_3,B_7,B_6):
    awei = 4 * (B_3 - B_7) - (0.25 * B_5 + 2.75 * B_6) 
    return awei

def get_wri(B_5,B_3,B_4,B_7):
    wri = np.divide(B_3 + B_4, B_5+ B_7)
    return wri

def get_n2(B_5,B_7):
    #p = (2.713*np.log((B_2+B_3)))
    TN = np.divide((B_5-B_7),(0.865-2.2))
    return TN


def IndexCalculation(path_input,outPath):
    """
    path_input : Image folder path containing Band collection from same time.
    outPath : Out put folder path.
    
    """
    
    List_of_img = glob.glob(path_input+'/*B*.TIF')
    List_of_img.sort()
    #bands = []
    raster_array = []
    folderNm = pathlib.PurePath(path_input).name[:40]
    #fileNm = pathlib.PurePath(path_input).name
    
    for img in List_of_img:
        W_im = gdal.Open(img)
        #rasterBand = W_im.GetRasterBand(1)
        raster_array.append(W_im.GetRasterBand(1).ReadAsArray().astype(np.float32))

        #crs_ = osr.SpatialReference(wkt=W_im.GetProjection())
        
    cols =  W_im.RasterXSize
    rows =  W_im.RasterYSize
    projection = W_im.GetProjection()
    geotransform = W_im.GetGeoTransform()
    originX,pixelWidth,empty,finalY,empty2,pixelHeight=geotransform
        
    NDVI = get_ndvi(raster_array[4],raster_array[3])
    #os.mkdir(outPath+'/'+folderNm)
    saveRaster(NDVI,outPath+'/'+folderNm+'/NDVI'+folderNm+'.tif',cols,rows,projection,geotransform)
    
    NDWI = get_ndwi(raster_array[4],raster_array[2])
    saveRaster(NDWI,outPath+'/'+folderNm+'/NDWI'+folderNm+'.tif',cols,rows,projection,geotransform)

    MNDWI = get_mndwi(raster_array[5],raster_array[2])
    saveRaster(MNDWI,outPath+'/'+folderNm+'/MNDWI'+folderNm+'.tif',cols,rows,projection,geotransform)
    
    NDMI = get_ndmi(raster_array[4],raster_array[5])
    saveRaster(NDMI,outPath+'/'+folderNm+'/NDMI'+folderNm+'.tif',cols,rows,projection,geotransform)
    
    AWEI = get_awei(raster_array[4],raster_array[2],raster_array[6],raster_array[5])
    saveRaster(AWEI,outPath+'/'+folderNm+'/AWEI'+folderNm+'.tif',cols,rows,projection,geotransform)
    
    WRI = get_wri(raster_array[4],raster_array[2],raster_array[3],raster_array[6])
    saveRaster(WRI,outPath+'/'+folderNm+'/WRI'+folderNm+'.tif',cols,rows,projection,geotransform)
    
    




