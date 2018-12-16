#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 21:02:25 2018

@author: Ruoyu Zhang (University of Virginia)
"""

# From PRISM ftp server to download cliamte data
# Email, timeinterval (monthly or daily), variables (can be multiple in a list),
#    and start/end year are required statements of the function. Users can enter
#    the path to save files, otherwise the path where the path of script will be 
#    used to save files. 
# A folder called PRISM will be created under the path, inside the PRISM folder,
#    montly and daily folder will also be created if you download both type data,
#    folders named by variables will also be created to save PRISM data. [make a structure picture]
# Since the data of prism is in zip format and we need to unzip to get the raster
#    for climate data, users can turn on the unzip = True to automatically unzip
#    all downloaded files. If they don't want to keep the zip files, turn keepzip to False
#    so the zip files will be deleted. 

def PRISMdownload(email, timeinterval, variables, startyear, endyear, \
                  savedir=None, unzip=False, keepzip=True):
    '''
    Function PRISMdownload can download the monthly or daily PRISM cliamte data for a user defined
        period (in years ONLY). Since the data are provided in zip format, the function is also built 
        with capability to unzip downloaded files and delete the zip files.
    A folder called PRISM will be created under the "savedir" path. Inside the PRISM folder,
        montly and daily folder will also be created if you download both type data,
        folders named by variables will also be created to save PRISM data.
        Example: {savedir}/PRISM/daily (or monthly)/ppt (or other variables)/(list of data)
    The function handles if user download duplicated data. If the zip file or unzipped file of a date is 
        existing, the function will skip this date and the data will not be downloaded since it is already
        exist. 
    
    *** 1. For SWAT model weather data, we recommend to download daily data.
    
    Parameters:
        email: an email address which is required to login to PRISM ftp server
        timeinterval: can be "d" or "m" (for daily or monthly data). Can only select one as the input
        variables: a list of variables (ppt: precipitation, tmax: max temperature, tmin: min temperature, and etc.)
        startyear: the beginning year of data to download
        endyear: the end year of data to download (end year is included)
        savedir: the place to save the PRISM data
        unzip: Whether to extract the zip files. 
               True will unzip the downloaded zip files, False will keep the zip files (save disk space)
        keepzip: Whether to keep the zip files. Don't turn this off if unzip is set to False, or you will delete 
               downloaded zip files, meaning no data will be saved.
        
    '''
    def folderexist(folder):
        if not os.path.exists(os.getcwd()+"/"+folder):
            os.makedirs(folder)
    import ftplib as fl
    import zipfile, os
    
    if unzip is False: print "Your download data are in zip file" 
    else: print "Your download data will be unzipped"
    if keepzip is True: print "Your data in zip files are kept"
    else: print "Your data in zip format will be deleted"
    if (unzip is False and keepzip is False): 
        print "No data will be saved.\nOperation is terminated."
    if savedir is None:
        savedir = os.getcwd()
        print "Saving data to", savedir
    os.chdir(savedir)
    folderexist("PRISM")                 # create PRISM folder to store data
    ftp = fl.FTP('prism.nacse.org')   # connect to PRISM FTP serve
    ftp.login(passwd=email)
    
    if timeinterval in ['m','M']:     # if we are downloading monthly data
        ftp.cwd("monthly")
        os.chdir(savedir + "/PRISM")
        folderexist("monthly") 
        os.chdir(savedir + "/PRISM/monthly")
        
        for vari in variables:
            folderexist(vari)
            os.chdir(savedir + "/PRISM/monthly/" + vari)
            ftp.cwd(vari.lower())
            fnbase = "PRISM_"+ vari +"_stable_4kmM"
            fnmid = '2_'   #year before 1981
            fnend = '_all_bil.zip'             
                                            # monthly data min year 1895
            for year in range(int(startyear), int(endyear)+1):
                if year > 1980 and vari == 'ppt':
                    fnmid = '3_'
                ftp.cwd(str(year))
                fn = fnbase + fnmid + str(year) + fnend
                if os.path.exists(os.getcwd()+"/"+fn[:-3]+"bil"):
                    continue                    # avoid to download duplicated data
                elif (os.path.exists(os.getcwd()+"/"+fn) and unzip is True):
                    zfile = zipfile.ZipFile(fn)
                    zfile.extractall()
                    zfile.close()
                else:    
                    file = open(fn, 'wb')  # wb: write binary
                    ftp.retrbinary("RETR " + fn, file.write)
                    file.close()
                    if unzip is True:
                        zfile = zipfile.ZipFile(fn)
                        zfile.extractall()
                        zfile.close()
                    if keepzip is False:
                        os.remove(fn)
                ftp.cwd('../')
                print str(year), "monthly", vari, "DONE"
            ftp.cwd("../")
            os.chdir("../")
                
    elif timeinterval in ['d','D']:   # if we are downloading daily data PRISM_ppt_stable_4kmD2_19810101_bil.zip
        ftp.cwd("daily")
        os.chdir(savedir + "/PRISM")
        folderexist("daily")
        os.chdir(savedir + "/PRISM/daily")
        for vari in variables:
            folderexist(vari)
            os.chdir(savedir + "/PRISM/daily/" + vari)
            ftp.cwd(vari.lower())
            
            for year in range(int(startyear), int(endyear)+1):
                ftp.cwd(str(year))
                filenames = ftp.nlst()
                for fn in filenames:
                    if os.path.exists(os.getcwd()+"/"+fn[:-3]+"bil"):
                        continue
                    elif os.path.exists(os.getcwd()+"/"+fn):
                        if unzip is True:
                            print fn
                            zfile = zipfile.ZipFile(fn)
                            zfile.extractall()
                            zfile.close()
                        if keepzip is False:
                            os.remove(fn) 
                    else:
                        file = open(fn, 'wb')
                        ftp.retrbinary("RETR " + fn, file.write)
                        file.close()
                        if unzip is True:
                            zfile = zipfile.ZipFile(fn)
                            zfile.extractall()
                            zfile.close()
                            if keepzip is False:
                                os.remove(fn) 
                print str(year), "daily", vari, "DONE"
                ftp.cwd("../")
            os.chdir("../")
            ftp.cwd("../")
            
    ftp.quit()
# if you want to test you can comment lines below
#PRISMdownload('xxx@gmail.com','d',['ppt','tmax','tmin'], 2002,2003, savedir= ???, unzip=True)

# Using Google map elevation API to get the elevation data for SWAT
def get_elevation(lat, lng, Google_API=None):
    '''
    Function get_elevation currently uses Google Map Elevation API to get the elevation at a coordinate.
    Users are recommended to have one account/key from Google Earth Engine and activate the elevation API. 
    
    *** 1. We highly recommend users to get their own API from Google Earth Engine,
        as author's key is provided but can be invalid in the future.  
    
    Parameters:
        lat: latitude of the point
        lng: longitude of the point
        Google_API: the key of Google Earth Engine with Elevation API activated!!
    '''
    if abs(lat) > 90 or abs(lng) > 180:
        print "Your point is out of bounce[-90 < Lat < 90; -180 < Lng < 180]."

    import urllib2, json
    ## build the url for the API call
    ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'
    URL_PARAMS = "locations=%.7f,%.7f&key=%s" % (lat, lng, "AIzaSyC61eXnJkcWHqCab4r0VzFfDTldR1dYYZU" if Google_API is None else Google_API)
    url = ELEVATION_BASE_URL + "?" + URL_PARAMS

    f = urllib2.urlopen(url)
    response = json.load(f)
    #print response
    if response['status'] == 'OK':
        result = response["results"][0]
        elevation = float(result["elevation"])
    else:
        elevation = None
        print "Elevation is NONE,\nPlease get a key for Google Earth Engine and activate Elevation API or correct your coordinate input."
    return(round(elevation,3))

def dayofyears(yearstart, yearend):
    '''
    Function dayofyears give the total days within a year period.
    '''
    total = 0
    for year in range(yearstart, yearend+1):
        if year % 4 == 0:
            total += 366
        else:
            total += 365
    return total

def generate_SWATweather(WatershedPath, PRISMfolderPath, OutputFolder, yearstart, yearend, Google_API=None, shapeout=True):
    '''
    Function “generate_SWATweather” can create daily time series of precipitation and temperature (max and min)
        from PRISM pixels within the watershed. The center point of each pixel will be treated as a weather station
        for SWAT model. 
        
        *** 1. This function is not capable to check the continous of time series. Users are recommended to use PRISMdownload
            function to download PRISM data, in which the continuity is guaranteed.  
        *** 2. If zip files exist, the function will unzip these files; if no zip or unzipped files are found, the function
            will quit, and you need to use PRISMdownload to download the data for your study period.
        
    Parameters:
        WatershedPath: the path of the watershed shapefile;
        PRISMfolderPath: the PRISM parent folder created by PRISMdownload function or following such structure:
                         "./PRISM/daily/ppt or tmin or tmax";
        OutputFolder: the path of folder storing tables in format that SWAT requires;
        yearstart: the beginning year of the timeseries;
        yearend: the end year of the time series;
        Google_API: The key of API for Google Map Elevation API. Users are recommended to get one from Google for free,
                    or the function will use author's API to download (can be disabled anytime). 
    '''
    import os
    import rasterio
    from rasterio.mask import mask
    import geopandas as gpd
    from rasterio import Affine
    import numpy as np
    import zipfile
    
    Google_API = "AIzaSyC61eXnJkcWHqCab4r0VzFfDTldR1dYYZU" if Google_API is None else Google_API
    pptpath = PRISMfolderPath + "/daily/ppt"
    tmaxpath = PRISMfolderPath + "/daily/tmax"
    tminpath = PRISMfolderPath + "/daily/tmin"
    path_list = [pptpath, tmaxpath, tminpath]
    
    tables_ls = []
    os.chdir(OutputFolder)#save files in the output folder
    for vari_path in path_list:
        file_rasters = [f for f in os.listdir(vari_path) if (f.endswith('.bil') and any(str(x) in f for x in range(yearstart, yearend+1)))]
        if len(file_rasters) < dayofyears(yearstart, yearend):
            ziptest = [f for f in os.listdir(vari_path) if (f.endswith('.zip') and any(str(x) in f for x in range(yearstart, yearend+1)))]
            print len(ziptest)
            if len(ziptest) > 0:
                for fn in ziptest:
                    if os.path.exists(vari_path + '/' + fn[:-3]+ "bil"):
                        continue
                    else:
                        fn = vari_path + "/" + fn
                        print fn
                        zfile = zipfile.ZipFile(fn)
                        zfile.extractall(vari_path)
                        print "DONE"
                        zfile.close()
                file_rasters = [f for f in os.listdir(vari_path) if f.endswith('.bil')]
                print len(file_rasters)
            if len(file_rasters) < dayofyears(yearstart,yearend):
                print "Missing some dates' PRISM data."
                indi = raw_input("\nWant to download missing data? (Y/N)")
                if indi == "Y":
                    email = raw_input("Enter an email address to download missing PRISM data.")
                    PRISMdownload(email, 'd', [vari_path[vari_path.rfind("/")+1:]], yearstart , yearend, \
                            savedir=PRISMfolderPath[:PRISMfolderPath.rfind("/")], unzip=True, keepzip=True)
                    file_rasters = [f for f in os.listdir(vari_path) if (f.endswith('.bil') and any(str(x) in f for x in range(yearstart, yearend+1)))]
                #if vari_path[vari_path.rfind('/')+1:]=='ppt':
                #    raster_year = list(set([int(year[23:27]) for year in file_rasters]))
                #else:
                #    raster_year = list(set([int(year[24:28]) for year in file_rasters]))
                #if raster_year != range(yearstart, yearend+1):
                #    missyear = [i for i in range(yearstart,yearend+1) if i not in raster_year]
                #    print "Found gap years", missyear,
                #    indi = input("\nWant to download missing data? (Y/N)")
                #    if indi == "Y":
                #        email = raw_input("Enter an email address to download missing PRISM data.")
                #        PRISMdownload(email, 'd', vari_path[vari_path.rfind("/")+1:], yearstart , yearend, \
                #            savedir=PRISMfolderPath[:PRISMfolderPath.rfind("/")], unzip=True, keepzip=True)
                else:
                    return
        file_rasters.sort()  # make sure the data list is organized in order of date
        os.chdir(OutputFolder)
        
        shapefile = gpd.read_file(WatershedPath)
        shapefile1 = shapefile.to_crs({'init': 'epsg:4269'})   # reproject the shapefile as same as PRISM data's
        geoms = shapefile1.geometry.values
        #geometry = geoms[0]  # to check the geometry of watershed
            
        from shapely.geometry import mapping #, Point
        geoms = [mapping(geoms[0])]
        
        for ind, raster in enumerate(file_rasters):
            full_path = vari_path + '/'+ raster

            date = raster[-16:-8]
            with rasterio.open(full_path) as src:
                out_image, out_transform = mask(src, geoms, crop=True)
            
            no_data = src.nodata
            data = out_image.data[0]
            variable = np. extract(data != no_data, data)
            
            T1 = out_transform * Affine.translation(0.5, 0.5)  # reference the pixel center
            rc2xy = lambda r, c:(c,r) * T1
            
            if ind == 0:
                row, col = np.where(data != no_data)
                d = gpd.GeoDataFrame({'col':col, 'row':row})
                d['x'] = d.apply(lambda row: rc2xy(row.row, row.col)[0], axis=1)
                d['y'] = d.apply(lambda row: rc2xy(row.row, row.col)[1], axis=1)
                if shapeout is True:
                    from shapely.geometry import Point
                    d['geometry'] = d.apply(lambda row: Point(row['x'], row['y']), axis=1)
                    d.crs = {'init': 'epsg:4326'}
                    d.to_file(driver = 'ESRI Shapefile', filename = "weatherstations.shp")
                d[date] = variable
            else:
                d[date] = variable
        tables_ls.append(d)
        
        
    table_tot = open("tmp.txt","w")
    line = ','.join(['id', 'name', 'lat', 'long', 'elevation'])
    table_tot.write(line+"\n")
    for i in range(tables_ls[1].count()[0]):  # number of rows
        a = tables_ls[1].loc[[i]]   # get each row for tmax and tmin
        b = tables_ls[2].loc[[i]]
        line1 = ",".join([str(i), "t"+str(i), str(round(a['y'],5)), str(round(a['x'],5)), str(get_elevation(round(a['y'],7), round(a['x'],7)))])
        table_tot.write(line1+"\n")
        table_station = open("t"+str(i)+".txt", "w")
        table_station.write(str(a.columns[5])+"\n")
        for x in a:
            if x.isdigit():
                table_station.write(str(round(a[x],3))+","+str(round(b[x],3))+"\n")
        table_station.close()
    table_tot.close()
    
    table_tot = open("pcp.txt","w")
    line = ','.join(['id', 'name', 'lat', 'long', 'elevation'])
    table_tot.write(line+"\n")
    for i in range(tables_ls[0].count()[0]):  # number of rows
        a = tables_ls[0].loc[[i]]   # get each row for ppt
        line1 = ",".join([str(i), "p"+str(i), str(round(a['y'],5)), str(round(a['x'],5)), str(get_elevation(round(a['y'],7), round(a['x'],7)))])
        table_tot.write(line1+"\n")
        table_station = open("p"+str(i)+".txt", "w")
        table_station.write(str(a.columns[5])+"\n")
        for x in a:
            if x.isdigit():
                table_station.write(str(round(a[x],3))+"\n")
        table_station.close()
    table_tot.close()
    return tables_ls

#a = generate_SWATweather(WatershedPath, PRISMfolderPath, OutputFolder, 2002, 2003)
#a is the list containing three tables for data of ppt[0], tmax[1], and tmin[2]

    
