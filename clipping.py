import numpy as np
from osgeo import gdal,ogr,osr
import glob,os,pathlib

def Create_boundBox(shape_save_path,projection):
    """
    shape_save_path : Path to which the created shape file is saved.
    projection : Cordinate reference of the shape obtained from the image.
    input for the cordinates are then given in input() fn according to the CRS
    
    """
    
    tllat = (float(input('Give TOP LEFT Lattitude in Decimal Degrees or northings in case of UTM:')))
    tllong = (float(input('Give TOP LEFT longitude in Decimal Degrees or eastings in case of UTM:')))

    brlat = (float(input('Give BOTTOM RIGHT Lattitude in Decimal Degrees or northings in case of UTM:')))
    brlong = (float(input('Give BOTTOM RIGHT Longitude in Decimal Degrees or eastings in case of UTM :')))

    Hdist = brlong-tllong
    Vdist = tllat-brlat
    shape_name = input('Give name for shape file(avoid invalied filenames):')
    #pointstllat,tllong
    #tllat,tllong,trlat,trlong,brlat,brlong,bllat,bllong =tllat,tllong ,tllat,tllong+Hdist ,brlat,brlong , tllat-Vdist,tllong
    print(tllat,tllong ,tllat,tllong+Hdist ,brlat,brlong , tllat-Vdist,tllong)


    ring = ogr.Geometry(ogr.wkbLinearRing) #(long,lat) anticlock
    ring.AddPoint(tllong,tllat-Vdist) #11.586101282798912, 77.63620736510678
    ring.AddPoint(brlong,brlat) #, 77.99657914761914
    ring.AddPoint(tllong+Hdist,tllat) #11.989962973654878, 78.00569199522926
    ring.AddPoint(tllong,tllat) #11.989962973654878
    ring.AddPoint(tllong,tllat-Vdist)

    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    driver = ogr.GetDriverByName("ESRI Shapefile")

    outds = driver.CreateDataSource(f"{shape_save_path}/{shape_name}.shp") # give path to save .shp
    Outlayer = outds.CreateLayer("Study_Area",projection)
    feature = ogr.Feature(Outlayer.GetLayerDefn())
    feature.SetGeometry(poly)
    Outlayer.CreateFeature(feature)

    outds = Outlayer = feature = None

    path_to_shape = f"{shape_save_path}/{shape_name}.shp"
    
    return path_to_shape

def clip_with_cordinate(path_input,outPath,path_to_shape,shape_available=False):
    """
    path_input : Image to be clipped is given.
    outPath : Out put folder path. Only give path for directry to which you want to save images the function create folders
               and file  with names.
    shape_available : bool, wether shape file for clipping available or not. True if Yes False if no.
    path_to_shape : Path to the .shp file if it is available or path to save the created shape if it is not.
    
    """
    folderNm = pathlib.PurePath(path_input).name[:40]
    fileNm = pathlib.PurePath(path_input).name
    
    #print(path_to_shape)

    W_im = gdal.Open(path_input)
    rasterBand = W_im.GetRasterBand(1)
    elevArray = W_im.GetRasterBand(1).ReadAsArray().astype(np.float32)
    
    projection = osr.SpatialReference(wkt=W_im.GetProjection())
    #
    if shape_available == True:
        options = gdal.WarpOptions(cutlineDSName=path_to_shape,format="GTiff",cropToCutline=True,dstNodata=np.nan)
        outBand = gdal.Warp(srcDSOrSrcDSTab=path_input,
                            destNameOrDestDS=outPath+'/'+folderNm+'/Clipped_'+fileNm,
                            options=options)
        outBand= None
        
        print('saved at :',outPath+'/'+folderNm+'/Clipped_'+fileNm)
            
    else:
        shape_save_path = path_to_shape
        path_to_shape=Create_boundBox(shape_save_path,projection)
        
        
        options = gdal.WarpOptions(cutlineDSName=path_to_shape,format="GTiff",cropToCutline=True,dstNodata=np.nan)
        outBand = gdal.Warp(srcDSOrSrcDSTab=path_input,
                            destNameOrDestDS=outPath+'/'+folderNm+'/Clipped_'+fileNm,
                            options=options)
        
        print('saved at :',outPath+'/'+folderNm+'/Clipped_'+fileNm)
        shape_available = True
        
    return path_to_shape ,shape_available


def Clip_to_bound(In_path,output_path,shp_path):
    
    folderNm = pathlib.PurePath(In_path).name[:40]
    fileNm = pathlib.PurePath(In_path).name
    
    options = gdal.WarpOptions(cutlineDSName=shp_path,format="GTiff",cropToCutline=True,dstNodata=np.nan)
    outBand = gdal.Warp(srcDSOrSrcDSTab=In_path,
                        destNameOrDestDS=output_path+'/'+folderNm+'/Clipped_'+fileNm,
                        options=options)
    outBand= None
    
    print('saved at :',output_path+'/'+folderNm+'/Clipped_'+fileNm)


def Clip_to_bound1(In_path,output_path,shp_path):
    
    #folderNm = pathlib.PurePath(path_input).name[:40]
    #fileNm = pathlib.PurePath(path_input).name
    
    options = gdal.WarpOptions(cutlineDSName=shp_path,format="GTiff",cropToCutline=True,dstNodata=np.nan)
    outBand = gdal.Warp(srcDSOrSrcDSTab=In_path,
                        destNameOrDestDS=output_path,
                        options=options)
    outBand= None
        
        
        
