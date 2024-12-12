from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Task
from rest_framework import viewsets
from .selializers import TaskSelializers,UserSelializer
from .ownpermissions import ProfilePermissiom

class UserViewSet(viewsets.ModelViewSet):#ManageUserView：基本的なCRUD操作（Create, Read, Update, Delete）を自動的に実装
    '''
    全ユーザーデータに対してCRUD操作(作成、読み取り、更新、削除)を行うAPIエンドポイント
    全てのユーザーの取得、特定のユーザーの情報を取得、更新、削除、新しいユーザーの作成
    '''
    queryset = User.objects.all()#全てのユーザーを取得（すべてのユーザーがCRUDの対象）
    serializer_class = UserSelializer# Userモデルをシリアライズするクラス
    permission_classes = (ProfilePermissiom,)#GETやCRESTEのみアクセス可能

class ManageUserView(generics.RetrieveUpdateAPIView):#RetrieveUpdateAPIView:GETメソッドでユーザー情報を取得、PUTやPATCHでユーザー用法の更新
    '''
    トークン認証によってログインしているユーザー自身のユーザー情報の取得や更新ができる
    '''
    serializer_class = UserSelializer
    authentication_classes = (TokenAuthentication,)#リクエストに含まれる認証トークンを使用して認証を行う
    permission_classes = (IsAuthenticated,)#認証済みユーザーだけがこのエンドポイントにアクセス
    
    def get_object(self):
        '''
        ユーザー情報の取得、更新を行う関数
        selfでリクエストしたユーザー自身のデータだけが対象になる
        '''
        return self.request.user

class TaskViewSet(viewsets.ModelViewSet):
    '''
    トークン認証によってアクセスしたらすべてのTaskのデータが作成、取得、更新、削除の対象になるエンドポイント
    '''
    queryset = Task.objects.all()#すべてのTaskを取得
    serializer_class = TaskSelializers
    authentication_classes = (TokenAuthentication,)#リクエストに含まれる認証トークンを使用して認証を行う
    permission_classes = (IsAuthenticated,)#認証済みユーザーだけがこのエンドポイントにアクセス