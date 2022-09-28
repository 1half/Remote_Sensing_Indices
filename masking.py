import numpy as np
#import matplotlib.pyplot as plt
from osgeo import gdal,ogr,osr
import glob,os,pathlib
import geopandas as gpd
from shapely.geometry import Polygon, mapping,LineString,Point

def get_contour(path_input,contourPath):
    
    """
    path_input : Input path to raster.
    
    contourPath : path+name.shp to save
    """
    #folderNm = pathlib.PurePath(path_input).name[:40]
    fileNm = pathlib.PurePath(path_input).name[:-4]
    
    W_im = gdal.Open(path_input)
    rasterBand = W_im.GetRasterBand(1)
    elevArray = W_im.GetRasterBand(1).ReadAsArray().astype(np.float32)
    
    proj = osr.SpatialReference(wkt=W_im.GetProjection())
    
    demNan = -99999
    
    #get dem max and min
    demMax = elevArray.max()
    demMin = elevArray[elevArray!=demNan].min()
    print("Maximun dem elevation: %.2f, minimum dem elevation: %.2f"%(demMax,demMin))
          
          
    contourDs = ogr.GetDriverByName("ESRI Shapefile").CreateDataSource(contourPath+'/Contour_'+fileNm+'.shp')
    #define layer name and spatial
    contourShp = contourDs.CreateLayer('contour', proj)
    #define fields of id and elev
    fieldDef = ogr.FieldDefn("ID", ogr.OFTInteger)
    contourShp.CreateField(fieldDef)
    fieldDef = ogr.FieldDefn("elev", ogr.OFTReal)
    contourShp.CreateField(fieldDef)
                  
    gdal.ContourGenerate(rasterBand, 50.0, 1250.0, [], 1, -32768., 
                         contourShp, 0, 1)
    contourDs.Destroy()



def cut_line_at_points(line, points):
    

    # First coords of line
    coords = list(line.coords)

    # Keep list coords where to cut (cuts = 1)
    cuts = [0] * len(coords)
    cuts[0] = 1
    cuts[-1] = 1

    # Add the coords from the points
    coords += [list(p.coords)[0] for p in points]    
    cuts += [1] * len(points)        

    # Calculate the distance along the line for each point    
    dists = [line.project(Point(p)) for p in coords]    

    # sort the coords/cuts based on the distances    
    # see http://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list    
    coords = [p for (d, p) in sorted(zip(dists, coords))]    
    cuts = [p for (d, p) in sorted(zip(dists, cuts))]          

    # generate the Lines    
    #lines = [LineString([coords[i], coords[i+1]]) for i in range(len(coords)-1)]    
    lines = []        

    for i in range(len(coords)-1):    
        if cuts[i] == 1:    
            # find next element in cuts == 1 starting from index i + 1   
            j = cuts.index(1, i + 1)    
            lines.append(LineString(coords[i:j+1]))            

    return lines


def Get_mask(shape_line,mask_OutPath):
    
    new_line = LineString([Point(143693,1321428),Point(144030,1322160),Point(144108.3,1322621.4),Point(144215.6,1323074.2)])

    IntersectionLines=gpd.GeoSeries([new_line])
    
    fileNm = pathlib.PurePath(shape_line).name
    
    cn_line = gpd.read_file(shape_line)
    cn_line['length'] = cn_line.length
    crs1 =cn_line.crs
    LargL = cn_line.loc[cn_line['length']==cn_line['length'].max()]#Get the largest line here it should be line along water edge.
    
    #to shapely.geometry.linestring.LineString
    Linr = LargL.geometry.unary_union
    
    IntPoints=Linr.intersection(IntersectionLines.unary_union)
    
    SplitSegments = cut_line_at_points(Linr,IntPoints)
    
    cut_df = gpd.GeoDataFrame(
        {'ID': [1000,1001,1003],
         'elev': [0,0,0], 'geometry': [SplitSegments[0],SplitSegments[1],
                                       SplitSegments[2]]},crs=crs1)
    cut_df ['length'] = cut_df.length
    cut_df = cut_df.loc[cut_df['length']==cut_df['length'].max()]
    
    cut_df['geometry'] = [Polygon(mapping(x)['coordinates']) for x in cut_df.geometry]
    
    
    cut_df.to_file(mask_OutPath+'/Mask_'+fileNm,driver = "ESRI Shapefile")




