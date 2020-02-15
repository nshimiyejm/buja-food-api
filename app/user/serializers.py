from django.contrib.auth import get_user_model , authenticate
from django.utils.translation  import ugettext_lazy as _

from rest_framework import serializers 

class UserSericalizer(serializers.ModelSerializer):
    """ Serializer for the user object""" 

    class Meta: 
        # Model we are basing the model serializer from 
        model = get_user_model()
        fields = ('email', 'password', 'name')

        # Configure extra settings in the serializer 
        extra_kwargs = {'password': {'write_only':True, 'min_length': 5}}
    
    # Overriding the create function 
    def create(self, validated_data):
        """Create new user with encrypted passwrod and return it"""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and returning it"""
        # instance is the model instance lineked to the model serializer 
        # valided_data is the data created above in the meta 
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password: 
            user.set_password(password)
            user.save()
        return user



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        trim_whitespace=False
    )
    # Validate the sericalize all values are correct 
    def validate(self, attrs): 
        """Validate and auth the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'), 
            username=email, 
            password=password
        )
        if not user: 
            msg = _('unable to authenticate with provided credentals')
            raise serializers.ValidationError(msg, code='authorization')

        # when overriding the validate function and if the auth is successful 
        # Return the values at the end 
        attrs['user'] = user

        return attrs