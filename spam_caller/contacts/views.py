from rest_framework import permissions, authentication, views, response
from .models import Contact, Spam_Number
from users.models import Profile
from django.contrib.auth.models import User
from .serializers import ContactSerializer, SpamNumberSerializer, ContactSpamSerializer
from users.serializers import ProfileSerializer, ProfileSpamSerializer
from rest_framework import status
from django.db.models import Q
import json

class ContactListView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Contact.objects.all()
        contact_serializer = ContactSerializer(queryset, many=True)

        return response.Response(contact_serializer.data)


class ContactCreateView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        phone_number = request.data.get("phone_number")
        email = '' if request.data.get("email") == None else request.data.get("email")
        user_id = request.data.get("user_id")

        existing_contact = Contact.objects.filter(
            name=name,
            phone_number=phone_number,
            user_id=user_id
        ).first()

        if existing_contact:
            return response.Response(
                {"Message": "A contact with the same name, phone number, and user ID already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            contact = Contact.objects.create(
                name = name,
                phone_number = phone_number,
                email = email,
                user_id = user_id
            )

            contact_serializer = ContactSerializer(contact)


            return response.Response(contact_serializer.data)
        except Exception as e:
            return response.Response(
                    {"Message": f"User not exits"},
                    status=status.HTTP_400_BAD_REQUEST
                )


class ContactSetSpamView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        user_id = request.data.get('user_id')
        spam_type = request.data.get('spam_type')

        existing_spam_number = Spam_Number.objects.filter(
            phone_number=phone_number,
            added_by_id=user_id
        ).first()

        if existing_spam_number:
            return response.Response(
                {"Message": "Number already registed for spam"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        spam_number = Spam_Number.objects.create(
            phone_number = phone_number,
            added_by_id = user_id,
            spam_type = spam_type if spam_type else 'spam'
        )    

        spam_number_serializer = SpamNumberSerializer(spam_number)

        return response.Response(spam_number_serializer.data)
    

class ContactSearchByNameView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        name = request.query_params.get('name', None)
        if name:
            prefix_matches = Contact.objects.filter(Q(name__startswith=name))

            substring_matches = Contact.objects.filter(Q(name__icontains=name)).exclude(Q(name__startswith=name))

            queryset = list(prefix_matches) + list(substring_matches)
        
            contact_serializer = ContactSpamSerializer(queryset, many=True)

            for contact in contact_serializer.data:

                spam_number = Spam_Number.objects.filter(phone_number = contact['phone_number'])

                spam_number_serializer = SpamNumberSerializer(spam_number, many=True)

                contact['spam_percentage'] = "{:.2f}".format(len(spam_number_serializer.data) / Profile.objects.all().count())   

            return response.Response(contact_serializer.data)
    
        else:
            return response.Response([])



    

class ContactSearchByMobileNumberView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]    
        
    def get(self, request):
        phone_number = request.query_params.get('phone_number', None)

        if phone_number:
            profile = Profile.objects.filter(phone_number = phone_number).first()

            if profile:
                profile_serializer = ProfileSpamSerializer(profile)

                spam_number = Spam_Number.objects.filter(phone_number = profile_serializer.data['phone_number'])

                spam_number_serializer = SpamNumberSerializer(spam_number, many=True)
                data = profile_serializer.data

                data['spam_percentage'] = "{:.2f}".format(len(spam_number_serializer.data) / Profile.objects.all().count())
                return response.Response(data)
            else:
                contact = Contact.objects.filter(phone_number = phone_number)
                contact_serializer = ContactSpamSerializer(contact, many=True)

                for contact in contact_serializer.data:
                    spam_number = Spam_Number.objects.filter(phone_number = contact['phone_number'])

                    spam_number_serializer = SpamNumberSerializer(spam_number, many=True)

                    contact['spam_percentage'] = "{:.2f}".format(len(spam_number_serializer.data) / Profile.objects.all().count())

                return response.Response(contact_serializer.data)
        else:
            return response.Response([])


class ContactDisplayView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        name = request.query_params.get('name', None)
        phone_number = request.query_params.get('phone_number', None)
        user_id_searcher = request.data.get('user_id')

        spam_number = Spam_Number.objects.filter(phone_number = phone_number)

        if spam_number:
            spam_number_seriealizer = SpamNumberSerializer(spam_number, many=True)
            data = spam_number_seriealizer.data[0]

            data['spam_percentage'] = "{:.2f}".format(len(spam_number_seriealizer.data)/Profile.objects.all().count())
            data['spam_registers_count'] = len(spam_number_seriealizer.data)

            profile = Profile.objects.filter(phone_number = phone_number).first()
            searcher = Profile.objects.get(id=user_id_searcher)
            
            if profile and searcher:
                profile_serializer = ProfileSerializer(profile)
                searcher_serializer = ProfileSerializer(searcher)

                contact = Contact.objects.filter(phone_number = searcher_serializer.data['phone_number'], user_id=profile_serializer.data['id']).first()

                if contact:
                    data['email'] = profile_serializer.data['email']
                return response.Response(data)
        
            else:
                return response.Response(data)
        else:
            return response.Response({'phone_number': phone_number, 'name': name, 'spam_percentage': 0.00, 'spam_registers_count': 0})