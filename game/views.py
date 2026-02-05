from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import models
from .models import Level, UserProgress, UserStats
import json
import time


@login_required
def play(request):
    """Main game view - shows level selection or redirects to current level"""
    user_stats, created = UserStats.objects.get_or_create(user=request.user)
    
    # Get or create progress for all levels
    levels = Level.objects.all()
    for level in levels:
        UserProgress.objects.get_or_create(user=request.user, level=level)
    
    # Get user's progress
    progress = UserProgress.objects.filter(user=request.user).select_related('level')
    
    # Calculate progress percentage
    total_levels = levels.count()
    completed_levels = progress.filter(completed=True).count()
    progress_percentage = (completed_levels / total_levels * 100) if total_levels > 0 else 0
    
    context = {
        'levels': levels,
        'progress': {p.level.level_number: p for p in progress},
        'user_stats': user_stats,
        'progress_percentage': round(progress_percentage, 1),
        'perc': round(progress_percentage, 1),
        'completed_levels': completed_levels,
        'total_levels': total_levels,
    }
    
    return render(request, 'game/level_select.html', context)


@login_required
def play_level(request, level_number):
    """Play a specific level"""
    level = get_object_or_404(Level, level_number=level_number)
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        level=level
    )
    
    # Check if previous level is completed (except for level 1)
    if level_number > 1 and not request.user.is_staff:
        previous_level = Level.objects.filter(level_number=level_number - 1).first()
        if previous_level:
            previous_progress = UserProgress.objects.filter(
                user=request.user,
                level=previous_level
            ).first()
            if not previous_progress or not previous_progress.completed:
                return redirect('game:play')
    
    # Update last played level
    user_stats, created = UserStats.objects.get_or_create(user=request.user)
    user_stats.last_played_level = level_number
    user_stats.save()
    
    context = {
        'level': level,
        'user_progress': user_progress,
    }
    
    return render(request, 'game/play_level.html', context)


@login_required
@require_POST
def validate_solution(request):
    """AJAX endpoint to validate user's CSS solution"""
    try:
        data = json.loads(request.body)
        level_number = data.get('level_number')
        user_css = data.get('css', '').strip()
        time_taken = data.get('time_taken', 0)
        
        level = get_object_or_404(Level, level_number=level_number)
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            level=level
        )
        
        # Increment attempts
        user_progress.attempts += 1
        
        # Validate solution
        is_correct = level.validate_solution(user_css)
        
        # Admin testing mode: don't save progress
        if request.user.is_staff:
            next_level = Level.objects.filter(level_number=level_number + 1).first()
            return JsonResponse({
                'success': is_correct,
                'message': f'✅ (Admin Mode) Correct! Solution is valid.' if is_correct else '❌ (Admin Mode) Not quite right.',
                'next_level': next_level.level_number if is_correct and next_level else None,
                'attempts': 'N/A'
            })

        if is_correct and not user_progress.completed:
            # Mark as completed
            user_progress.completed = True
            user_progress.time_taken = time_taken
            
            # Track attempt time for average calculation
            if not user_progress.attempt_times:
                user_progress.attempt_times = []
            user_progress.attempt_times.append(time_taken)
            
            user_progress.completed_at = timezone.now()
            user_progress.save()
            
            # Update user stats
            user_stats, created = UserStats.objects.get_or_create(user=request.user)
            user_stats.update_stats()
            
            # Check if there's a next level
            next_level = Level.objects.filter(level_number=level_number + 1).first()
            
            return JsonResponse({
                'success': True,
                'message': f'✅ Correct! Level completed in {time_taken}s! 🥕',
                'next_level': next_level.level_number if next_level else None,
                'attempts': user_progress.attempts
            })
        elif is_correct:
            # Already completed, but track the attempt time
            if not user_progress.attempt_times:
                user_progress.attempt_times = []
            user_progress.attempt_times.append(time_taken)
            user_progress.save()
            
            # Update stats with new average
            user_stats, created = UserStats.objects.get_or_create(user=request.user)
            user_stats.update_stats()
            
            avg_time = user_progress.get_average_time()
            return JsonResponse({
                'success': True,
                'message': f'✅ Correct! (Avg time: {int(avg_time)}s)',
                'already_completed': True,
                'attempts': user_progress.attempts
            })
        else:
            user_progress.save()  # Save incremented attempts
            return JsonResponse({
                'success': False,
                'message': '❌ Not quite right. Try again! 🐰',
                'attempts': user_progress.attempts
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=400)


@login_required
def user_dashboard(request):
    """User dashboard showing progress and stats"""
    user_stats, created = UserStats.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            user_stats.avatar = avatar_file
            user_stats.save()
            from django.contrib import messages
            messages.success(request, "Avatar updated successfully! 🐰")
            return redirect('game:dashboard')

    progress = UserProgress.objects.filter(user=request.user).select_related('level').order_by('level__level_number')
    
    # Calculate additional stats
    total_levels = Level.objects.count()
    completed_count = progress.filter(completed=True).count()
    progress_percentage = (completed_count / total_levels * 100) if total_levels > 0 else 0
    
    # Format time
    hours = user_stats.total_time_spent // 3600
    minutes = (user_stats.total_time_spent % 3600) // 60
    seconds = user_stats.total_time_spent % 60
    
    # Calculate global rank (exclude staff)
    if request.user.is_staff:
        global_rank = "Admin ⚙️"
    else:
        better_users = UserStats.objects.filter(
            models.Q(total_levels_completed__gt=user_stats.total_levels_completed) |
            models.Q(total_levels_completed=user_stats.total_levels_completed, total_time_spent__lt=user_stats.total_time_spent),
            user__is_staff=False
        ).count()
        global_rank = f"#{better_users + 1}"
    
    context = {
        'user_stats': user_stats,
        'progress': progress,
        'total_levels': total_levels,
        'completed_count': completed_count,
        'progress_percentage': round(progress_percentage, 1),
        'perc': round(progress_percentage, 1),
        'time_formatted': f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s",
        'global_rank': global_rank
    }
    
    return render(request, 'game/dashboard.html', context)


# ================= Admin Panel Views =================
from django.contrib.auth.decorators import user_passes_test
from .forms import LevelForm
from django.contrib.auth.models import User
from django.contrib import messages

def staff_check(user):
    return user.is_staff

@user_passes_test(staff_check)
def admin_panel(request):
    """Main admin cockpit"""
    stats = {
        'total_users': User.objects.filter(is_staff=False).count(),
        'total_levels': Level.objects.count(),
        'total_completed': UserProgress.objects.filter(completed=True).count(),
        'completed_levels_avg': UserProgress.objects.filter(completed=True).count() / max(User.objects.filter(is_staff=False).count(), 1),
    }
    return render(request, 'game/admin/panel.html', {'stats': stats})

@user_passes_test(staff_check)
def admin_levels(request):
    """List all levels for management"""
    levels = Level.objects.all().order_by('level_number')
    return render(request, 'game/admin/levels_list.html', {'levels': levels})

@user_passes_test(staff_check)
def admin_level_add(request):
    """Add a new level"""
    if request.method == 'POST':
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New level added to the garden! 🥕")
            return redirect('game:admin_levels')
    else:
        form = LevelForm()
    return render(request, 'game/admin/level_form.html', {'form': form, 'title': 'Add New Level'})

@user_passes_test(staff_check)
def admin_level_edit(request, pk):
    """Edit existing level"""
    level = get_object_or_404(Level, pk=pk)
    if request.method == 'POST':
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, f"Level {level.level_number} updated! 📝")
            return redirect('game:admin_levels')
    else:
        form = LevelForm(instance=level)
    return render(request, 'game/admin/level_form.html', {'form': form, 'title': f'Edit Level {level.level_number}'})

@user_passes_test(staff_check)
@require_POST
def admin_level_delete(request, pk):
    """Delete a level"""
    level = get_object_or_404(Level, pk=pk)
    level.delete()
    messages.warning(request, "Level removed from history. 🗑️")
    return redirect('game:admin_levels')

@user_passes_test(staff_check)
def admin_users(request):
    """List all players for management"""
    users = User.objects.filter(is_staff=False).prefetch_related('stats')
    return render(request, 'game/admin/users_list.html', {'users': users})

@user_passes_test(staff_check)
@require_POST
def admin_user_delete(request, pk):
    """Ban/Delete a user"""
    user = get_object_or_404(User, pk=pk, is_staff=False)
    user.delete()
    messages.error(request, "Player has been removed from the garden. 🚪")
    return redirect('game:admin_users')

