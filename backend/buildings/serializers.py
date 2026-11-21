from rest_framework import serializers
from buildings.models import Building,OfficeSpace,BuildingImage,OfficeImage,Amenity


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = [
            'id',
            'building_name',
            'address',
            'city',
            'district',
            'state',
            'pincode',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OfficeSpaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeSpace
        fields = [
            'id',
            'building',
            'office_number',
            'area_sqft',
            'monthly_rent',
            'security_deposit',
            'status',
            'description',
            'created_at',
            'updated_at',
        ]

        read_only_fields = ['id', 'building', 'created_at', 'updated_at']

class BuildingImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingImage
        fields = [
            'id',
            'building',
            'image',
            'caption',
            'created_at',
        ]

        read_only_fields = ['id', 'building', 'created_at']


class OfficeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeImage
        fields = ['id', 'office_space', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'office_space', 'created_at']


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ['id', 'name', 'amenity_type', 'description']



class BuildingAmenitySerializer(serializers.ModelSerializer):

    amenities = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(),many=True)

    class Meta:
        model = Building
        fields = ['id', 'building_name', 'amenities']
        read_only_fields = ['id', 'building_name']

    def validate_amenities(self, value):
        for amenity in value:
            if amenity.amenity_type not in ['building', 'both']:
                raise serializers.ValidationError(
                    f"{amenity.name} cannot be assigned to a building.")
        return value
    

class OfficeAmenitySerializer(serializers.ModelSerializer):

    amenities = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(),many=True)

    class Meta:
        model = OfficeSpace
        fields = ['id', 'office_number', 'amenities']
        read_only_fields = ['id', 'office_number']

    def validate_amenities(self, value):
        for amenity in value:
            if amenity.amenity_type not in ['office', 'both']:
                raise serializers.ValidationError(
                    f"{amenity.name} cannot be assigned to an office."
                )
        return value
    

class BuildingBrowseSerializer(serializers.ModelSerializer):

    amenities = serializers.StringRelatedField(many=True)
    images = BuildingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = [
            'id',
            'building_name',
            'address',
            'city',
            'district',
            'state',
            'pincode',
            'description',
            'amenities',
            'images',
        ]


class OfficeBrowseSerializer(serializers.ModelSerializer):

    amenities = serializers.StringRelatedField(many=True)
    images = OfficeImageSerializer(many=True, read_only=True)

    class Meta:
        model = OfficeSpace
        fields = [
            'id',
            'office_number',
            'area_sqft',
            'monthly_rent',
            'security_deposit',
            'status',
            'description',
            'amenities',
            'images',
        ]


class BuildingBrowseDetailSerializer(serializers.ModelSerializer):

    amenities = serializers.StringRelatedField(many=True)
    images = BuildingImageSerializer(many=True, read_only=True)
    office_spaces = OfficeBrowseSerializer(source='office_spaces',many=True,read_only=True)

    class Meta:
        model = Building
        fields = [
            'id',
            'building_name',
            'address',
            'city',
            'district',
            'state',
            'pincode',
            'description',
            'amenities',
            'images',
            'office_spaces',
        ]


class OfficeBrowseDetailSerializer(serializers.ModelSerializer):

    amenities = serializers.StringRelatedField(many=True)
    images = OfficeImageSerializer(many=True, read_only=True)
    building = BuildingBrowseSerializer(read_only=True)

    class Meta:
        model = OfficeSpace
        fields = [
            'id',
            'building',
            'office_number',
            'area_sqft',
            'monthly_rent',
            'security_deposit',
            'status',
            'description',
            'amenities',
            'images',
        ]
