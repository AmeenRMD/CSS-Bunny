from django.contrib import admin
from .models import Level, UserProgress, UserStats


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level_number', 'title', 'css_property', 'difficulty', 'bunny_count', 'carrot_count']
    list_filter = ['difficulty', 'css_property']
    search_fields = ['title', 'instruction', 'css_property']
    ordering = ['level_number']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('level_number', 'title', 'css_property', 'difficulty')
        }),
        ('Game Setup', {
            'fields': ('bunny_count', 'carrot_count', 'instruction')
        }),
        ('Solution', {
            'fields': ('correct_solution',),
            'description': 'Enter correct CSS solution. For multiple valid solutions, separate with ||'
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'completed', 'time_taken', 'attempts', 'completed_at']
    list_filter = ['completed', 'level']
    search_fields = ['user__username', 'level__title']
    readonly_fields = ['created_at', 'completed_at']
    ordering = ['user', 'level__level_number']


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_levels_completed', 'highest_level_reached', 'total_time_spent', 'last_played_level']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-highest_level_reached', 'total_time_spent']
    
    actions = ['recalculate_stats']
    
    def recalculate_stats(self, request, queryset):
        for stats in queryset:
            stats.update_stats()
        self.message_user(request, f"Recalculated stats for {queryset.count()} users.")
    recalculate_stats.short_description = "Recalculate selected user stats"
