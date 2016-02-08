# peps_download

This is a simple piece of code to automatically download the products provided by the French Sentinel collaborative ground segment named PEPS : https://peps.cnes.fr. PEPS is mirroring all the Sentinel data provided by ESA, and is providing a simplified access.

This code was written thanks to the precious help of one my colleagues at CNES [Jérôme Gasperi](https://www.linkedin.com/pulse/rocket-earth-your-pocket-gasperi-jerome) who developped the "rocket" interface which is used by Peps.

This code relies on python 2.7 and on the curl utility. Because of that, I guess it only works with linux.

## Examples
This software is still quite basic, but if you have an account at PEPS, you may download products using command lines like 

- `python ./peps_download.py  -c S2 -l 'Toulouse' -a peps.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the Sentinel-2 products above Toulouse, acquired in November 2015.

- `python ./peps_download.py  -c S2 --lon 1 --lat 43.5 -a peps.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the Sentinel-2 products above --lon 1 --lat 43.5 (~Toulouse), acquired in November 2015.
 
 - `python ./peps_download.py  -c S2 --lon 1 --lat 43.5 -a peps.txt -d 2015-11-01 -f 2015-12-01 -o 51` 

 which downloads the Sentinel-2 products above --lon 1 --lat 43.5 (~Toulouse), acquired in November 2015 from orbit path number 51 only.

- `python ./peps_download.py  -c S1 --lonmin 1 --lonmax 2 --latmin 43 --latmax 44 -a peps.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the Sentinel-1 products in latitude, longitude box around Toulouse, acquired in November 2015.



##Authentification 

The file peps.txt must contain your email address and your password on the same line, such as follows :
`your.email@address.fr top_secret`

To get an account : https://peps.cnes.fr/rocket/#/register


