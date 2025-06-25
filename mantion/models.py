from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import ValidationError


class Composer(models.Model):
    composer_name = models.CharField(max_length=100)
    composer_alt_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.composer_name


class Song(models.Model):
    song_name = models.CharField(max_length=100)
    song_alt_name = models.CharField(max_length=100, blank=True, null=True)
    composer = models.ManyToManyField(Composer, blank=True)
    bpm = models.IntegerField()
    youtube_link = models.URLField(blank=True, null=True)
    keywords = ArrayField(models.CharField(max_length=50), size=20, blank=True, default=list, help_text="help searching")

    def __str__(self):
        return self.song_name

    class Meta:
        ordering = ["song_name"]


class Game(models.Model):
    game_name = models.CharField(max_length=100)
    game_abbr = models.SlugField(max_length=10)

    def __str__(self):
        return self.game_name


class Mode(models.Model):
    mode_name = models.CharField(max_length=10)
    mode_abbr = models.SlugField(max_length=4)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    diff_name = ArrayField(models.CharField(max_length=20), size=8)

    def __str__(self):
        return self.mode_name


class Pack(models.Model):
    pack_name = models.CharField(max_length=30)
    pack_abbr = models.SlugField(max_length=10)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.pack_name


class Type(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Pattern(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    diff_value = ArrayField(models.IntegerField(null=True, blank=True), blank=True, size=8)
    types = models.ManyToManyField(Type, blank=True)

    def __str__(self):
        smode = self.mode.mode_abbr if self.mode else "?"
        spack = self.pack.pack_abbr if self.pack else "?"
        return f"{smode}@{spack}:{self.song.song_name}"

    def clean(self):
        errors = {}

        if self.mode and self.pack and self.mode.game != self.pack.game:
            msg = "The selected Mode and Pack must belong to the same Game."
            errors["mode"] = msg
            errors["pack"] = msg

        if self.mode:
            max_len = len(self.mode.diff_name)
            actual_len = len(self.diff_value or [])

            if actual_len > max_len:
                errors["diff_value"] = f"Too many difficulty values: expected at most {max_len}, got {actual_len}."

        if errors:
            raise ValidationError(errors)
