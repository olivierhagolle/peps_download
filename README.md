# theia_download

This is a simple piece of code to automatically download the products provided by Theia land data center : https://theia.cnes.fr. It can download the products delivered by Theia, such as the [Landsat L2A products](http://www.cesbio.ups-tlse.fr/multitemp/?page_id=3487) and the [SpotWorldHeritage L1C products](https://www.theia-land.fr/en/projects/spot-world-heritage).

This code was written thanks to the precious help of one my colleague at CNES [Jérôme Gasperi](https://www.linkedin.com/pulse/rocket-earth-your-pocket-gasperi-jerome) who developped the "rocket" interface which is used by Theia, and the mechanism to get a token.

This code relies on python 2.7 and on the curl utility. Because of that, I guess it only works with linux.

## Examples
This software is still quite basic, but if you have an account at theia, you may download products using command lines like 

- `python ./theia_download.py -l 'Toulouse' -a auth_theia.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the LANDSAT 8 products above Toulouse, acquired in November 2015.

- `python ./theia_download.py --lon 1 --lat 43.5 -a auth_theia.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the LANDSAT 8 products above --lon 1 --lat 43.5 (~Toulouse), acquired in November 2015.

- `python ./theia_download.py --lonmin 1 --lonmax 2 --latmin 43 --latmax 44 -a auth_theia.txt -d 2015-11-01 -f 2015-12-01`

 which downloads the LANDSAT 8 products in latitude, longitude box around Toulouse, acquired in November 2015.


- `python theia_download.py -l 'Toulouse' -a auth_theia.txt -c SpotWorldHeritage -p SPOT4 -d 2005-11-01 -f 2006-12-01`
 which downloads the SpotWorldHeritage products acquired by SPOT5 in 2005-2006

##Authentification 

The file auth_theia.txt must contain your email address and your password on the same line, such as follows :
`your.email@address.fr top_secret`

The program first fetches a token using your email address and password, and then uses it to download the products. As the token is only valid for two hours, itis advised to request only a reasonable number of products. 

