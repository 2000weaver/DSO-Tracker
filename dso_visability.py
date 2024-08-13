from astropy.time import Time
from astropy.coordinates import EarthLocation
from astroplan import Observer
import astropy.units as u
import pytz
from datetime import timedelta

class ObsParams:
    def __init__(self, lat, long, height, utcOffset, daylightSavings):
        """
        Initialize the ObsParams class with the given parameters
        
        Parameters:
         - lat: Latitude in degrees (float)
         - long: Longitude in degrees (float)
         - height: Elevation in meters (float)
         - utcOffset: UTC offset in hours (int)
         - daylightSavings: Boolean indicating if daylight savings time is observed (boolean)"""

        self.lat = lat * u.deg
        self.long = long * u.deg
        self.height = height * u.m 
        self.utcOffset = utcOffset
        self.daylightSavings = daylightSavings

        def __repr__(self):
            return (f"ObsParams(lat={self.lat}, long={self.long}, height={self.height}, "f"utcOffset={self.utcOffset}, daylightSavings={self.daylightSavings})")
    
    def get_timezone_offset(self):
        """
        Calculate the timezone offset considering daylight savings.
        
        Returns:
        - The timezone offset in hours (float)
        """
        offset = self.utcOffset
        if self.daylightSavings:
            if self.utcOffset > 0:
                offset += 1
            else:
                offset -= 1
        return offset

def calcNextSunriseSunSet(obsDate, obsParams):

    def convert_utc_to_local(utc_time, utc_offset):
        """COnvert UTC time to local time based on UTC offset in hours"""
        return utc_time + timedelta(hours = utc_offset)
    
    loc = EarthLocation(lat = obsParams.lat, lon = obsParams.long, height = obsParams.height)

    timezone = pytz.timezone('UTC')

    observer = Observer(location = loc, timezone = 'UTC')

    next_sunrise_utc = observer.sun_rise_time(obsDate, which = 'next')
    next_sunset_utc = observer.sun_set_time(obsDate, which = 'next')

    utc_offset_hours = obsParams.utcOffset

    next_sunrise_local = convert_utc_to_local(next_sunrise_utc.datetime, utc_offset_hours)
    next_sunset_local = convert_utc_to_local(next_sunset_utc.datetime, utc_offset_hours)

    #print(f"Next Sunset: {next_sunset_local}\nNext Sunrise: {next_sunrise_local}")


def calcDSOVisability(dso_catalog_data,obsDate,obsLocation):







    filtered_dso_catalog = []

    return filtered_dso_catalog