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
            'url': '/checker/',
            'stats': 1250
        },
        {
            'name': 'DNS Tool',
            'icon': 'fa-globe',
            'color': 'info',
            'description': 'Outils DNS avancés',
            'url': '/dns_tool/',
            'stats': 340
        },
        {
            'name': 'Scanner',
            'icon': 'fa-radar',
            'color': 'danger',
            'description': 'Scanner de vulnérabilités',
            'url': '/scanner/',
            'stats': 789
        },
        {
            'name': 'Intruder',
            'icon': 'fa-lock',
            'color': 'warning',
            'description': 'Tests de pénétration',
            'url': '/intruder/',
            'stats': 420
        },
        {
            'name': 'Protegio Tools',
            'icon': 'fa-shield',
            'color': 'success',
            'description': 'Outils de protection',
            'url': '/protegioTools/',
            'stats': 560
        },
        {
            'name': 'Performance',
            'icon': 'fa-tachometer-alt',
            'color': 'secondary',
            'description': 'Analyse de performance',
            'url': '/perforNet/',
            'stats': 210
        },
        {
            'name': 'Reports',
            'icon': 'fa-file-chart-line',
            'color': 'primary',
            'description': 'Rapports détaillés',
            'url': '/reports/',
            'stats': 95
        },
        {
            'name': 'Intégrations',
            'icon': 'fa-puzzle-piece',
            'color': 'info',
            'description': 'Intégrations externes',
            'url': '/integrations/',
            'stats': 12
        },
        {
            'name': 'DIG-MX Tool',
            'icon': 'fa-network-wired',
            'color': 'danger',
            'description': 'DNS MX Lookup',
            'url': '/dig-mx/',
            'stats': 0
        },
        {
            'name': 'SQLMap Scanner',
            'icon': 'fa-database',
            'color': 'danger',
            'description': 'SQL Injection Scanner',
            'url': '/sqlmap/',
            'stats': 0
        },
        {
            'name': 'NIKTO',
            'icon': 'fa-shield-virus',
            'color': 'danger',
            'description': 'Web Server Scanner',
            'url': '/nikto/',
            'stats': 0
        },
        {
            'name': 'burp_suite',
            'icon': 'fa-lock-open',
            'color': 'danger',
            'description': 'Web Security Testing',
            'url': '/burp-suite/',
            'stats': 0
        },
    ]
    
    # Statistiques globales
    stats = {
        'total_scans': 3666,
        'vulnerabilities': 42,
        'reports_generated': 156,
        'active_tasks': 8,
        'users_online': 3,
        'protegioTools_uses': 42,
        'checker_uses': 47,
        'scanner_uses': 111,
        'dns_tool_uses': 112,
        'dig_mx_uses': 0,
        'sqlmap_uses': 0,
        'nikto_uses': 50,
        'burp_suite_uses': 34,
    }
    
    context = {
        'stats': stats,
        'apps_menu': apps_menu,
    }
    
    return render(request, 'dashboard/dashboard.html', context)