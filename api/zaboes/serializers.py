from django.apps import apps as django_apps
from rest_framework import serializers
from apps.zaboes.models import Zabo, Timeslot, Comment, Recomment, Participate, Poster
from django.conf import settings




class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = (
            'zabo',
            'image',
        )





class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = '__all__'




class RecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )

class CommentSerializer(serializers.ModelSerializer):
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'content',
            'created_time',
            'updated_time',
            'is_private',
            'is_deleted',
            'is_blocked',
            'recomments'
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )



class ZaboSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    posters = PosterSerializer(many=True, read_only=True)
    timeslots = TimeslotSerializer(many=True, read_only=True)
    class Meta:
        model = Zabo
        fields = (
            'founder',
            'location',
            'content',
            'category',
            'apply',
            'payment',
            'created_time',
            'updated_time',
            'limit',
            'posters',
            'comments',
            'timeslots'
            )
        read_only_fields = (
            'created_time',
            'updated_time',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.


class ZaboListSerializer(serializers.ModelSerializer):
    posters = PosterSerializer(many=True, read_only=True)

    class Meta:
        model = Zabo
        fields = (
            'id',
            'founder',
            'posters',
            'created_time',
            'updated_time',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )
        # auto_now_add나 auto_now가 true이면 read_only_fields여야 함


class ZaboCreateSerializer(serializers.ModelSerializer):
    posters = PosterSerializer(many=True)
    timeslots = TimeslotSerializer(many=True)

    class Meta:
        model = Zabo
        fields = (
            'location',
            'content',
            'category',
            'apply',
            'payment',
            'timeslots',
            'deadline',
            'posters',
        )

    def create(self, validated_data):
        timeslots_data = validated_data.pop('timeslots')
        posters_data = validated_data.pop('posters')
        zabo = Zabo.objects.create(**validated_data)
        for timeslot_data in timeslots_data:
            Timeslot.objects.create(zabo=zabo, **timeslot_data)

        for poster_data in posters_data:
            Poster.objects.create(zabo=zabo, **poster_data)
        return zabo;