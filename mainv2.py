import os
from platform import system as sys
import hashlib

class Main:
    def __init__(self):
        self.usuario = None

    def CriaUsuario(self):
        self.usuario = Usuario()

    def main(self):
        def ExecutaFuncao(cmd, functions):
            func = functions.get(cmd)
            if func:
                func()
            else:
                print("Escolha Inválida!")

        logou, motivo = False, "Login ainda não começou."

        while True:
            ManipulaTerminal.Limpa()
            print("Você quer:\n1 = logar\n2 = Cadastrar")
            cmd = input(" -> ").strip()
            if cmd.isdigit() and int(cmd) in [1,2]:
                break
            else:
                input("Insira um valor válido!")

        if int(cmd) == 1:
            nome, senha = Login.PerguntaDados()
            logou, motivo = Login.LoginUsuario(nome, senha)
            if logou:
                print("Login realizado com sucesso!")
            else:
                print(motivo)
        else:
            SignIn.CadastraUsuario()
            logou = True


        while True:
            if not logou:
                break
            functions = self.usuario.Funcoes()
            ManipulaTerminal.Limpa()
            ManipulaTerminal.Cabecalho(self.usuario.nome_usuario)
            if self.usuario.tipo_usuario == "adm":
                ManipulaTerminal.CabecalhoAdm()

            cmd = input(" -> ").strip()
            if cmd.isdigit() and int(cmd) in functions:
                ExecutaFuncao(int(cmd),functions)
            elif cmd.isdigit() and int(cmd) == 0:
                break
            else:
                input("Insira um valor válido!")

main_instance = Main()

class ManipulaTerminal:
    def Limpa(): #Retira todas as mensagens do terminal
        sistema = sys()
        if sistema == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def Cabecalho(usuario): #Cria o cabeçalho de opções iniciais
        print("+----------------------------+")
        print("| 1 = Adicionar Contato      |")
        print("| 2 = Ver Contatos           |")
        print("| 3 = Excluir Contato        |")
        print("| 4 = Pesquisar contato      |")
        print("| 5 = Editar Contato         |")
        print("| 0 = Fechar                 |")
        print("+----------------------------+")

    def CabecalhoAdm():
        print("\n")
        print("+--------------------------------+")
        print("| Opções de administrador        |")
        print("+--------------------------------+") 
        print("| 101 = Adicionar Campo          |")
        print("| 102 = Exclui Campo             |")
        print("| 103 = Mostra Campos Adicionais |")
        print("| 104 = Adicionar ADM a Alguém   |")
        print("+--------------------------------+")
   
    def MostraCamposAdicionais():
        campos_adicionais = ManipulaArqTXT.LeCamposAdicionais()
        campos_obrigatorios = ManipulaArqTXT.LeObrigatorioCamposAdicionais()

        if not campos_adicionais:
            input("Não há campos adicionais listados.")
            return

        print("Campos adicionais:\n")

        for i, campo in enumerate(campos_adicionais):
            obrigatorio = "Sim" if campos_obrigatorios[i] == "1" else "Não"
            print(f"Campo: {campo.capitalize()}\nObrigatório: {obrigatorio}")
            print("-"*65)
    
        input("Pressione Enter para continuar...")


    def CapitalizaTodasPalavras(txt):
        return " ".join([word.capitalize() for word in txt.split()])

    def MostraContatos(contatos): #Mostra ao usuário todos os contatos da lista
        if not contatos:
            input("Não há contatos na lista.")
            return

        campos_contato = set()
        campos_endereco = set()

        for contato in contatos:
            campos_contato.update(contato.keys())
            if "endereco" in contato:
                campos_endereco.update(contato["endereco"].keys())

        campos_contato = ["nome"] + sorted(campos_contato - {"nome"} - {"endereco"}) + ["endereco"]
        campos_endereco = sorted(campos_endereco)

        for contato in contatos:
            ManipulaTerminal.MostraContato(contato)
            print("-" * 65)
            
        input("Pressione Enter para continuar...")
    
    def MostraContato(contato):
        campos = set()

        contatos = ManipulaArqTXT.CriaLista(main_instance.usuario.nome_usuario)

        campos = set()
        campos_endereco = set()
        
        for contato in contatos:
            campos.update(contato.keys())
            campos_endereco.update(contato["endereco"].keys())
        
        campos = ["nome"] + sorted(campos - {"nome", "endereco"}) + ["endereco"]
        campos_endereco = sorted(campos_endereco)

        for campo in campos:
            if campo == "endereco":
                ManipulaTerminal.MostraEndereco(contato[campo])
                continue
            print(f"{campo.capitalize()}: {ManipulaTerminal.CapitalizaTodasPalavras(contato[campo])}")
    
    def MostraEndereco(endereco):
        print("Endereço:")
        for campo in endereco:
            print(f"\t{campo.capitalize()}: {ManipulaTerminal.CapitalizaTodasPalavras(endereco[campo])}")

    def PesquisaContatos(usuario): #Mostra no terminal uma lista contendo os resultados de uma pesquisa realizado pelo usuário
        campo = ""
        contatos = ManipulaArqTXT.CriaLista(usuario)
        campos = set()
        campos_endereco = set()
        resultados = []
        
        for contato in contatos:
            campos.update(contato.keys())
            campos_endereco.update(contato["endereco"].keys())

        print("Campos disponíveis:")
        for i in campos:
            print(f" ° {i}")
        print("-"*25)

        campo = str(input("Digite o campo que quer pesquisar.\n -> ")).lower().strip()

        while campo not in campos:
            print("Digite um campo dentro das opções. Tente de novo.")
            campo = str(input("Digite o campo que quer pesquisar.\n -> ")).lower().strip()


        if campo == "endereco":

            print("Campos de endereço disponíveis:")
            for i in campos_endereco:
                print(f" ° {i}")
            print("-"*25)

            campo2 = str(input("Digite o campo de endereço que quer pesquisar.\n -> ")).lower().strip()

            while campo2 not in campos_endereco:
                print("Digite um campo dentro das opções. Tente de novo.")
                campo2 = str(input("Digite o campo que quer pesquisar.\n -> ")).lower().strip()
    
        pesquisa = str(input("Qual valor quer pesquisar?\n -> "))

        if not campo == "endereco":
            for contato in contatos:
                if pesquisa == contato[campo]:
                    resultados.append(contato)
        else:
            for contato in contatos:
                if pesquisa == contato[campo][campo2]:
                    resultados.append(contato)

        if resultados:
            ManipulaTerminal.MostraContatos(contatos=resultados)
        else:
            input("Nenhum contato correspondente à sua pesquisa.")

class ManipulaArqTXT:
    def Caminho(usuario): #Retorna uma string do caminho do arquivo .txt (contatosv2.txt) que armazena os contatos
        try:
            caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"contatos\{usuario}_contatos.txt")
            return caminho
        except Exception as e:
            input(f"Ocorreu o erro: {e}")

    def CaminhoPastaContatos():
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"contatos")
        return caminho

    def CaminhoConfiguracaoCamposContato():
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_campos.txt")
        return caminho
    
    def CaminhoObrigatorioCamposadicionais():
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_obrigatorio.txt")
        return caminho

    def CaminhoUsuario():
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.txt")
        return caminho

    def TodosContatos():
        caminho = ManipulaArqTXT.CaminhoPastaContatos()
        data = {}
        for arquivo in os.listdir(caminho):
            caminho_arquivo = os.path.join(caminho, arquivo)
            with open(caminho_arquivo, "r", encoding="utf-8") as file:
                conteudo = file.read().strip()
                if conteudo:
                    try:
                        data[caminho_arquivo] = eval(conteudo)
                    except (SyntaxError, NameError):
                        data[caminho_arquivo] = []
                else:
                    data[caminho_arquivo] = []
        return data

    def LeUsuarios():
        caminho = ManipulaArqTXT.CaminhoUsuario()
        try:
            with open(caminho, "r") as file:
                linhas = file.readlines()        
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")            
            return {}
        usuarios = {}
        for linha in linhas:
            nome, senha_hash, salt, tipo_usuario = linha.strip().split("|")
            usuarios[nome] = {"senha_hash": senha_hash, "salt": salt, "tipo_usuario": tipo_usuario}
        return usuarios
            
    def SalvaUsuario(usuario):
        caminho = ManipulaArqTXT.CaminhoUsuario()
        nome, senha_hash, salt, tipo_usuario = usuario
        try:
            with open(caminho, "a") as file:
                file.write(f"{nome}|{senha_hash.hex()}|{salt.hex()}|{tipo_usuario}\n")
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")

    def EscreveUsuarios(usuarios):
        caminho = ManipulaArqTXT.CaminhoUsuario()
        with open(caminho, "w") as file:
            file.write("")
        with open(caminho, "a") as file:
            for usuario in usuarios:
                senha_hash, salt, tipo_usuario = usuarios[usuario].values()
                file.write(f"{usuario}|{senha_hash}|{salt}|{tipo_usuario}\n")

    def LeObrigatorioCamposAdicionais():
        try:
            caminho = ManipulaArqTXT.CaminhoObrigatorioCamposadicionais()
            with open(caminho, "r", encoding="utf-8") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")
            return []
        
    def SalvaObrigatorioCamposAdicionais(valor):
        try:
            caminho = ManipulaArqTXT.CaminhoObrigatorioCamposadicionais()
            with open(caminho, "a", encoding="utf-8") as file:
                file.write(valor + "\n")
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")

    def LeCamposAdicionais():
        try:
            caminho = ManipulaArqTXT.CaminhoConfiguracaoCamposContato()
            with open(caminho, "r", encoding="utf-8") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")
            return []
        
    def SalvaCamposAdicionais(campo):
        try:
            caminho = ManipulaArqTXT.CaminhoConfiguracaoCamposContato()
            with open(caminho, "a", encoding="utf-8") as file:
                file.write(campo + "\n")
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")

    def EscreveCamposAdicionais(data):
        try:
            caminho = ManipulaArqTXT.CaminhoConfiguracaoCamposContato()
            with open(caminho, "w", encoding="utf-8") as file:
                file.write("")
            with open(caminho, "a", encoding="utf-8") as file:
                for campo in data:
                    file.write(campo + "\n")
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")

    def EscreveObrigatorioCamposAdicionais(data):
        try:
            caminho = ManipulaArqTXT.CaminhoObrigatorioCamposadicionais()
            with open(caminho, "w", encoding="utf-8") as file:
                file.write("")
            with open(caminho, "a", encoding="utf-8") as file:
                for campo in data:
                    file.write(campo + "\n")
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")

    def EscreveArquivo(txt, usuario): #Escreve um texto (variável do parâmetro "txt") no arquivo "contatosv2.txt"
        caminho = ManipulaArqTXT.Caminho(usuario)
        with open(caminho, "w", encoding="utf-8") as file:
            file.writelines(txt)
    
    def LeArquivo(usuario): #Retorna o texto contido em "contatosv2.txt"
        caminho = ManipulaArqTXT.Caminho(usuario)
        try:
            with open(caminho, "r", encoding="utf-8") as file:
                arquivo_data = file.read()
            return arquivo_data
        except FileNotFoundError:
            input("Erro: Arquivo não encontrado.")

    def CriaLista(usuario): #Retorna uma lista python de todos os contatos em formato de dicionário
        contatos = []
        try:
            arquivo_data = ManipulaArqTXT.LeArquivo(usuario)
            if arquivo_data:
                contatos = eval(arquivo_data)
        except FileNotFoundError:
            input("Arquivo Não Encontrado!")
        except SyntaxError:
            input("Erro de Sintaxe no Arquivo")
        return contatos

class Endereco:
    def __init__(self, rua="rua", numero_casa="numero", complemento="complemento", cidade="cidade", estado="estado", pais="país") -> None:
        self.rua = rua
        self.numero_casa = numero_casa
        self.complemento = complemento
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
    
    def PerguntaEndereco(self): #Pergunta as informações do endereço de um novo contato ao usuário e armazena nos atributos da classe "Endereco"
        print("Endereço:")
        print("\nOs campos marcados com '*' são obrigatórios.\n")
        
        campos_obrigatorios = {"rua": True, "numero_casa": True, "complemento": False, "cidade": True, "estado": True, "pais": True}

        for campo, obrigatorio in campos_obrigatorios.items():
            valor = Endereco.PerguntaCampo(campo, obrigatorio)

            setattr(self, campo, valor)

    def PerguntaCampo(campo, obrigatorio):
        while True:
            valor = input(f"Qual o valor de '{campo}'? {'*' if obrigatorio else ''}\n -> ").lower().strip()
            if obrigatorio and not valor:
                print(f"O campo '{campo}' é obrigatório. Por favor, preencha.")
                continue
            return valor

    def TransformaDict(self):
        return {
            "rua": self.rua,
            "numero_casa": self.numero_casa,
            "complemento": self.complemento,
            "cidade": self.cidade,
            "estado": self.estado,
            "pais": self.pais,
        }

class Contato:
    campos_adicionais = []
    obrigatorio_adicionais = []

    def __init__(self, nome="nome", numero="número de telefone", anotacao="anotação", endereco=None) -> None:
        if endereco is None:
            endereco = Endereco()
        self.nome = nome
        self.numero = numero
        self.anotacao = anotacao
        self.endereco = endereco
        for campo in Contato.campos_adicionais:
            setattr(self, campo, None)
    
    @classmethod
    def CarregaCampos(cls):
        cls.campos_adicionais = ManipulaArqTXT.LeCamposAdicionais()

    @classmethod
    def CarregaObrigatorio(cls):
        cls.obrigatorio_adicionais = ManipulaArqTXT.LeObrigatorioCamposAdicionais()

    def PerguntaContato(self):
        Contato.CarregaCampos()
        Contato.CarregaObrigatorio()

        print("Novo contato:")
        print("\nOs campos marcados com '*' são obrigatórios.\n")

        nome = input(f"Qual o valor de 'nome'? *\n -> ")

        while not nome:
            print(f"O campo 'nome' é obrigatório. Por favor, preencha.")
            nome = input(f"Qual o valor de 'nome'? *\n -> ")

        while ManipulaLista.EstaNaLista(nome):
            print(f"O nome '{nome}' já está na lista. Por favor, tente de novo.")
            nome = input(f"Qual o valor de 'nome'? *\n -> ")            

        self.nome = nome
        self.numero = self.PerguntaCampo("numero", True)
        self.anotacao = self.PerguntaCampo("anotacao", False)

        for i, campo in enumerate(Contato.campos_adicionais):
            obrigatorio = Contato.obrigatorio_adicionais[i] == "1"
            valor = self.PerguntaCampo(campo, obrigatorio)
            setattr(self, campo, valor)

        self.endereco.PerguntaEndereco()

    @staticmethod
    def PerguntaCampo(campo, obrigatorio):
        while True:
            valor = input(f"Qual o valor de '{campo}'? {'*' if obrigatorio else ''}\n -> ").lower().strip()
            if obrigatorio and not valor:
                print(f"O campo '{campo}' é obrigatório. Por favor, preencha.")
                continue
            return valor

    def TransformaDict(self):
        contato_dict = {
            "nome": self.nome,
            "numero": self.numero,
            "anotacao": self.anotacao,
            "endereco": self.endereco.TransformaDict(),
        }
        for campo in Contato.campos_adicionais:
            contato_dict[campo] = getattr(self, campo, None)
        return contato_dict    

class ManipulaContato:
    contato = Contato()

    @staticmethod
    def CriaContato():
        contato = Contato()
        contato.PerguntaContato()
        return contato.TransformaDict()

    def AdicionaCampoAosContatos(data, campo):
        for arquivo, contatos_usuario in data.items():
            if isinstance(contatos_usuario, list):
                for i in range(len(contatos_usuario)):
                    contatos_usuario[i][campo] = ""

            
            try:
                with open(arquivo, "w", encoding="utf-8") as file:
                    file.write(str(contatos_usuario))
            except Exception as e:
                print(f"Erro ao salvar o arquivo {arquivo}: {e}")

    def AdicionaCampo():
        novo_campo = str(input("Qual o nome do novo campo?\n -> ")).lower().strip()

        contatos = ManipulaArqTXT.TodosContatos()

        if not novo_campo:
            input("O nome do campo não pode ser vazio. Por favor, insira um nome válido.")
            return

        if novo_campo in ManipulaArqTXT.LeCamposAdicionais():
            input(f"O campo '{novo_campo}' já existe nos contatos.")
            return

        while True:
            obrigatorio = str(input(f"O campo '{novo_campo}' é obrigatório? [1 = sim, 0 = não]\n -> ")).strip()
            if obrigatorio in ["1","0"]:
                break
            else:
                print("Por favor, insira '1' para sim ou '0' para não.")

        setattr(Contato, novo_campo, None)

        ManipulaArqTXT.SalvaCamposAdicionais(novo_campo)

        ManipulaArqTXT.SalvaObrigatorioCamposAdicionais(obrigatorio)

        ManipulaContato.AdicionaCampoAosContatos(contatos, novo_campo)

        input(f"O campo {novo_campo} foi adicionado com sucesso.")

    def ExcluiCampo():
        contatos = ManipulaArqTXT.TodosContatos()
        campo_excluir = str(input("Qual o nome do campo que deseja excluir?\n -> ")).lower().strip()

        campos = ManipulaArqTXT.LeCamposAdicionais()
        obrigatorios = ManipulaArqTXT.LeObrigatorioCamposAdicionais()

        certeza = str(input(f"Tem certeza que quer excluir o campo '{campo_excluir}'?\n 1 = sim\n 2 = não\n -> "))

        while certeza not in ["1","2"]:
            print("Insira um valor dentro das opções.")
            certeza = str(input(f"Tem certeza que quer excluir o campo '{campo_excluir}'?\n 1 = sim\n 2 = não\n -> "))

        certeza = certeza == "1"

        if campo_excluir in campos and certeza:
            index = campos.index(campo_excluir)
            campos.pop(index)
            obrigatorios.pop(index)
            ManipulaArqTXT.EscreveCamposAdicionais(campos)
            ManipulaArqTXT.EscreveObrigatorioCamposAdicionais(obrigatorios)
            Contato.CarregaCampos()
            Contato.CarregaObrigatorio()
            ManipulaContato.TiraCampoContatos(contatos, campo_excluir)
            print(f"{campo_excluir.capitalize()} retirado com sucesso.")
        else:
            input(f"{campo_excluir.capitalize()} não encontrado.")

    def TiraCampoContatos(data, campo):
        for arquivo, contatos_usuario in data.items():
            if isinstance(contatos_usuario, list):
                for i in range(len(contatos_usuario)):
                    if isinstance(contatos_usuario[i], dict):
                        contatos_usuario[i].pop(campo, None)

            
            try:
                with open(arquivo, "w", encoding="utf-8") as file:
                    file.write(str(contatos_usuario))
            except Exception as e:
                print(f"Erro ao salvar o arquivo {arquivo}: {e}")

class ManipulaLista:
    def AdicionaContato(usuario): #Adiciona as informações de um novo contato dentro da lista de contatos do arquivo "contatosv2.txt"
        contato = ManipulaContato.CriaContato()

        contatos = ManipulaArqTXT.CriaLista(usuario)

        contatos.append(contato)
        
        ManipulaArqTXT.EscreveArquivo(str(contatos), usuario)

    def ExcluiContato(usuario): #Exclui um contato da lista de contatos e reescreve o arquivo "contatosv2.txt" com a nova lista
        contatos = ManipulaArqTXT.CriaLista(usuario)
        contato_excluir = str(input("Qual o nome do contato que quer excluir?\n -> ")).lower().strip()
        
        existe = False
        for i in range(len(contatos)-1, -1, -1):
            if contatos[i]["nome"] == contato_excluir:
                index = i
                existe = True
                break
        if existe:
            certeza = str(input(f"Tem certeza que quer excluir {ManipulaTerminal.CapitalizaTodasPalavras(contato_excluir)} da lista? [1 = sim, 2 = não]\n -> "))
            if certeza.isdigit():
                certeza = int(certeza)
                if certeza == 2:
                    return
            contatos.pop(index)
            ManipulaArqTXT.EscreveArquivo(str(contatos), usuario)
            input(f"{ManipulaTerminal.CapitalizaTodasPalavras(contato_excluir)} retirado da lista com sucesso.")
        else:
            input(f"{ManipulaTerminal.CapitalizaTodasPalavras(contato_excluir)} não encontrado na lista.")
            
        
    def EstaNaLista(nome):
        contatos = ManipulaArqTXT.CriaLista(main_instance.usuario.nome_usuario)
        return any(contato.get("nome", "").lower() == nome.lower() for contato in contatos)
                

    def EditaContato(usuario):
        contatos = ManipulaArqTXT.CriaLista(usuario)
        contato_editar_nome = input("Qual o nome do contato que quer editar?\n -> ").strip().lower()

        for i, contato in enumerate(contatos):
            if contato.get("nome", "").lower() == contato_editar_nome:
                ManipulaLista.EditaCamposContato(contato)
                contatos[i] = contato
                ManipulaArqTXT.EscreveArquivo(str(contatos), usuario)
                input("Contato atualizado com sucesso.")
                return

        input("Este nome não está na lista. Tente outro.")

    def EditaCamposContato(contato):
        campos_disponiveis = {i + 1: chave for i, chave in enumerate(contato.keys())}

        while True:
            print("Campos disponíveis para edição:")
            for i, chave in campos_disponiveis.items():
                print(f"{i} = {chave.capitalize()}")

            escolha = input("Escolha o campo a ser editado (número):\n -> ").strip()
            if escolha.isdigit() and int(escolha) in campos_disponiveis:
                campo_editar = campos_disponiveis[int(escolha)]
                break
            else:
                input("Insira um valor dentro das opções.")

        if campo_editar == "nome":
            ManipulaLista.EditaNome(contato)
        elif campo_editar == "endereco":
            ManipulaLista.EditaEndereco(contato["endereco"])
        else:
            novo_valor = input(f"Qual o novo valor para '{campo_editar}'?\n -> ").lower().strip()
            contato[campo_editar] = novo_valor

    def EditaNome(contato):
        while True:
            novo_nome = input("Qual o novo nome do contato?\n -> ").strip().lower()
            if not ManipulaLista.EstaNaLista(novo_nome):
                contato["nome"] = novo_nome
                break
            else:
                input("Já existe um contato com este nome. Tente outro.")

    def EditaEndereco(endereco):
        campos_endereco = {i + 1: chave for i, chave in enumerate(endereco.keys())}

        while True:
            print("Campos disponíveis para editar o endereço:")
            for i, chave in campos_endereco.items():
                print(f"{i} = {chave.capitalize()}")

            escolha = input("Escolha o campo do endereço a ser editado (número):\n -> ").strip()
            if escolha.isdigit() and int(escolha) in campos_endereco:
                campo_editar = campos_endereco[int(escolha)]
                break
            else:
                input("Insira um valor dentro das opções.")

        novo_valor = input(f"Qual o novo valor para '{campo_editar}'?\n -> ").strip().lower()
        endereco[campo_editar] = novo_valor

class ManipulaUsuarios:
    def UsuarioExiste(usuario):
        usuarios = ManipulaArqTXT.LeUsuarios()
        return usuario in usuarios

    def CriptografaSenha(senha):
        salt = os.urandom(16)
        senha_bytes = senha.encode("utf-8")
        hash_nome = "sha256"
        iteracoes = 100000
        senha_hash = hashlib.pbkdf2_hmac(hash_nome, senha_bytes, salt, iteracoes)
        return senha_hash, salt

    def VerificaSenha(usuario, senha):
        usuarios = ManipulaArqTXT.LeUsuarios()
        if usuario not in usuarios:
            return False
        
        senha_hash_bd = bytes.fromhex(usuarios[usuario]["senha_hash"])
        salt = bytes.fromhex(usuarios[usuario]["salt"])
        senha_bytes = senha.encode("utf-8")
        hash_nome = "sha256"
        iteracoes = 100000
        senha_hash = hashlib.pbkdf2_hmac(hash_nome, senha_bytes, salt, iteracoes)
        return senha_hash == senha_hash_bd

    def TipoUsuario(usuario):
        usuarios = ManipulaArqTXT.LeUsuarios()
        if usuario in usuarios:
            return usuarios[usuario]["tipo_usuario"]
        return None
    
    def AdicionaAdm():
        usuario = str(input("Qual usuario quer adicionar?\n -> "))
        if not ManipulaUsuarios.UsuarioExiste(usuario=usuario):
            input("Usuário não encontrado.")
            return
        
        usuarios = ManipulaArqTXT.LeUsuarios()
        tipo_usuario = ManipulaUsuarios.TipoUsuario(usuario=usuario)

        if tipo_usuario == "adm":
            input(f"O usuário {usuario} já é um ADM.")
            return

        usuarios[usuario]["tipo_usuario"] = "adm"

        ManipulaArqTXT.EscreveUsuarios(usuarios=usuarios)

class Usuario:
    def __init__(self, nome_usuario=None, tipo_usuario="usuario"):    
        self.nome_usuario = nome_usuario
        self.tipo_usuario = tipo_usuario
        contatos = []
        functions_padrao = {
                1: lambda: ManipulaLista.AdicionaContato(usuario=main_instance.usuario.nome_usuario),
                2: lambda: ManipulaTerminal.MostraContatos(contatos=contatos),
                3: lambda: ManipulaLista.ExcluiContato(usuario=main_instance.usuario.nome_usuario),
                4: lambda: ManipulaTerminal.PesquisaContatos(usuario=main_instance.usuario.nome_usuario),
                5: lambda: ManipulaLista.EditaContato(usuario=main_instance.usuario.nome_usuario),
        }
        
        self.functions = functions_padrao

    def Funcoes(self):
        caminho = ManipulaArqTXT.Caminho(main_instance.usuario.nome_usuario)
        if not os.path.exists(caminho):
            with open(caminho, "w") as file:
                file.write("")
        contatos = ManipulaArqTXT.CriaLista(main_instance.usuario.nome_usuario)    
        if main_instance.usuario.tipo_usuario == "adm":
            functions = {
                101: ManipulaContato.AdicionaCampo,
                102: ManipulaContato.ExcluiCampo,
                103: ManipulaTerminal.MostraCamposAdicionais,
                104: ManipulaUsuarios.AdicionaAdm,
                1: lambda: ManipulaLista.AdicionaContato(usuario=main_instance.usuario.nome_usuario),
                2: lambda: ManipulaTerminal.MostraContatos(contatos=contatos),
                3: lambda: ManipulaLista.ExcluiContato(usuario=main_instance.usuario.nome_usuario),
                4: lambda: ManipulaTerminal.PesquisaContatos(usuario=main_instance.usuario.nome_usuario),
                5: lambda: ManipulaLista.EditaContato(usuario=main_instance.usuario.nome_usuario),
            }
            setattr(self, "functions", functions)
            return functions
        else:
            functions = {
                1: lambda: ManipulaLista.AdicionaContato(main_instance.usuario.nome_usuario),
                2: lambda: ManipulaTerminal.MostraContatos(contatos=contatos),
                3: lambda: ManipulaLista.ExcluiContato(usuario=main_instance.usuario.nome_usuario),
                4: lambda: ManipulaTerminal.PesquisaContatos(usuario=main_instance.usuario.nome_usuario),
                5: lambda: ManipulaLista.EditaContato(usuario=main_instance.usuario.nome_usuario),
            }
            setattr(self, "functions", functions)
            return functions

class Login:
    def PerguntaDados():
        while True:
            nome = str(input("Qual o nome de usuário?\n -> ")).strip().lower()
            if not nome:
                print(f"O nome de usuário não pode estar em branco. Tente novamente.")
            elif ManipulaUsuarios.UsuarioExiste(nome):
                break
            else:
                print(f"O usuário {ManipulaTerminal.CapitalizaTodasPalavras(nome)} não existe no banco de dados. Tente outro.")
        while True:
            senha = str(input("Qual a senha?\n -> ")).strip()
            if senha:
                break
            else:
                input("A senha não pode estar em branco. Tente novamente.")

        return nome, senha

    def LoginUsuario(nome, senha):
        if ManipulaUsuarios.UsuarioExiste(nome) and ManipulaUsuarios.VerificaSenha(nome, senha):
            tipo_usuario = ManipulaUsuarios.TipoUsuario(nome)
            setattr(main_instance.usuario, "tipo_usuario", tipo_usuario)
            setattr(main_instance.usuario, "nome_usuario", nome)
            return True, "Sucesso no login."
        if not ManipulaUsuarios.UsuarioExiste(nome):
            return False, f"O usuário {nome} não existe no banco de dados."
        elif not ManipulaUsuarios.VerificaSenha(nome, senha):
            return False, "A senha não corresponde à do usuário digitado."
        

class SignIn():
    def CadastraUsuario():
        while True:
            nome = str(input("Qual o nome de usuário?\n -> ")).strip().lower()
            if not nome:
                print(f"O nome de usuário não pode estar em branco. Tente novamente.")
            elif ManipulaUsuarios.UsuarioExiste(nome):
                print(f"O usuário {ManipulaTerminal.CapitalizaTodasPalavras(nome)} já existe. Tente outro.")
            else:
                break
        while True:
            senha = str(input("Qual a senha?\n -> ")).strip()
            if senha:
                break
            else:
                input("A senha não pode estar em branco. Tente novamente.")

        senha_hash, salt = ManipulaUsuarios.CriptografaSenha(senha)
        
        ManipulaArqTXT.SalvaUsuario((nome, senha_hash, salt, "usuario"))
        logou, motivo = Login.LoginUsuario(nome, senha)
        if not logou:
            print(motivo)
        caminho = ManipulaArqTXT.Caminho(nome)
        with open(caminho, "w") as file:
            file.write("")

main_instance.CriaUsuario()
main_instance.main()
