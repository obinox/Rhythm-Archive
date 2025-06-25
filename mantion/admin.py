from django.contrib import admin
from .models import *


class ComposerAdmin(admin.ModelAdmin):
    list_display = ("composer_name",)


class SongAdmin(admin.ModelAdmin):
    list_display = ("song_name", "get_composers", "bpm")

    @admin.display(description="Composers")
    def get_composers(self, obj):
        return ", ".join(c.composer_name for c in obj.composer.all())

    list_filter = ("composer",)
    search_fields = ("song_name", "composer__composer_name")


class GameAdmin(admin.ModelAdmin):
    list_display = ("game_name", "game_abbr")


class ModeAdmin(admin.ModelAdmin):
    list_display = ("mode_name", "mode_abbr", "game")
    list_filter = ("game",)


class PackAdmin(admin.ModelAdmin):
    list_display = ("pack_name", "pack_abbr", "game")
    list_filter = ("game",)


class PatternAdmin(admin.ModelAdmin):
    list_display = ("song", "mode", "pack", "display_diff_value")
    list_filter = ("mode__game", "mode", "pack")
    search_fields = ("song__song_name",)

    def display_diff_value(self, obj):
        return ", ".join(map(str, obj.diff_value)) if obj.diff_value else "N/A"

    display_diff_value.short_description = "Difficulty Values"


class TypeAdmin(admin.ModelAdmin):
    list_display = ("type_name",)
    search_fields = ("type_name",)


admin.site.register(Composer, ComposerAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Mode, ModeAdmin)
admin.site.register(Pack, PackAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Type)
