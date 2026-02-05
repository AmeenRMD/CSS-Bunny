from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Level(models.Model):
    """Represents a CSS learning level in the game"""
    level_number = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    instruction = models.TextField(help_text="Instructions shown to the player")
    css_property = models.CharField(max_length=100, help_text="CSS property being taught (e.g., flex-direction)")
    correct_solution = models.TextField(help_text="Correct CSS solution (can be multiple valid solutions separated by ||)")
    bunny_count = models.IntegerField(default=1, help_text="Number of bunnies in this level")
    carrot_count = models.IntegerField(default=1, help_text="Number of carrots in this level")
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='easy'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['level_number']

    def __str__(self):
        return f"Level {self.level_number}: {self.title}"

    def validate_solution(self, user_css):
        """
        Validates if the user's CSS matches any of the correct solutions.
        Ignores unknown properties and focuses on the required ones.
        """
        import re
        
        def get_props(css):
            """Extracts property-value pairs into a normalized dictionary"""
            # Remove comments
            css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
            # Remove all whitespace for keys/values
            props = {}
            for item in css.split(';'):
                if ':' in item:
                    k, v = item.split(':', 1)
                    # Normalize: lowercase and remove all whitespace
                    k = re.sub(r'\s+', '', k.lower())
                    v = re.sub(r'\s+', '', v.lower())
                    if k:
                        props[k] = v
            return props
        
        user_props = get_props(user_css)
        valid_solutions = self.correct_solution.split('||')
        
        for solution in valid_solutions:
            target_props = get_props(solution)
            if not target_props:
                continue
            
            # Check if all target properties are present and match in user_props
            match = True
            for k, v in target_props.items():
                if k not in user_props or user_props[k] != v:
                    match = False
                    break
            
            if match:
                return True
        return False


class UserProgress(models.Model):
    """Tracks user progress through levels"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0, help_text="Best/Latest time taken in seconds")
    attempt_times = models.JSONField(default=list, help_text="List of all attempt times in seconds")
    attempts = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'level']
        ordering = ['level__level_number']

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{self.user.username} - Level {self.level.level_number} {status}"
    
    def get_average_time(self):
        """Calculate average time from all attempts"""
        if self.attempt_times:
            return sum(self.attempt_times) / len(self.attempt_times)
        return self.time_taken


class UserStats(models.Model):
    """Overall statistics for a user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_levels_completed = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0, help_text="Total average time in seconds")
    highest_level_reached = models.IntegerField(default=0)
    last_played_level = models.IntegerField(default=1)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, help_text="User's profile picture")

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + self.user.username
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User stats"

    def __str__(self):
        return f"{self.user.username} - Stats"

    def update_stats(self):
        """Recalculate user statistics using average times"""
        completed_progress = UserProgress.objects.filter(user=self.user, completed=True)
        self.total_levels_completed = completed_progress.count()
        
        # Calculate total time using average of all attempts for each level
        total_avg_time = 0
        for progress in completed_progress:
            total_avg_time += progress.get_average_time()
        self.total_time_spent = int(total_avg_time)
        
        if completed_progress.exists():
            self.highest_level_reached = completed_progress.order_by('-level__level_number').first().level.level_number
        
        self.save()
