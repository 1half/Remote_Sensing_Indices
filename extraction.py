import glob
import pathlib
import os
import tarfile


def choose_files():
    checkL=['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','ANG','QA_PIXEL','QA_RADSAT','QA_AEROSOL','ATRAN',
        'CDIST','DRAD','EMIS','EMSD','QA','TRAD','URAD','MTL']
    bnds = []
    c = True
    while c:
        a = input('Give band or file name(b1,b2,b3,MTL, ..etc) type "ok" when done:').upper()
        if a in checkL:
            bnds.append(a)
        elif a == 'OK': 
            c= False
        else:
            print('invalid input')
    
    return bnds


def match_choise(bnds,tarFile):
    match =[]
    for b in bnds:
        m = [s for s in tarFile if (b+'.TIF') in s] + [s for s in tarFile if (b+'.txt') in s]
        match.extend(m)
            
    return match

def extract_tar(path_tar,out_path,extract_all=True):
    
    """
    path_tar : give path to the folder where .tar files are 
    
    out_path : where to extract the files
    
    extract_all : True or False, wether to extract all the files or not.if False specify files.
    
    """
    
    path_tarfolder = glob.glob(path_tar+'/*.tar')
    #pathlib.PurePath(List_of_im[0]).name[:-4]
    
    if extract_all is True:
        for tfile in path_tarfolder:
                            
            fname = pathlib.PurePath(tfile).name[:-4] #get name of file
            os.mkdir(out_path+'/'+fname)  #make folder with name of tar file
            
            my_tar = tarfile.open(tfile)            
            my_tar.extractall(out_path+'/'+fname) # specify which folder to extract to
            my_tar.close()
    else:
        choise_ = choose_files()# gives key for chosen bands
        print(choise_)
        for tfile in path_tarfolder:
            
            fname = pathlib.PurePath(tfile).name[:-4] #get name of file
            os.mkdir(out_path+'/'+fname)  #make folder with name of tar file
            print(tfile)
            print(out_path+'/'+fname)
            my_tar = tarfile.open(tfile)
            files_in_tar = my_tar.getnames()
            #my_tar.close()
            #choise_ = choose_files(files_in_tar)  # gives list of chosen bands
            matchs = match_choise(choise_,files_in_tar)# gives list of chosen bands
            print(matchs)
            for file in matchs:
                #my_tar = tarfile.open(tfile)
                my_tar.extract(file,out_path+'/'+fname)
            my_tar.close()


def ListBands_n_MTL(lsat_im_path):
    
    Bands = {'BAND1':[],'BAND2':[],'BAND3':[],'BAND4':[],'BAND5':[],'BAND6':[],
         'BAND7':[],'BAND8':[],'BAND9':[],'BAND10':[],'BAND10':[],'BAND11':[],'BAND12':[]}

    MTL_dict = {}

    List_of_im = glob.glob(lsat_im_path+"/L*/")
    
    for path in List_of_im:
        
        lst_title = pathlib.PurePath(path).name[:25]
        MTL_dict[lst_title] = glob.glob(f"{path}*MTL.txt")
                
        for n in range(1,13):
            Band_no = f'BAND{n}'
            band_path = glob.glob(f"{path}*B{n}.tif")
            Bands[Band_no].extend(band_path)
            
    return Bands,MTL_dict



