from datetime import datetime, date
import random
from tkinter import filedialog
import tkinter as tk 


'''
PROGRAMA DE SORTEIO PARA A ESEBA

O programa deve receber um arquivo em formato CSV com separador sendo o caractere ";"
A tabela do CSV deve conter, nesta ordem:
- Numero identificador, o atributo chave. Um número único que identifique o candidato.
- Nome do estudante
- Número de irmãos gêmeos do estudante (0 em caso não tenha, o número de irmãos gêmeos caso tenha)
- Data de mascimento do candidato no formato DD/MM/AAAA
- Se o candidato é ou não PCD - se for, valor 1; se não for, valor 0
- O ano letivo para o qual o candidato está se candidatando, no formato "2º período"; "1º ano"...
- O número referente à cota para a qual o candidato se inscreveu
- O número do CPF do responsável

Todos os comandos PRINT podem ser ignorados, eles servem apenas para guiar e mostrar para a direção e a secretaria
sobre como as coisas estão implementadas.

Busquei utilizar Python para ficar mais fácil a leitura para outra pessoa que fosse mexer.

Tentei utilizar PyScript para montar uma interface que fosse mais amigável para o pessoal da escola, mas não consegui
fazer funcionar. Passo o bastão para você.

Dúvidas e no que eu puder ajudar, pode me chamar. maxpziller@gmail.com
'''

#Classe que recebe os dados de um candidato único
class Candidato:
    def __init__(self, id, nome, gemeo, nascimento, pcd, ano, cota, cpf_responsavel):
        self.id = id
        self.nome = nome
        self.gemeo = gemeo
        data = datetime.strptime(nascimento,"%d/%m/%Y")
        self.nascimento = data.strftime("%d/%m/%Y")
        self.pcd = pcd
        self.ano = ano
        self.cota = cota
        self.cpf_responsavel = cpf_responsavel

    def Imprime(self):
        print(str(self.id)+" - "+ (self.nome))


#Adicionar valor de texto para o nome de cada cota
class Vaga:
    def __init__(self, ano, cota, quantidade):
        self.ano = ano
        self.cota = cota
        self.quantidade = quantidade
        self.selecionados = []
        self.lista_candidatos = []

    def Adiciona_candidato(self, novo):
        self.lista_candidatos.append(novo)
        return True

    def Imprime_candidatos(self):
        print("\n"+str(self.ano)+" - Cota "+str(self.cota))
        print("Total de "+str( len(self.lista_candidatos))+" candidatos para "+str(self.quantidade)+" vagas.\n")
        for candidato in self.lista_candidatos:
            candidato.Imprime()
        print("------------------")

    def Imprime_selecionados(self):
        print("\n"+str(self.ano)+" - Cota "+str(self.cota))
        print("Total de "+str( len(self.lista_candidatos))+" candidatos para "+str(self.quantidade)+" vagas.\n")
        for candidato in self.selecionados:
            candidato.Imprime()
        print("------------------")

    def Recebe_vagas(self,quantidade):
        self.quantidade += quantidade

    def Sobra_vagas(self):
        qtdd_candidatos = len(self.lista_candidatos)
        sobra = self.quantidade - qtdd_candidatos
        if (sobra < 0):
            return 0
        else:
            return sobra

    def Retira_candidato(self,candidato):
        self.lista_candidatos.remove(candidato)

    def Realiza_sorteio(self,semente):
        random.seed(semente)
        if ( len(self.lista_candidatos) < self.quantidade ):
            self.selecionados = random.sample(self.lista_candidatos,len(self.lista_candidatos))
        else:
            for i in range(self.quantidade):
                sorteado = self.lista_candidatos.pop( random.randrange(len(self.lista_candidatos)) )
                self.selecionados.append(sorteado)

'''
Classe Sorteio
possui como atributo inicial a data

atributos:
- data: valor inteiro. Ano letivo para o qual o sorteio acontecerá.
- arvore: Uma estrutura de dados em árvore para lidar com a herança de vagas não preenchidas de acordo com resolução
- vagas: Dicionário. O dicionário tem duas chaves, sendo elas o ano de inscrição em valor string e o número da cota.
    O valor apontado pelo dicionário é um obeto Vaga. A importância do objeto Vaga é guardar as listas de candidatura
    de forma ordenada e separar os selecionados pelo mesmo tipo.
    EXEMPLO: vagas["1º Período",2] = CLASS VAGA

- anos_com_cota e anos_sem_cota: Estabelecem em que anos que se aplica a divisão das vagas em cotas e em quais não.
    ATENÇÃO, pois a cada ano as listas anos_com_cota e anos_sem_cota devem ser revistas.
    Em caso de mudança das normas, como a mudança da quantidade de vagas de alguma cota, esta função deve ser alterada

'''
class Sorteio:
    def __init__(self, data, semente):
        self.data = data

        print("\nSelecione o arquivo com os dados dos candidatos inscritos.\n")

        self.anos_com_cota = ["2º período","1º ano","2º ano","3º ano","4º ano"]
        self.anos_sem_cota = ["5º ano","6º ano","7º ano","8º ano","9º ano"]

        #Inicia o procedimento para escolha do arquivo fonte das inscrições
        root = tk.Tk()
        root.withdraw()

        # Make it almost invisible - no decorations, 0 size, top left corner.
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        # Show window again and lift it to top so it can get focus,
        # otherwise dialogs will end up behind the terminal.
        root.deiconify()
        root.lift()
        root.focus_force()
        
        file_path = filedialog.askopenfilename()

        self.semente = int(semente)

        #Chama a leitura do documento e monta os objetos do sorteio dentro de
        self.Ler_documento(file_path)
        root.destroy()

        return

    #Função que recebe o documento indicado pelo usuário e transforma as informações em objetos manipuláveis
    def Ler_documento(self, endereco_arquivo):

        #Organiza o objeto com as vagas de acordo com o edital
        self.Prepara_vagas("padrao")

        #Quebra cada linha do arquivo em uma lista para a criação de uma instância da classe Candidato por linha
        linhas = []
        with open (endereco_arquivo) as arquivo:
            for linha in arquivo:
                cand = linha.strip().split(";")
                
                candidato = Candidato(cand[0],cand[1],cand[2],cand[3],cand[4],cand[5].lower(),cand[6],cand[7])
                self.vagas[cand[5].lower(),int(cand[6])].Adiciona_candidato(candidato)

        return True



    '''
    Função que salva no objeto a quantidade de pessoas a serem sorteadas para cada cota de cada ano.
    A função foi feita de forma a existir um padrão preestabelecido de acordo com as normas de quando o projeto
    foi desenvolvido, em 2023. As cotas, como avançam um ano de cada vez progressivamente, ainda não estão em
    todos os sorteios.

    A função foi criada com um condicional para facilitar o manuseio em caso de necessidade de realizar um sorteio
    personalizado, fora dos padrões das normas. Pode-se simplesmente adicionar um "elif" e colocar o novo código.

    O objeto Vaga guardará as listas dos candidatos selecionados e não-selecionados para cada tipo de vaga'''

    def Prepara_vagas(self,modo):
        dicionario = dict()
        if ( modo == "padrao" ):
            nova = Vaga("1º período",1,8)
            dicionario["1º período",1] = nova
            nova = Vaga("1º período",2,8)
            dicionario["1º período",2] = nova
            nova = Vaga("1º período",3,8)
            dicionario["1º período",3] = nova
            nova = Vaga("1º período",4,2)
            dicionario["1º período",4] = nova
            nova = Vaga("1º período",5,2)
            dicionario["1º período",5] = nova
            nova = Vaga("1º período",6,2)
            dicionario["1º período",6] = nova
            nova = Vaga("1º período",7,30)
            dicionario["1º período",7] = nova
            
            

            for ano in self.anos_com_cota:
                for i in range(1,8):
                    nova = Vaga(ano,i,10)
                    dicionario[ano,i] = nova
            for ano in self.anos_sem_cota:
                for i in range(1,3):
                    nova = Vaga(ano,i,10)
                    dicionario[ano,i] = nova
            self.vagas = dicionario
            return True
        else:
            print("\nERRO: Formatação da quantidade de vagas não identificada.\n")
            return False
    

    def Imprime_candidatos(self):
        for vaga in self.vagas:
            self.vagas[vaga].Imprime_candidatos()


    #DAR UM JEITO DESSA SEMENTE DAR CERTO CARALHO
    def Realiza_sorteio(self):

        print("SEMENTE: "+str(self.semente))
        lista = self.anos_com_cota

        '''
        Primeiro período e separado pois deve ter todas as heranças das cotas
        '''

        ano = "1º período"
        arvore_cotas = Arvore()
        arvore_cotas.Arvore_cotas("comcotas")
        ordem = arvore_cotas.Lista_folha_para_raiz()
        ampla = ordem[-1]
        ordem = ordem[:-1]

        '''Primeiro deve ser feito o sorteio da Ampla Concorrência com todos no sorteio'''
        vaga_ampla = self.vagas[ano,ampla]
        tamanho_ampla = len(vaga_ampla.lista_candidatos)
        for cota in ordem:
            vaga = self.vagas[ano,cota]
            for cand in vaga.lista_candidatos:
                vaga_ampla.Adiciona_candidato(cand)
        vaga_ampla.Realiza_sorteio(self.semente)
        for aluno in vaga_ampla.selecionados:
            for cota in ordem:
                if aluno in self.vagas[ano,cota].selecionados:
                    self.vagas[ano,cota].Retira_candidato(aluno)
                    print("Candidato "+aluno.nome+" da cota "+str(cota)+" sorteado na ampla concorrência.")
                    break
        

        '''Depois, o sorteio das outras cotas'''

        for cota in ordem:
            vaga = self.vagas[ano,cota]

            sobra = vaga.Sobra_vagas()
            pai = arvore_cotas.Localiza_pai(cota)
            self.vagas[ano,pai].Recebe_vagas(sobra)
                
            vaga.Realiza_sorteio(self.semente)
                
        ordem.sort()
        for cota in ordem:
            vaga = self.vagas[ano,cota]
            vaga.Imprime_selecionados()
        print("Originalmente há "+str(tamanho_ampla)+" candidatos na ampla concorrência.")
        vaga_ampla.Imprime_selecionados()

        '''
        Agora é feito o sorteio do segundo período até o próximo ano que tenha as cotas
        '''
        ordem = arvore_cotas.Lista_folha_para_raiz()
        ordem.sort()
        for ano in lista:
            arvore_cotas = Arvore()
            arvore_cotas.Arvore_cotas("comcotas")
            ordem = arvore_cotas.Lista_folha_para_raiz()
            ordem.sort()

            for cota in ordem:
                vaga = self.vagas[ano,cota]
                vaga.Realiza_sorteio(self.semente)
                vaga.Imprime_selecionados()
                

        '''
        Agora é feito o sorteio do segundo período até o próximo ano que NÃO tenha as cotas
        '''

        lista = self.anos_sem_cota
        
        for ano in lista:
            arvore_cotas = Arvore()
            arvore_cotas.Arvore_cotas("semcotas")
            ordem = arvore_cotas.Lista_folha_para_raiz()
            ordem.sort()

            for cota in ordem:
                vaga = self.vagas[ano,cota]
                vaga.Realiza_sorteio(self.semente)
                vaga.Imprime_selecionados()


'''
Classes No e Arvore criadas para facilitar programação da herança das cotas
Ela foi feita para que qualquer mudança na normativa das cotas seja facilmente implementada
A classe No contém os seguintes atributos:
- valor: Valor, geralmente inteiro, dado para caracterizar cada cota
- pai: Instância de outro objeto No, usado para apontar o nó acima. Caso o nó seja a raiz, o valor é None
- filhos: Lista, inicialmente vazia, que recebe todos os Nós que são filhos deste Nó
'''
class No:
    def __init__(self,valor,pai):
        self.valor = valor
        self.pai = pai
        self.filhos = []

    def Adiciona_filho(self,no_filho):
        self.filhos.append(no_filho)
        return True

    def Valores_filhos(self):
        lista = []
        for filho in self.filhos:
            lista.append(filho.valor)
        return lista


class Arvore:
    def __init__(self):
        self.dicionario_nos = dict()
        self.raiz = None

    '''
    Função que cria um novo objeto No, e o liga ao nó pai de forma duplamente encadeada, ou seja
    tanto há vínculo do filho com o pai através do atribulo "pai" do objeto No
    quanto liga o pai com o filho através do atribulo "filhos" do objeto No
    '''
    def Adiciona_no(self,valor,pai):
        if (valor in self.dicionario_nos.keys()):
            return None
        else:
            if (pai == None):
                novo = No(valor, None)
                self.raiz = novo
            else:
                no_pai = self.dicionario_nos[pai]
                novo = No(valor,no_pai)
                no_pai.Adiciona_filho(novo)
            self.dicionario_nos[valor] = novo
            return novo

    '''
    Função que retorna, caso o Nó exista na árvore, o objeto Nó a partir do valor
    '''
    def Localiza_no(self,valor):
        if (valor in self.dicionario_nos.keys()):
            return self.dicionario_nos[valor]
        else:
            return None

    def Localiza_pai(self,valor):
        filho = self.Localiza_no(valor)
        if (filho.pai == None):
            return None
        else:
            return filho.pai.valor


    '''
    Função que returna uma lista com todos os nós
    Os nós são organizados de forma às folhas estarem sempre á frente dos seus nós-pai, sendo uma ordem segura para seguir os sorteios
    e as heranças de vaga.
    '''
    def Lista_folha_para_raiz(self):
        lista = []
        inicio = self.raiz.valor
        avisitar = [inicio]
        while (( len(lista) < len(self.dicionario_nos.keys() ) ) and (len(avisitar) > 0) ):
            visita = avisitar.pop(0)
            avisitar += self.dicionario_nos[visita].Valores_filhos()
            lista.insert(0,visita)
        return lista
    

    '''
    Montagem da árvore de acordo com a normativa
    Uma vaga não ocupada em uma cota (folha) será transferida para o Nó Pai
    As cotas vêm numeradas para sua identificação. Caso haja alteração nas cotas, as turmas que ainda existem deverão continuar com o modelo de cotas de quando as turmas foram montadas
    nos seus primeiros períodos. Um novo modo deve ser feito para as novas turmas com formato de cotas diferentes.
    '''
    def Arvore_cotas(self,modo):
        if (modo == "comcotas"):
            self.Adiciona_no(7,None)
            self.Adiciona_no(1,7)
            self.Adiciona_no(3,7)
            self.Adiciona_no(2,3)
            self.Adiciona_no(6,7)
            self.Adiciona_no(4,6)
            self.Adiciona_no(5,6)
        elif (modo == "semcotas"):
            self.Adiciona_no(1,None)
            self.Adiciona_no(2,1)


#Cria o objeto Sorteio2024 como um objeto da classe Sorteio e a inicializa
aleatorio = input("Deseja utilizar de semente pré-estabelecida? Digite S para sim ou N para não.")
while( (aleatorio != 'S') and (aleatorio != 'N')):
    aleatorio = input("Digite uma entrada válida. S para sim ou N para não.")
if (aleatorio == 'S'):
    semente = input("Digite o valor numérico da semente")
else:
    semente = random.randint(0,1048576)
Sorteio2024 = Sorteio(2024,semente)
Sorteio2024.Realiza_sorteio()
    


