from rest_framework import serializers
from .models import CustomUser, Organization, Event


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'phone_number',
            'password', 
            'organization',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        organization_data = representation.pop('organization', None)
        event_data = representation.pop('event', None)

        if organization_data:
            if isinstance(organization_data, int):
                organization_instance = Organization.objects.get(pk=organization_data)
                representation['organization'] = OrganizationSerializer(organization_instance).data
            else:
                representation['organization'] = OrganizationSerializer(organization_data).data

        if event_data:
            representation['event'] = EventSerializer(event_data).data

        return representation


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'title', 'address', 'postcode')


class EventSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()
    users = CustomUserSerializer(
        many=True,
        source='participants',
        read_only=True
    )

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'organizations',
            'users',
            'image',
            'date'
        )

    def get_organizations(self, instance):
        organizations_data = instance.organizations.all()
        return OrganizationSerializer(organizations_data, many=True, read_only=True).data

    def get_image_preview(self, obj):
        if obj.image:
            return obj.image.url
        return None
