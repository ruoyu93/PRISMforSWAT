# PRISMforSWAT
A set of functions for using PRISM (http://prism.oregonstate.edu) dataset to prepare weather input data for SWAT model (Arnold et al., 1998).

If users ONLY want to download PRISM data (either monthly or daily), please use the function "PRISMdownload" and follow the intructions in the .py file

If users want to prepare the data, "generate_SWATweather" will automatically download the PRISM daily precipitation (ppt), maximum and minimum temperature (tmax and tmin) and create the weather tables.

For details, check the introductions in the .py file under each function.

# Reference

Arnold, Jeffrey G., et al. "Large area hydrologic modeling and assessment part I: model development 1." JAWRA Journal of the American Water Resources Association 34.1 (1998): 73-89.
