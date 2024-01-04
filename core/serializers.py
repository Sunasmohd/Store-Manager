from djoser.serializers import UserCreateSerializer as BaseUCS,UserSerializer as BaseUS

class UserCreateSerializer(BaseUCS):
  class Meta(BaseUCS.Meta):
      fields = ['id','email','username','first_name','last_name', 'password']


class UserSerializer(BaseUS):
  class Meta(BaseUS.Meta):
      fields = ['id','email','username','first_name','last_name']


