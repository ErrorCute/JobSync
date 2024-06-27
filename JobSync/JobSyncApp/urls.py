from django.urls import path
from .import views,views_colaborador,views_reporte


urlpatterns = [

    path('index', views.index, name='index'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    
    path('', views.custom_login, name='custom_login'),
    path('registro/', views.registro, name='registro'), 
    
    path('custom_logout/', views.custom_logout, name='custom_logout'),
    # admin ---- 
    path('home/', views.home, name='home'), 
    path('colaboradores/', views.lista_colaboradores, name='colaboradores'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
     path('modificar_usuario/<int:user_id>/', views.modificar_usuario, name='modificar_usuario'),

    # gestion de trabajos admin 
    path('index_trabajo/', views.index_trabajo, name='index_trabajo'),
    path('trabajos/', views.trabajos, name='trabajos'),
     path('clientes/', views.clientes, name='clientes'),
    path('crear_trabajo/<int:cliente_id>', views.crear_trabajo, name='crear_trabajo'),
    path('modificar_trabajo/<int:trabajo_id>/', views.modificar_trabajo, name='modificar_trabajo'),
    path('eliminar_trabajo/<int:trabajo_id>/', views.eliminar_trabajo, name= 'eliminar_trabajo'),


    path('seleccionar_colaborador/', views.seleccionar_colaborador, name='seleccionar_colaborador'),
    path('ver_agenda/<int:colaborador_id>/', views.ver_agenda, name='ver_agenda'),
    
    path('trabajos_sin_asignar/<int:colaborador_id>/<str:fecha>/', views.trabajos_sin_asignar, name='trabajos_sin_asignar'),
    path('asignar-y-desasignar-trabajo/<int:user_id>', views.asignar_y_desasignar_trabajos, name='asignar_y_desasignar_trabajo'),
    # colaborador ---
    path('index_colaborador/', views.index_colaborador, name='index_colaborador'),
    path('mi_agenda/',views_colaborador.mi_agenda,name='mi_agenda'),
    path('mi_trabajos/<int:colaborador_id>/<str:fecha>/', views_colaborador.mi_trabajos, name='mi_trabajos'),
    path('reagendar_trabajo/<int:trabajo_id>/', views_colaborador.reagendar_trabajo, name='reagendar_trabajo'),
    path('actualizar_estado_trabajo/<int:trabajo_id>', views_colaborador.actualizar_estado_trabajo, name='actualizar_estado_trabajo'),
    # reportes
    # ---vista admin
    path('index_reporte/', views_reporte.index_reporte, name='index_reporte'),
    path('reporte_general/', views_reporte.reporte_general, name='reporte_general'),
    path('selecciona_colaborador_reporte/', views_reporte.selecciona_colaborador_reporte, name='selecciona_colaborador_reporte'),
    path('reporte_colaborador/<int:colaborador_id>/', views_reporte.reporte_colaborador, name='reporte_colaborador'),
    # ---vista colaborador
    path('mi_reporte/', views_reporte.mi_reporte, name='mi_reporte'),
    path('mi_perfil/', views_colaborador.mi_perfil, name='mi_perfil'),
]