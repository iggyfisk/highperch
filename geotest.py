import geoip2.database
import sys


def geoip_country(ip_addr):
    reader = geoip2.database.Reader('perchweb/resource/GeoLite2-Country.mmdb')
    try:
        response = reader.country(ip_addr)
        result = {'code': response.country.iso_code,
                  'name': response.country.name}
        return result
    except Exception as e:
        return {'code': "xx", 'name': "unknown"}


def geoip_city(ip_addr):
    reader = geoip2.database.Reader('perchweb/resource/GeoLite2-City.mmdb')
    try:
        response = reader.city(ip_addr)
        return (response.city.name, response.subdivisions.most_specific.iso_code)
    except Exception as e:
        return 'unknown'

def format_ip_addr(ip_addr):
    country_code = geoip_country(ip_addr)['code']
    city, subdivision = geoip_city(ip_addr)
    return f'{ip_addr} ({city}, {subdivision}, {country_code})'

print(format_ip_addr(sys.argv[1]))