# urls para front
from django.urls import path
from . import views

#Adiciona as rotas e direciona para as views
urlpatterns = [
    path('login',views.Login,name='Login'),
    path('cadastro/usuario', views.CadastroUsuario, name='CadastroUsuario'),
    path('remove/usuario/<str:user>', views.DeletaUsuario, name='DeletaUsuario'),
    path('cadastro/disciplina', views.CadastroDisciplina, name='CadastroDisciplina'),
    path('cadastro/atividade', views.CadastroAtividade, name='CadastroAtividade'),
    path('lista/disciplinas/<int:user>', views.ListaDisciplinas, name='ListaDisciplinas'),
    path('detalhes/disciplina/<int:disc>', views.InfosDisciplina, name='InfosDisciplina'),
    path('detalhes/atividade/<int:atividade_id>', views.InfosAtividade, name='InfosAtividade'),
    path('atualiza/disciplina/<int:disc>', views.AtualizaDisciplina,name='AtualizaDisciplina'),
    path('atualiza/atividade/<int:atividade_id>', views.AtualizaAtividade,name='AtualizaAtividade'),
    path('remove/disciplina/<int:disc>', views.DeletaDisciplina,name='DeletaDisciplina'),
    path('remove/atividade/<int:atividade_id>', views.DeletaAtividade,name='DeletaAtividade'),
    path('cronograma/<int:user>', views.CronogramaAtividades,name='CronogramaAtividades'),
    path('lista/atividades/<int:id>',views.ListaAtividades,name='ListaAtividades'),
]