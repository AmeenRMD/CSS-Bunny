from django.shortcuts import render, redirect
from django.db.models import Q, F
from game.models import UserStats
from django.contrib.auth.models import User


def leaderboard(request):
    """Global leaderboard view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('game:admin_panel')
        
    # Get all user stats ordered by highest level reached (desc) and total time (asc)
    # Exclude admins/staff from the leaderboard
    leaderboard_data = UserStats.objects.select_related('user').filter(
        total_levels_completed__gt=0,
        user__is_staff=False
    ).order_by('-highest_level_reached', 'total_time_spent')
    
    # Add rank
    ranked_data = []
    for idx, stats in enumerate(leaderboard_data, 1):
        hours = stats.total_time_spent // 3600
        minutes = (stats.total_time_spent % 3600) // 60
        seconds = stats.total_time_spent % 60
        
        ranked_data.append({
            'rank': idx,
            'user': stats.user,
            'stats': stats,
            'time_formatted': f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
        })
    
    # Get current user's rank if authenticated
    current_user_rank = None
    if request.user.is_authenticated:
        try:
            user_stats = UserStats.objects.get(user=request.user)
            for item in ranked_data:
                if item['user'] == request.user:
                    current_user_rank = item['rank']
                    break
        except UserStats.DoesNotExist:
            pass
    
    context = {
        'leaderboard': ranked_data[:100],  # Top 100
        'current_user_rank': current_user_rank,
        'total_players': len(ranked_data)
    }
    
    return render(request, 'leaderboard/leaderboard.html', context)
