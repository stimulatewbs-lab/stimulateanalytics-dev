
from django.contrib import admin
from .models import Sport, Competition, Match


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "sport", "country", "is_active")
    list_filter = ("sport", "country", "is_active")
    search_fields = ("name", "country")


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "home_team",
        "away_team",
        "competition",
        "kickoff",
        "status",
        "home_score",
        "away_score",
        "is_featured",
    )
    list_filter = ("status", "competition", "is_featured")
    search_fields = ("home_team", "away_team")
    list_editable = ("status", "home_score", "away_score", "is_featured")
    date_hierarchy = "kickoff"
