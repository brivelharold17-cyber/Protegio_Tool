from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_home(request):
    """Dashboard principal avec statistiques et accès aux applications"""
    
    # Applications disponibles avec leurs informations
    apps_menu = [
        {
            'name': 'Checker',
            'icon': 'fa-magnifying-glass',
            'color': 'primary',
            'description': 'Vérifier les informations',
            'url': '#',
            'stats': 1250
        },
        {
            'name': 'DNS Tool',
            'icon': 'fa-globe',
            'color': 'info',
            'description': 'Outils DNS avancés',
            'url': '#',
            'stats': 340
        },
        {
            'name': 'Scanner',
            'icon': 'fa-radar',
            'color': 'danger',
            'description': 'Scanner de vulnérabilités',
            'url': '#',
            'stats': 789
        },
        {
            'name': 'Intruder',
            'icon': 'fa-lock',
            'color': 'warning',
            'description': 'Tests de pénétration',
            'url': '#',
            'stats': 420
        },
        {
            'name': 'Protegio Tools',
            'icon': 'fa-shield',
            'color': 'success',
            'description': 'Outils de protection',
            'url': '#',
            'stats': 560
        },
        {
            'name': 'Performance',
            'icon': 'fa-tachometer-alt',
            'color': 'secondary',
            'description': 'Analyse de performance',
            'url': '#',
            'stats': 210
        },
        {
            'name': 'Checker Reports',
            'icon': 'fa-file-chart-line',
            'color': 'primary',
            'description': 'Rapports détaillés',
            'url': '#',
            'stats': 95
        },
        {
            'name': 'Intégrations',
            'icon': 'fa-puzzle-piece',
            'color': 'info',
            'description': 'Intégrations externes',
            'url': '#',
            'stats': 12
        },
    ]
    
    # Statistiques globales
    stats = {
        'total_scans': 3666,
        'vulnerabilities': 42,
        'reports_generated': 156,
        'active_tasks': 8,
        'users_online': 3,
    }
    
    context = {
        'stats': stats,
        'apps_menu': apps_menu,
    }
    
    return render(request, 'dashboard/dashboard.html', context)