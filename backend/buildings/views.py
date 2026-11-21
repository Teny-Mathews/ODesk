from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Building,OfficeSpace,BuildingImage,OfficeImage,Amenity
from .serializers import (
    BuildingSerializer,
    OfficeSpaceSerializer,
    BuildingImageSerializer,
    OfficeImageSerializer,
    AmenitySerializer,
    BuildingAmenitySerializer,
    OfficeAmenitySerializer,
    BuildingBrowseSerializer,
    BuildingBrowseDetailSerializer,
    OfficeBrowseSerializer,
    OfficeBrowseDetailSerializer
)

class BuildingListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        buildings = Building.objects.filter(owner=request.user)
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can create buildings'},
                status=status.HTTP_403_FORBIDDEN)
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BuildingDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_building(self, request, pk):
        return get_object_or_404(Building,id=pk,owner=request.user)


    def get(self, request, pk):
        building = self.get_building(request, pk)
        serializer = BuildingSerializer(building)
        return Response(serializer.data)
    

    def put(self, request, pk):
        if request.user.role != 'owner':
            return Response({'error': 'Only owners can update buildings'},
                status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(request, pk)
        serializer = BuildingSerializer(building,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can update buildings'},
                status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(request, pk)
        serializer = BuildingSerializer(
            building,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can delete buildings'},
                status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(request, pk)
        building.delete()
        return Response(
            {'message': 'Building deleted successfully'},
            status=status.HTTP_200_OK)




class OfficeSpaceListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_building(self, building_id, user):
        return get_object_or_404(Building, id=building_id, owner=user)


    def get(self, request, building_id):
        building = self.get_building(building_id, request.user)
        offices = OfficeSpace.objects.filter(building=building)
        serializer = OfficeSpaceSerializer(offices, many=True)
        return Response(serializer.data)


    def post(self, request, building_id):
        if request.user.role != 'owner':
            return Response({'error': 'Only owners can create offices'}, status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(building_id, request.user)
        serializer = OfficeSpaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(building=building)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficeSpaceDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_office(self, building_id, pk, user):
        return get_object_or_404(
            OfficeSpace,id=pk,building_id=building_id,building__owner=user)


    def get(self, request, building_id, pk):
        office = self.get_office(building_id, pk, request.user)
        serializer = OfficeSpaceSerializer(office)
        return Response(serializer.data)


    def put(self, request, building_id, pk):
        if request.user.role != 'owner':
            return Response({'error': 'Only owners can update offices'},
                            status=status.HTTP_403_FORBIDDEN)
        office = self.get_office(building_id, pk, request.user)
        serializer = OfficeSpaceSerializer(office,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, building_id, pk):
        if request.user.role != 'owner':
            return Response({'error': 'Only owners can update offices'}, status=status.HTTP_403_FORBIDDEN)
        office = self.get_office(building_id, pk, request.user)
        serializer = OfficeSpaceSerializer(office,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, building_id, pk):
        if request.user.role != 'owner':
            return Response({'error': 'Only owners can delete offices'}, status=403)
        office = self.get_office(building_id, pk, request.user)
        office.delete()
        return Response({'message': 'Office deleted successfully'}, status=200)


class BuildingImageListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_building(self, building_id, user):
        return get_object_or_404(Building,id=building_id,owner=user)

    def get(self, request, building_id):

        building = self.get_building(building_id, request.user)
        images = BuildingImage.objects.filter(building=building)
        serializer = BuildingImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, building_id):

        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can upload building images'},status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(building_id, request.user)
        serializer = BuildingImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(building=building)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BuildingImageDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_image(self, building_id, pk, user):
        return get_object_or_404(
            BuildingImage,id=pk,building_id=building_id,building__owner=user)
    
    
    def get(self, request, building_id, pk):
        image = self.get_image(building_id, pk, request.user)
        serializer = BuildingImageSerializer(image)
        return Response(serializer.data)


    def delete(self, request, building_id, pk):
        if request.user.role != 'owner':
            return Response({'error': 'Only owners can delete building images'},status=status.HTTP_403_FORBIDDEN)
        image = self.get_image(building_id, pk, request.user)
        image.image.delete(save=False)
        image.delete()
        return Response({'message': 'Building image deleted successfully'},status=status.HTTP_200_OK)


class OfficeImageListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_office(self, building_id, office_id, user):
        return get_object_or_404(OfficeSpace,id=office_id,building_id=building_id,building__owner=user)


    def get(self, request, building_id, office_id):
        office = self.get_office(building_id, office_id, request.user)
        images = OfficeImage.objects.filter(office_space=office)
        serializer = OfficeImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, building_id, office_id):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can upload office images'},status=status.HTTP_403_FORBIDDEN)
        office = self.get_office(building_id, office_id, request.user)
        serializer = OfficeImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(office_space=office)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OfficeImageDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_image(self, building_id, office_id, pk, user):
        return get_object_or_404(OfficeImage,id=pk,office_space_id=office_id,
                                office_space__building_id=building_id,office_space__building__owner=user)


    def get(self, request, building_id, office_id, pk):
        image = self.get_image(building_id, office_id, pk, request.user)
        serializer = OfficeImageSerializer(image)
        return Response(serializer.data)


    def delete(self, request, building_id, office_id, pk):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can delete office images'},
                status=status.HTTP_403_FORBIDDEN)
        image = self.get_image(building_id, office_id, pk, request.user)
        image.image.delete(save=False)
        image.delete()
        return Response({'message': 'Office image deleted successfully'},status=status.HTTP_200_OK)



class AmenityListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        amenities = Amenity.objects.all().order_by('name')
        serializer = AmenitySerializer(amenities, many=True)
        return Response(serializer.data)


    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin can create amenities."},
                status=status.HTTP_403_FORBIDDEN)
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BuildingAmenityView(APIView):

    permission_classes = [IsAuthenticated]

    def get_building(self, pk, user):
        return get_object_or_404(Building,id=pk,owner=user)


    def get(self, request, pk):
        building = self.get_building(pk, request.user)
        serializer = BuildingAmenitySerializer(building)
        return Response(serializer.data)


    def put(self, request, pk):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can assign building amenities'},
                status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(pk, request.user)
        serializer = BuildingAmenitySerializer(building,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self, request, pk):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can update building amenities'},
                status=status.HTTP_403_FORBIDDEN)
        building = self.get_building(pk, request.user)
        serializer = BuildingAmenitySerializer(building,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class OfficeAmenityView(APIView):

    permission_classes = [IsAuthenticated]

    def get_office(self, building_id, office_id, user):
        return get_object_or_404(
            OfficeSpace,
            id=office_id,
            building_id=building_id,
            building__owner=user
        )

    def get(self, request, building_id, office_id):
        office = self.get_office(building_id, office_id, request.user)
        serializer = OfficeAmenitySerializer(office)
        return Response(serializer.data)

    def put(self, request, building_id, office_id):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can assign office amenities'},
                status=status.HTTP_403_FORBIDDEN)
        office = self.get_office(building_id, office_id, request.user)
        serializer = OfficeAmenitySerializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, building_id, office_id):
        if request.user.role != 'owner':
            return Response(
                {'error': 'Only owners can update office amenities'},
                status=status.HTTP_403_FORBIDDEN)
        office = self.get_office(building_id, office_id, request.user)
        serializer = OfficeAmenitySerializer(office,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BuildingBrowseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        buildings = Building.objects.all().order_by('-created_at')
        serializer = BuildingBrowseSerializer(buildings, many=True)
        return Response(serializer.data)
    

class BuildingBrowseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        building = get_object_or_404(Building, id=pk)
        serializer = BuildingBrowseDetailSerializer(building)
        return Response(serializer.data)
    


class OfficeBrowseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        offices = OfficeSpace.objects.filter(status='available')

        city = request.query_params.get('city')
        district = request.query_params.get('district')
        min_rent = request.query_params.get('min_rent')
        max_rent = request.query_params.get('max_rent')
        min_area = request.query_params.get('min_area')
        max_area = request.query_params.get('max_area')

        # Validate numeric filters
        try:
            if min_rent is not None and float(min_rent) < 0:
                return Response({'error': 'Minimum rent cannot be negative.'}, status=400)

            if max_rent is not None and float(max_rent) < 0:
                return Response({'error': 'Maximum rent cannot be negative.'}, status=400)

            if min_area is not None and float(min_area) < 0:
                return Response({'error': 'Minimum area cannot be negative.'}, status=400)

            if max_area is not None and float(max_area) < 0:
                return Response({'error': 'Maximum area cannot be negative.'}, status=400)

            if min_rent is not None and max_rent is not None and float(min_rent) > float(max_rent):
                return Response({'error': 'Minimum rent cannot be greater than maximum rent.'}, status=400)

            if min_area is not None and max_area is not None and float(min_area) > float(max_area):
                return Response({'error': 'Minimum area cannot be greater than maximum area.'}, status=400)

        except ValueError:
            return Response({'error': 'Rent and area must contain valid numbers.'}, status=400)

        # Apply filters
        if city:
            offices = offices.filter(building__city__icontains=city)

        if district:
            offices = offices.filter(building__district__icontains=district)

        if min_rent is not None:
            offices = offices.filter(monthly_rent__gte=min_rent)

        if max_rent is not None:
            offices = offices.filter(monthly_rent__lte=max_rent)

        if min_area is not None:
            offices = offices.filter(area_sqft__gte=min_area)

        if max_area is not None:
            offices = offices.filter(area_sqft__lte=max_area)

        offices = offices.order_by('-created_at')

        serializer = OfficeBrowseSerializer(offices, many=True)

        return Response(serializer.data)



class OfficeBrowseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        office = get_object_or_404(OfficeSpace,id=pk,status='available')
        serializer = OfficeBrowseDetailSerializer(office)
        return Response(serializer.data)


    