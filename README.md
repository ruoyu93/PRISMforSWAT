# PRISMforSWAT
A set of functions for using PRISM (http://prism.oregonstate.edu) dataset to prepare weather input data for SWAT model (Arnold et al., 1998) built via. Python 2.7.

If users ONLY want to download PRISM data (either monthly or daily), please use the function "PRISMdownload" and follow the intructions in the .py file

If users want to prepare the data, "generate_SWATweather" will automatically download the PRISM daily precipitation (ppt), maximum and minimum temperature (tmax and tmin) and create the weather tables.

For details, check the introductions in the .py file under each function.

# Examples
Use of “PRISMdownload”:

PRISMdownload(email = xxx@gmail.com, timeinterval = “d”, variables = [‘ppt’, ‘tmax’, ‘tmin’], 2000, 2005, savedir = “C:/Downloads”, unzip = False, keepzip = True)

1. The timeinterval can only be ‘d” for daily or ‘m’ for monthly data. 
2. Savedir, unzip, and keepzip are optional. Savedir is the saving directory and highly recommended to customized by users, or the script will download data and create folder structure (figure 1) in current working directory. Unzip and keepzip are False and True by default, but unzip is highly recommended to be set as True to extract download zip files of PRISM data.
3. This function will download zip files of precipitation (ppt), maximum and minimum temperature (tmax and tmin) for the contiguous US from 2000 to 2005 to the path C:/Downloads.



Use of “generate_SWATweather”

generate_SWATweather(WatershedPath = “C:/SWAT/watershed.shp", PRISMfolderPath = “C:/Downloads/PRISM”, OutputFolder = “C:/SWAT/PRISMdata”, 2000, 2005)

1. Developer's Google Earth Engine API is used, and is likely to be disabled. Recommend users to have an account from Google and activate Elevation API.
2. A shapefile of watershed is required (path of file passed to WatershedPath).
3. PRISM folder has to be the main folder with the structure in figure 1. 
4. The weather tables will be saved at path “C:/SWAT/PRISMdata” from 2000 to 2005. 


# Reference

Arnold, Jeffrey G., et al. "Large area hydrologic modeling and assessment part I: model development 1." JAWRA Journal of the American Water Resources Association 34.1 (1998): 73-89.
