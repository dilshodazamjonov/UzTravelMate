from rest_framework import serializers
from user_preferences.models import (
    TravelDestinations,
    TravelerPreferences,
    TravelerInterest,
    Interest
)

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


class TravelerInterestSerializer(serializers.ModelSerializer):
    interest = InterestSerializer(read_only=True)
    interest_id = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(),
        source='interest',
        write_only=True
    )

    class Meta:
        model = TravelerInterest
        fields = ['interest', 'interest_id']


class TravelerPreferencesSerializer(serializers.ModelSerializer):
    top_destination = serializers.PrimaryKeyRelatedField(
        queryset=TravelDestinations.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = TravelerPreferences
        fields = [
            'travel_style',
            'budget_level',
            'top_destination',
            'travel_start_date',
            'travel_end_date',
        ]
        extra_kwargs = {field: {'required': False} for field in fields}



class TravelerPreferencesFullSerializer(serializers.Serializer):
    preferences = TravelerPreferencesSerializer()
    interests = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all()),
        allow_empty=True,
        required=False
    )

    def update(self, instance, validated_data):
        preferences_data = validated_data.get('preferences', {})
        interests_data = validated_data.get('interests', [])

        # Update or create preferences
        preferences_instance, _ = TravelerPreferences.objects.get_or_create(traveler=instance)
        for attr, value in preferences_data.items():
            setattr(preferences_instance, attr, value)
        preferences_instance.save()

        # Update interests (clear & set new)
        if interests_data is not None:
            TravelerInterest.objects.filter(traveler=instance).delete()
            TravelerInterest.objects.bulk_create([
                TravelerInterest(traveler=instance, interest=interest) for interest in interests_data
            ])

        return {
            'preferences': preferences_instance,
            'interests': interests_data
        }

    def to_representation(self, instance):
        preferences_instance = getattr(instance, 'preferences', None)
        interests = TravelerInterest.objects.filter(traveler=instance)
        return {
            'preferences': TravelerPreferencesSerializer(preferences_instance).data if preferences_instance else None,
            'interests': [ti.interest.pk for ti in interests]
        }


class TravelDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelDestinations
        fields = ['id', 'name', 'description', 'image']


class ChoiceItemSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class PreferencesChoicesSerializer(serializers.Serializer):
    travel_styles = ChoiceItemSerializer(many=True)
    budget_levels = ChoiceItemSerializer(many=True)

    @classmethod
    def get_data(cls):
        def format_choices(choices):
            return [{'value': k, 'label': v} for k, v in choices]

        return {
            'travel_styles': format_choices(TravelerPreferences._meta.get_field('travel_style').choices),
            'budget_levels': format_choices(TravelerPreferences._meta.get_field('budget_level').choices),
        }