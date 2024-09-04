from django.contrib.auth.models import User
from rest_framework import serializers
from contacts.models import Contact, Spam_Number


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__' 


class SpamNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam_Number
        fields = '__all__' 


class ContactSpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'email', 'user']
