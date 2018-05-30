from rest_framework import filters
from apps.zaboes.models import Zabo

#작성 중...
class ArticleFilter(filters.FilterSet):
    class Meta:
        model = Zabo
        fields = {
            'title': [
                'contains',
            ],
            'content': [
                'contains',
            ],
            'is_anonymous': [
                'exact',
            ],
            'is_content_sexual': [
                'exact',
            ],
            'is_content_social': [
                'exact',
            ],
            'created_by': [
                'exact',
            ],
            'parent_topic': [
                'in',
                'exact',
            ],
            'parent_board': [
                'in',
                'exact',
            ],
        }

