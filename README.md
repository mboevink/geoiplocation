# Python GeoLocation

Recreated the following project: http://chir.ag/projects/geoiploc/ for python with the addition of live updates to the source material.
To start, download the geolocation database provided here: http://software77.net/geo-ip/history/ (Up-to-date files are provided as donationware.)

```
from geoiplocation import get_country

#  IP address, Full name or country code, csv file
print(get_country('8.8.8.8', False, '/path/to/my/database.csv'))
```

A cache is provided for batch processing.

