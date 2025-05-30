from friend.models import *
import math
from account.models import UserLocation, TravelerProfile


def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender,receiver=receiver, is_active=True)

    except FriendRequest.DoesNotExist:
        return False



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def get_nearby_users(current_user, radius_km=100, max_results=15):
    try:
        current_location = current_user.location
    except UserLocation.DoesNotExist:
        return []

    if current_location.latitude is None or current_location.longitude is None:
        return []

    nearby = []
    for location in UserLocation.objects.exclude(user=current_user).exclude(latitude__isnull=True).exclude(longitude__isnull=True):
        distance = haversine(
            current_location.latitude, current_location.longitude,
            location.latitude, location.longitude
        )
        if distance <= radius_km:
            user = location.user
            # Filter: only travelers with complete profiles and shared interests
            if user.user_type == 'traveler':
                try:
                    profile = user.travelerprofile
                    if profile.is_profile_complete() and \
                       set(profile.interests).intersection(set(current_user.travelerprofile.interests)):
                        nearby.append((user, distance))
                except TravelerProfile.DoesNotExist:
                    continue

    nearby.sort(key=lambda x: x[1])  # Sort by distance ascending
    return [user for user, dist in nearby[:max_results]]

