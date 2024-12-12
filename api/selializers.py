from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#クライアントから送信されたhttp形式のデータをpythonで読み込めるように文字列などに変換したり、クライアントにpythonのデータである、数値や文字列などをjson形式に変換することで異なる言語とデータをやり取りできるようにする
class UserSelializer(serializers.ModelSerializer):
    class Meta:
        '''
        シリアライザーが使用するモデルとフィールドの定義
        '''
        model = User
        fields = ('id','username','password')
        #パスワードを書き込み専用にして、レスポンスとして返せないようにする、パスワードを必須にする
        extra_kwargs = {'password':{'write_only':True, 'required':True}}
        
        def create(self, validated_data):
            '''
            新しいユーザーを作成するときに呼び出すメソッドの定義
            '''
            #リクエスト内容からパスワードのハッシュ化などを自動で行いユーザーを作成
            user = User.objects.create_user(**validated_data)
            #新しいユーザーが作成された後、トークン認証のためのトークンを生成
            Token.objects.create(user=user)
            #作成されたユーザーを返す
            return user

class TaskSelializers(serializers.HyperlinkedModelSerializer):
    '''
    HyperlinkedModelSerializerの場合、モデルが一対多で結ぶ付けられている時りれしょなるデータをidではなく、urlで返す
    http://example.com/api/tasks/1/
    上記のurlはurls.pyで定義したものから自動で生成
    '''
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = Task
        fields = ['id','title','created_at','updated_at']
