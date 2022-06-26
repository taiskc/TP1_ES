from django.utils.datastructures import MultiValueDictKeyError
from django.forms.models import model_to_dict
from .models import *
from .forms import *
from .utils import *
from hashlib import blake2s as khash
from copy import copy
from django.http import QueryDict
from django.utils import timezone
from datetime import datetime


@acerta_tipo("POST")
def Login(request):
    return_dict = {"sucesso":False}
    erros = []
    
    try:

        login = request.POST['login']
        senha = request.POST['senha']
        senha_cripto = str(khash(senha.encode('utf8')).hexdigest())[:30]

        usuario = Usuario.objects.get(login=login)
        if usuario.senha != senha_cripto:
            erros.append("Senha incorreta")
        else:
            return_dict["nome"] = usuario.nome
            return_dict["id"] = usuario.id
                
    except Usuario.DoesNotExist:
        erros.append("Usuário não cadastrado")

    except MultiValueDictKeyError as ex:
        erros.append(f"Campo {ex} não informado")

    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros 
    else:
        return_dict["sucesso"] = True 
    return return_dict #retorna o dicionário em formato Json

@acerta_tipo("POST")
def CadastroUsuario(request):
    return_dict = {"sucesso":False}
    erros = []

    try:
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = str(khash(usuario.senha.encode('utf8')).hexdigest())[:30]
            usuario.save()
            return_dict["id"] = usuario.id
        else:
            erros.append(form.errors)
    
    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("POST")
def CadastroDisciplina(request):
    return_dict = {"sucesso":False}
    erros = []

    try:
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['nome'] in [x[0] for x in Usuario.objects.get(pk=request.POST['usuario']).disciplinas.values_list('nome')]:
                erros.append("Já existe uma disciplina com esse nome para o usuário informado.")
            else:
                disciplina = form.save()
                return_dict["id"] = disciplina.id
        else:
            erros.append(form.errors)
    
    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("POST")
def CadastroAtividade(request):
    return_dict = {"sucesso":False}
    erros = []

    try:
        form = AtividadeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['nome'] in [x[0] for x in Disciplina.objects.get(pk=request.POST['disciplina']).atividades.values_list('nome')]:
                erros.append("Já existe uma atividade com esse nome para a disciplina informada.")
            elif form.cleaned_data['nota'] and not nota_valida(form.cleaned_data['nota'], form.cleaned_data['valor']):
                erros.append("Nota não pode ser maior que o total")
            elif form.cleaned_data['data'] and datetime.date(form.cleaned_data['data']) < timezone.now().date():
                erros.append("Data da atividade não pode ser passada")
            else:
                atividade = form.save()
                return_dict["id"] = atividade.id
        else:
            erros.append(form.errors)
    
    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("GET")
def ListaDisciplinas(request,user):
    return_dict = {"sucesso":False}
    erros = []
    try:
        disciplinas = Disciplina.objects.filter(usuario__id = user)
        if disciplinas:
            return_dict["disciplinas"] = [model_to_dict(i) for i in disciplinas]
        else:
            if not Usuario.objects.filter(id = user):
                erros.append("Não existe usuário com esse id")
            else:
                return_dict["disciplinas"] = []

    except Exception as ex:
        erros.append(str(ex))
    
    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict


@acerta_tipo("GET")
def InfosDisciplina(request,disc):
    return_dict = {"sucesso":False}
    erros = []

    try:
        disciplina = Disciplina.objects.get(id=disc)
        return_dict["disciplina"] = model_to_dict(disciplina)
        atividades = Atividade.objects.filter(disciplina__id=disc).values('id','nome','data')
        return_dict["atividades"] = list(atividades)

    except Disciplina.DoesNotExist:
        erros.append("Não existe disciplina com o código informado")  

    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("GET")
def InfosAtividade(request, atividade_id):
    return_dict = {"sucesso":False}
    erros = []

    try:
        atividade = Atividade.objects.get(id = atividade_id)
        return_dict["atividade"] = model_to_dict(atividade)
    except Atividade.DoesNotExist:
        erros.append("Não existe atividade com o código informado")  

    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("GET")
def CronogramaAtividades(request,user):
    return_dict = {"sucesso":False}
    erros = []
    try:
        Usuario.objects.get(pk=user)
        x = Atividade.objects.filter(disciplina__usuario__id=user).filter(data__gt=timezone.now()).order_by('data').values('nome','disciplina__nome','data')
        return_dict["sucesso"] = True
        return_dict["atividades"] = list(x)
    except Exception as ex:
        erros.append(str(ex))
        return_dict["erros"] = erros
    return return_dict

@acerta_tipo("PATCH")
def AtualizaDisciplina(request,disc):
    return_dict = {"sucesso":False}
    erros = []

    try:
        dados = QueryDict(request.body)
        if 'usuario' in dados:
            erros.append('Não é possível alterar o usuário que possui a disciplina')
        else:
            disciplina = Disciplina.objects.get(id=disc)
            post = copy(dados)
            for k,v in model_to_dict(disciplina).items():
                if k not in dados: post[k] = v
            form = DisciplinaForm(post,instance=disciplina)
            if form.is_valid():
                form.save()
            else:
                erros.append(form.errors)

    except Disciplina.DoesNotExist:
        erros.append("Não existe disciplina com o código informado")  

    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("PATCH")
def AtualizaAtividade(request,atividade_id):
    return_dict = {"sucesso":False}
    erros = []

    try:
        valida = nota_valida(request.data['nota'], request.data['valor'])
        if valida:
            dados = QueryDict(request.body)
            atividade = Atividade.objects.get(id=atividade_id)
            post = copy(dados)
            for k,v in model_to_dict(atividade).items():
                if k not in dados: post[k] = v
            form = AtividadeForm(post,instance=atividade)
            if form.is_valid():
                form.save()
            else:
                erros.append(form.errors)
        else:
            raise Exception("Nota não pode ser maior que o valor total")

    except Atividade.DoesNotExist:
        erros.append("Não existe atividade com o código informado")  

    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("DELETE")
def DeletaDisciplina(request,disc):
    return_dict = {"sucesso":False}
    erros = []
    try:
        dados = QueryDict(request.body)
        disciplina = Disciplina.objects.get(id=disc)
        disciplina.delete()
    
    except Disciplina.DoesNotExist:
        erros.append("Não existe disciplina com o código informado")  
    
    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("DELETE")
def DeletaUsuario(request,user):
    return_dict = {"sucesso":False}
    erros = []
    try:
        usuario = Usuario.objects.get(login=user)
        usuario.delete()
    
    except Usuario.DoesNotExist:
        erros.append("Não existe o usuário informado")  
    
    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("DELETE")
def DeletaAtividade(request,atividade_id):
    return_dict = {"sucesso":False}
    erros = []
    try:
        dados = QueryDict(request.body)
        # auth = dados["auth"]
        # if auth != 'tp1_es':
        #     raise Exception("Autenticação inválida")
        atividade = Atividade.objects.get(id=atividade_id)
        atividade.delete()
    
    except Atividade.DoesNotExist:
        erros.append("Não existe atividade com o código informado")  
    
    except Exception as ex:
        erros.append(str(ex))

    if erros:
        return_dict["erros"] = erros
    else:
        return_dict["sucesso"] = True
    return return_dict

@acerta_tipo("GET")
def ListaAtividades(request,id):
    return_dict = {"sucesso":False}
    erros = []
    try:
        Usuario.objects.get(pk=id)
        x = Atividade.objects.filter(disciplina__usuario__id=id).order_by('data').values('id','nome','valor','nota','data','disciplina__nome')
        return_dict["sucesso"] = True
        return_dict["atividades"] = list(x)
    except Exception as ex:
        erros.append(str(ex))
        return_dict["erros"] = erros
    return return_dict
