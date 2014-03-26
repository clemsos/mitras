# Create a map of Chinese province with d3js

Based on Mike Bostock's d3js [map tutorial](http://bost.ocks.org/mike/map/) and [this other tutorial](http://www.tnoda.com/blog/2013-12-07)

## Prepare map data

To map data for Sina Weibo, we need to combine several maps to include HK, Aomen and Taiwan. 

Map data map need to be downloaded from [Natural Earth](www.naturalearthdata.com) 1:10m Cultural Vectors 

* Admin 0 - Countries (including taiwan and HK)  [Download](http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries_lakes.zip)
* Admin 1 - States, Provinces (only the mainland) [Download](http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces_lakes.zip)

Then, we use command-line tool ```ogr2ogr``` to filter SHP and keep only relevant part of the map and convert to geojson.

For the countries, we use ISO 3166-1 alpha-3 standard names of the countries : 'CHN', 'HKG', 'TWN' and 'MAC'
 
    ogr2ogr -f GeoJSON -where "ADM0_A3 IN ('CHN', 'HKG', 'TWN', 'MAC')" zh-countries.geo.json ne_10m_admin_0_countries_lakes.shp

For the provinces, we need only the mainland.
    
    ogr2ogr -f GeoJSON -where "gu_A3 IN ('CHN')" zh-mainland-provinces.json ne_10m_admin_1_states_provinces_lakes.shp 

The we use mapshaper.org to simplify the geometry (make the file smaller) and download it as topojson. Final states of the files are available in this rep. 

TODO : Make the maps files smaller using npm topojson and removing useless fields

## Add info data

Now that we have our maps ready we can add data from a JS array and pass it to d3js to draw a colored map. Data should be an array where Chinese provinces are defined by their English official name (see topojson). Others are  "Taiwan", "HK" and "Macau". 

The array should look like this:

    var data=[["Xianggang",53],["Guangdong",24],["Beijing",10],["Shanghai",6],["Taiwan",6],["Qita",5],["Hunan",2],["Yunnan",2],["Zhejiang",2],["Haiwai",2],["Shaanxi",2],["Jiangsu",1],["Anhui",1],["Guangxi",1],["Tianjin",1],["Henan",1],["Liaoning",1],["Fujian",1]];



## Other useful links

* http://bl.ocks.org/mbostock/4707858
* http://technicaltidbit.blogspot.fr/2013/07/choropleth-in-d3js-and-pandas-ipython.html
* http://ccarpenterg.github.io/blog/us-census-visualization-with-d3js/