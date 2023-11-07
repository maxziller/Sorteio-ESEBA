from datetime import datetime, date
import random
from tkinter as Tk import tk

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

    def Realiza_sorteio(self,semente):
        qtdd_candidatos = len(self.lista_candidatos)
        if ( qtdd_candidatos < self.quantidade ):
            random.seed(semente)
            self.selecionados = random.sample(self.lista_candidatos,qtdd_candidatos)
        else:
            for i in range(self.quantidade):
                random.seed(semente)
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
        file_path = filedialog.askopenfilename()

        self.semente = int(semente)

        #Chama a leitura do documento e monta os objetos do sorteio dentro de
        self.Ler_documento(file_path)
               

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


    #def Realiza_sorteio(self):
        

    def Imprime_candidatos(self):
        for vaga in self.vagas:
            self.vagas[vaga].Imprime_candidatos()


    #DAR UM JEITO DESSA SEMENTE DAR CERTO CARALHO
    def Realiza_sorteio(self):

        print("SEMENTE: "+str(self.semente))
        lista = self.anos_com_cota
        lista.insert(0,"1º período")
        for ano in lista:
            arvore_cotas = Arvore()
            arvore_cotas.Arvore_cotas("comcotas")
            ordem = arvore_cotas.Lista_folha_para_raiz()
            for cota in ordem:
                vaga = self.vagas[ano,cota]
                vaga.Realiza_sorteio(self.semente)
                x = vaga.quantidade - len(vaga.selecionados)
                heranca = arvore_cotas.Localiza_pai(cota)
                if (heranca):
                    self.vagas[ano,heranca].quantidade += x
            ordem.sort()
            for cota in ordem:
                
                self.vagas[ano,cota].Imprime_selecionados()

        for ano in self.anos_sem_cota:
            arvore_cotas = Arvore()
            arvore_cotas.Arvore_cotas("semcotas")
            ordem = arvore_cotas.Lista_folha_para_raiz()
            for cota in ordem:
                vaga = self.vagas[ano,cota]
                vaga.Realiza_sorteio(self.semente)
                x = vaga.quantidade - len(vaga.selecionados)
                heranca = arvore_cotas.Localiza_pai(cota)
                if (heranca):
                    self.vagas[ano,heranca].quantidade += x
            ordem.sort()
            for cota in ordem:
                
                self.vagas[ano,cota].Imprime_selecionados()


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
    


