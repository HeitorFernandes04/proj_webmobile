# api/serializers.py
from rest_framework import serializers
from courses.models import Course, Module, Lesson, LessonProgress


class CourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    modules_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "slug", "description", "progress", "modules_count"]

    def get_progress(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        return obj.progress_for_user(request.user)

    def get_modules_count(self, obj):
        return obj.modules.count()


class ModuleSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ["id", "title", "description", "progress", "lessons_count"]

    def get_progress(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        return obj.progress_for_user(request.user)

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["id", "title", "video_url", "content", "completed"]

    def get_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        lp = LessonProgress.objects.filter(
            user=request.user,
            lesson=obj
        ).first()
        return lp.completed if lp else False
