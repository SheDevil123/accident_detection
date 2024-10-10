import geocoder
g = geocoder.ip('me')
print(g.latlng)
from geopy.geocoders import Nominatim
 
# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")
 
# Assign Latitude & Longitude
Latitude = "25.594095"
Longitude = "85.137566"
 
# Displaying Latitude and Longitude
print("Latitude: ", Latitude)
print("Longitude: ", Longitude)
 
# Get location with geocode
location = geolocator.geocode(str(g.latlng[0])+","+str(g.latlng[1]))
 
# Display location
print("\nLocation of the given Latitude and Longitude:")
print(location)