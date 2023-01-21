from rest_framework import serializers


class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    ph_no = serializers.CharField()
    password = serializers.CharField()
    
class PollSerializer(serializers.Serializer):
    question = serializers.CharField()
    option_1 = serializers.CharField()
    option_2 = serializers.CharField()
    option_3 = serializers.CharField()
    option_4 = serializers.CharField()
    