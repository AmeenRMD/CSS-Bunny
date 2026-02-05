from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    if dictionary is None:
        return None
    return dictionary.get(key)
@register.filter
def render_difficulty(difficulty):
    """Render a difficulty badge comfortably on one line"""
    if not difficulty: return ""
    return f'<span class="difficulty-badge difficulty-{difficulty.lower()}">{difficulty.capitalize()}</span>'

@register.filter
def render_completed(count):
    """Render completed levels badge comfortably on one line"""
    return f'<span class="badge badge-success">{count} Lvls</span>'

@register.filter
def format_time(seconds):
    """Format seconds into M:SS or H:MM:SS"""
    if not isinstance(seconds, (int, float)):
        return seconds
    
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {remaining_seconds}s"
    return f"{minutes}m {remaining_seconds}s"
