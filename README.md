

This code is not effective anymore as the PEPS server has been replaced by the [Geodes](https://geodes.cnes.fr/) server. GEODES now distributes all the Earth Observation produced by CNES, and it hosts the Copernicus Collaborative ground segment, that distributes Sentinel-1 and Sentinel-2 products.

GEODES uses [the STAC API](https://geodes.cnes.fr/support/api/) but also provides a [Python API mamed PyGeodes](https://cnes.github.io/pyGeodes/index.html), already functional but still in development (as of february 2025). 

![Geodes logo](https://wpedu2.sedoo.fr/wp-content-omp/uploads/sites/50/2024/08/Logo_GEODES-bleu-fond-transparent-2048x427.png)







# peps_download

This is a simple piece of code to automatically download the products provided by the French Sentinel collaborative ground segment named PEPS : https://peps.cnes.fr. PEPS is mirroring all the Sentinel data provided by ESA, and is providing a simplified access.

This code was written thanks to the precious help of one my colleagues at CNES [Jérôme Gasperi](https://www.linkedin.com/pulse/rocket-earth-your-pocket-gasperi-jerome) who developped the "rocket" interface which is used by Peps.

This code relies on python (2 or 3) and on the curl utility. I am not sure it can work on windows.

Only the recent PEPS products or the frequently accessed ones are stored on disks (2 PB), while the rest is stored on tapes (up to 14 PB). Data stored on tapes have an access time increased by 2 to 6 mn. **From the 23rd of March, peps_download has been fully reshaped to first stage products on tapes for download, then download products on disk, which gives some time to upload the tape products on disks. This procedures considerably speeds the downloads up.**

#Alternatives
There are now more professsional alternatives, such as EODAG from the company CS-SI, that can download data from various catalogues. PEPS is included in the list.
https://github.com/CS-SI/eodag
 

## Examples

### for Sentinel-2
This software is still quite basic, but if you have an account at PEPS, you may download products using command lines like 


- `python ./peps_download.py  -c S2ST -l 'Toulouse' -a peps.txt -d 2017-01-01 -f 2017-02-01`
- `python ./peps_download.py  -c S2ST -t 31TCJ -a peps.txt -d 2017-01-01 -f 2017-02-01`

 which downloads the *Sentinel-2 single tile* products  acquired in January 2017 above Toulouse (you may also specify the tile number as in the second example).
 When you provide a date YY-MM-DD, it is actually YY-MM-DD:00;00:00. So a request with `-d 2015-11-01 -f 2015-11-01` will yield no result, while `-d 2015-11-01 -f 2015-11-02` will yield data acquired on 2015-11-01 (provided they exist).
 
 - `python ./peps_download.py  -c S2ST --lon 1 --lat 43.5 -a peps.txt -d 2015-11-01 -f 2015-12-01 -o 51` 

 which downloads the Sentinel-2 products above --lon 1 --lat 43.5 (~Toulouse), acquired in November 2015 from orbit path number 51 only.
### for Sentinel-1
- `python ./peps_download.py  -c S1 --lonmin 1 --lonmax 2 --latmin 43 --latmax 44 -a peps.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the Sentinel-1 products in latitude, longitude box around Toulouse, acquired in November 2015.

- `python ./peps_download.py -c S1 -p GRD -l 'Toulouse' -a peps.txt -d 2015-11-01 -f 2015-12-01`
which downloads S1 GRD products above Toulouse

## Authentification 

The file peps.txt must contain your email address and your password on the same line, such as:

`your.email@address.fr top_secret`

To get an account : https://peps.cnes.fr/rocket/#/register

## Alternatives

The EODAG tool has an interface to download data from Theia, PEPS, and many others, and it is probably much more professional code. You might give it a try.

https://eodag.readthedocs.io/en/latest/#

https://github.com/CS-SI/eodag
