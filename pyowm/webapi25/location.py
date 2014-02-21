#!/usr/bin/env python

"""
Module containing location-related classes and data structures.
"""

import json


class Location(object):
    """
    A class representing a location in the world. A location is defined through
    a toponym, a couple of geographic coordinates such as longitude and
    latitude and a numeric identifier assigned by the OWM web API that uniquely
    spots the location in the world. Optionally, the country specification may
    be provided.

    Further reference about OWM city IDs can be found at:
    http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID

    :param name: the location's toponym
    :type name: Unicode
    :param lon: the location's longitude, must be between -180.0 and 180.0
    :type lon: int/float
    :param lat: the location's latitude, must be between -90.0 and 90.0
    :type lat: int/float
    :param ID: the location's OWM city ID
    :type ID: int
    :param country: the location's country (``None`` by default)
    :type country: Unicode
    :returns: a *Location* instance
    :raises: *ValueError* if lon or lat values are provided out of bounds
    """

    def __init__(self, name, lon, lat, ID, country=None):
        self._name = name
        if lon < -180.0 or lon > 180.0:
            raise ValueError("'lon' value must be between -180 and 180")
        self._lon = float(lon)
        if lat < -90.0 or lat > 90.0:
            raise ValueError("'lat' value must be between -90 and 90")
        self._lat = float(lat)
        self._ID = ID
        self._country = country

    def get_name(self):
        """
        Returns the toponym of the location

        :returns: the Unicode toponym

        """
        return self._name

    def get_lon(self):
        """
        Returns the longitude of the location

        :returns: the float longitude

        """
        return self._lon

    def get_lat(self):
        """
        Returns the latitude of the location

        :returns: the float latitude

        """
        return self._lat

    def get_ID(self):
        """
        Returns the OWM city ID of the location

        :returns: the int OWM city ID

        """
        return self._ID

    def get_country(self):
        """
        Returns the country of the location

        :returns: the Unicode country

        """
        return self._country

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({'name': self._name,
                         'coordinates': {'lon': self._lon, 'lat': self._lat},
                         'ID': self._ID, 'country': self._country})

    def to_XML(self):
        """Dumps object fields into a XML formatted string

        :returns:  the XML string

        """
        return '<location><name>%s</name><coordinates><lon>%s</lon>' \
                '<lat>%s</lat></coordinates><ID>%s</ID><country>%s</country>' \
                '</location>' % (self._name, self._lon, self._lat,
                                 self._ID, self._country)

    def __repr__(self):
        return "<%s.%s - id=%s, name=%s, lon=%s, lat=%s>" % (__name__, \
          self.__class__.__name__, self._ID, self._name, str(self._lon), \
          str(self._lat))


def location_from_dictionary(d):
    """
    Builds a *Location* object out of a data dictionary. Only certain
    properties of the dictionary are used: if these properties are not
    found or cannot be read, an error is issued.

    :param d: a data dictionary
    :type d: dict
    :returns: a *Location* instance
    :raises: *KeyError* if it is impossible to find or read the data
        needed to build the instance

    """
    country = None
    if 'sys' in d and 'country' in d['sys']:
        country = d['sys']['country']
    if 'city' in d:
        data = d['city']
    else:
        data = d
    name = data['name']
    lon = data['coord']['lon']
    lat = data['coord']['lat']
    ID = int(data['id'])
    if 'country' in data:
        country = data['country']
    return Location(name, lon, lat, ID, country)
