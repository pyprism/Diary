import django_filters
from django.db.models import Q
from django.utils.dateparse import parse_date

from diary.models import Diary, Tag
from utils.enums import PostType


class DiaryFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date")
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    post_type = django_filters.ChoiceFilter(choices=PostType.choices)
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__name",
        to_field_name="name",
        queryset=Tag.objects.all(),
        conjoined=False,
    )
    search = django_filters.CharFilter(method="filter_search")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = getattr(self, "request", None)
        if request is not None and request.user.is_authenticated:
            self.filters["tags"].queryset = Tag.objects.filter(user=request.user)
        else:
            self.filters["tags"].queryset = Tag.objects.none()

    def filter_search(self, queryset, name, value):
        value = (value or "").strip()
        if not value:
            return queryset

        tokens = [token for token in value.split() if token]
        if not tokens:
            return queryset

        searchable_fields = (
            "title__icontains",
            "post_type__icontains",
            "tags__name__icontains",
            "content__icontains",
            "analysis__status__icontains",
            "analysis__summary__icontains",
            "analysis__mood__icontains",
            "analysis__task_id__icontains",
            "analysis__error__icontains",
            "analysis__bangla_content__icontains",
        )

        for token in tokens:
            if token.isdigit():
                queryset = queryset.filter(id=int(token))
                continue

            token_filter = Q()
            for field in searchable_fields:
                token_filter |= Q(**{field: token})

            parsed_date = self._parse_search_date(token)
            if parsed_date is not None:
                token_filter |= Q(date=parsed_date)
                token_filter |= Q(created_at__date=parsed_date)
                token_filter |= Q(updated_at__date=parsed_date)

            queryset = queryset.filter(token_filter)

        return queryset.distinct()

    @staticmethod
    def _parse_search_date(token):
        parsed_date = parse_date(token)
        if parsed_date is not None:
            return parsed_date
        if len(token) == 10 and token[2] == "-" and token[5] == "-":
            return parse_date(f"{token[6:10]}-{token[3:5]}-{token[0:2]}")
        return None

    class Meta:
        model = Diary
        fields = ["date", "date_from", "date_to", "post_type", "tags", "search"]
