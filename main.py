import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
import openpyxl
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from tkcalendar import DateEntry
import sys

############# CRIANDO O DATA BASE ###############
conexao = sqlite3.connect('banco_clientes.db')
c = conexao.cursor()
c.execute('''CREATE TABLE if not exists clientes (OS integer primary key autoincrement, Nome text, DataCad date, Logradouro text, Nº numeric, Bairro text, Cidade text, Estado text, Email text, Telefone numeric, DescriProd text, Modelo text, Defeito text, DataEntrega date)''')
conexao.commit()
conexao.close()
############# LISTA DE ESTADOS PARA COMBOBOX ###############
lista_estados = ['Acre (AC)', 'Alagoas (AL)', 'Amapá (AP)', 'Amazonas (AM)', 'Bahia (BA)', 'Ceará (CE)',
                 'Distrito Federal (DF)', 'Espírito Santo (ES)', 'Goiás (GO)', 'Maranhão (MA)', 'Mato Grosso (MT)',
                 'Mato Grosso do Sul (MS)', 'Minas Gerais (MG)', 'Pará (PA)', 'Paraíba (PB)', 'Paraná (PR)',
                 'Pernambuco (PE)', 'Piauí (PI)', 'Rio de Janeiro (RJ)', 'Rio Grande do Norte (RN)',
                 'Rio Grande do Sul (RS)', 'Rondônia (RO)', 'Roraima (RR)', 'Santa Catarina (SC)', 'São Paulo (SP)',
                 'Sergipe (SE)', 'Tocantins (TO)']
############# ABRINDO A JANELA DO APP ###############
window = tk.Tk()
############# IMAGENS E ICONES DO APP ###############
window.iconphoto(False, tk.PhotoImage(file="images\\icon\\logo3.png"))
imagem = tk.PhotoImage(file="images\\logo\\logoindro.png")
############# FUNÇÃO PARA INSERIR OS DADOS NO BANCO DE DADOS ###############
def inserir_dados():
    if entry_nome.get() == '' or cal.get() == '' or entry_email.get() == '' or entry_tel.get() == '' or \
       entry_descriprod.get() == '' or entry_defeito.get('1.0','end') == '' or entry_os.get() == '':
        messagebox.showwarning(title='Error', message='Digite alguns dados do cliente para cadastrar!')
        return

    conexao = sqlite3.connect('banco_clientes.db')
    c = conexao.cursor()
    c.execute('INSERT INTO clientes VALUES (:OS, :Nome, :DataCad, :Logradouro,:Nº, :Bairro, :Cidade, :Estado, :Email, :Telefone, :DescriProd, :Modelo, :Defeito, :DataEntrega)',
        {
            'OS':entry_os.get(),
            'Nome':entry_nome.get(),
            'DataCad':cal.get(),
            'Logradouro':entry_logradouro.get(),
            'Nº':entry_num.get(),
            'Bairro':entry_bairro.get(),
            'Cidade':entry_cidade.get(),
            'Estado':combobox_estado.get(),
            'Email':entry_email.get(),
            'Telefone':entry_tel.get(),
            'DescriProd':entry_descriprod.get(),
            'Modelo':entry_modelo.get(),
            'Defeito':entry_defeito.get('1.0', 'end'),
            'DataEntrega':calEntrega.get()

        }
    )
    if entry_nome.get() != '' or cal.get() != '' or entry_email.get() != '' or entry_tel.get() != '' or entry_descriprod.get() != '' or entry_defeito.get('1.0', 'end') != '' or entry_os.get() != '':
        messagebox.showinfo(title='Concluído', message='Cliente cadastrado com sucesso!')
    conexao.commit()
    conexao.close()

    entry_os.delete(0, 'end')
    entry_nome.delete(0, 'end')
    cal.delete(0, 'end')
    entry_logradouro.delete(0, 'end')
    entry_num.delete(0,'end')
    entry_bairro.delete(0, 'end')
    entry_cidade.delete(0, 'end')
    combobox_estado.delete(0, 'end')
    entry_email.delete(0, 'end')
    entry_tel.delete(0,'end')
    entry_descriprod.delete(0, 'end')
    entry_defeito.delete('1.0', 'end')
    entry_modelo.delete(0, 'end')
    calEntrega.delete(0, 'end')
############# CONEXÃO COM O BANCO DE DADOS COM O SELECT ###############
def conexao_bancoApp():
    conexao = sqlite3.connect('banco_clientes.db')
    vc= conexao.cursor()
    vc.execute('SELECT * FROM clientes')
    res=vc.fetchall()
    vc.close()
    return res
############# FUNÇÃO PARA POPULAR O BANCO DE DADOS PARA O TREEVIEW ###############
def popular_banco():
    tv.delete(*tv.get_children())
    linhas=conexao_bancoApp()
    for i in linhas:
        tv.insert('', 'end', values=i)
############# FUNÇÃO PARA BUSCA PELA OS NO BANCO DE DADOS ###############
def conexao_bancoPesquisa():
    conexao = sqlite3.connect('banco_clientes.db')
    vc = conexao.cursor()
    vc.execute(f'SELECT * FROM clientes WHERE OS LIKE "%{entry_pesquisa.get()}%" OR Nome LIKE "%{entry_pesquisa.get()}%"')
    res=vc.fetchall()
    vc.close()
    return res
############# FUNÇÃO PARA DELETAR DADOS DO CLIENTE ESPECÍFICO ###############
def deletar():
    try:
        id = -1
        itemSelecionado = tv.selection()[0]
        valores_item = tv.item(itemSelecionado, 'values')
        id = valores_item[0]

        conexao = sqlite3.connect('banco_clientes.db')
        vc = conexao.cursor()
        vc.execute(f'DELETE FROM clientes WHERE OS = "{id}"')
        conexao.commit()
        conexao.close()
    except:
        messagebox.showerror(title='Erro ao deletar', message='Selecione um item para excluir.')
        return
    tv.delete((itemSelecionado))
############# FUNÇÃO DE PESQUISA PELO TREEVIEW ###############
def pesquisar():
    tv.delete(*tv.get_children())
    linhas=conexao_bancoPesquisa()
    for i in linhas:
        tv.insert('','end',values=i)
    entry_pesquisa.delete(0, 'end')
############# FUNÇÃO PARA EXPORTAR OS DADOS DA DATA BASE PARA EXCEL ###############
def exportar_dados():
    conexao = sqlite3.connect('banco_clientes.db')
    c = conexao.cursor()
    c.execute('SELECT *, oid FROM  clientes')
    clientes_cadastrados = c.fetchall()
    clientes_cadastrados = pd.DataFrame(clientes_cadastrados, columns=[
        'OS',
        'Nome',
        'DataCad',
        'Logradouro',
        'Nº',
        'Bairro',
        'Cidade',
        'Estado',
        'Email',
        'Telefone',
        'DescriProd',
        'Modelo',
        'Defeito',
        'DataEntrega',
        'ID Banco'

    ])
    clientes_cadastrados.to_excel('banco_de_clientes.xlsx')
    conexao.commit()
    conexao.close()
    if conexao != True:
        messagebox.showinfo(title='Banco exportado', message='Banco de dados exportado com sucesso!')

############# TITULO DA JANELA DO APP ###############
window.title('Cadastro de Clientes')
############# TAMANHO DA JANELA DO APP ###############
window.geometry('1520x800+400+153')
window.resizable(width=0, height=0)
# window.resizable(0, 0)
############# CRIANDO UMA NOVA ABA NO APP ###############
nb= ttk.Notebook(window)
nb.place(x=0, y=0, width=1520, height=800)
############# ABA TB1 PRIMEIRA ABA ###############
tb1=Frame(nb)
nb.add(tb1, text='Cadastro')
############# ABA TB2 SEGUNDA ABA ###############
tb2=Frame(nb)
nb.add(tb2, text='Clientes cadastrados')
############# CRIANDO LABEL PARA LOGO DA LOJA ###############
label_imagem = tk.Label(tb1, image=imagem)
label_imagem.place(x=450, y=5)
############# CRIANDO LABELS FRAMES PARA ENCAIXAR OS DADOS DENTRO DE UMA FRAME SÓ ###############
dadosPessoais = LabelFrame(tb1, text='  Dados pessoais  ', font='Arial 12 bold')
dadosPessoais.place(x=150, y=70, width=480, height=260)
############# CRIANDO LABELS FRAMES PARA ENCAIXAR OS DADOS DENTRO DE UMA FRAME SÓ ###############
dadosProdutos = LabelFrame(tb1, text='  Dados do produto  ', font='Arial 12 bold')
dadosProdutos.place(x=830, y=70, width=500, height=260)
############# CRIANDO LABEL FRAME PARA COLOCAR OS BOTÕES ###############
botoes = LabelFrame(tb1, relief='flat')
botoes.place(x=430, y=380, width=600, height=150)

############## ONDE PREENCHER O APP ###############
##### LABEL NOME #####
label_nome = tk.Label(dadosPessoais, text='Nome Completo:', font='Arial 12')
label_nome.place(x=5, y=15)
entry_nome = tk.Entry(dadosPessoais, font='Arial 12', relief='solid')
entry_nome.place(x=130, y=15, width=280, height=20)
entry_nome.focus()
##### LABEL DATA DE CADASTRO #####
label_datacad = tk.Label(dadosPessoais, text='Data de Cadastro:', font='Arial 12')
label_datacad.place(x=5, y=40)
cal = DateEntry(dadosPessoais, selectmode='day', locale='pt', font='Arial 12', relief='solid')
cal.place(x=143, y=40, width=110, height=20)
##### LABEL LOGRADOURO #####
label_logradouro = tk.Label(dadosPessoais,text='Logradouro:',font='Arial 12')
label_logradouro.place(x=5, y=65)
entry_logradouro = tk.Entry(dadosPessoais, font='Arial 12', relief='solid')
entry_logradouro.place(x=98, y=65, width=280, height=20)
##### LABEL NUMERO DA CASA #####
label_num = tk.Label(dadosPessoais, text='Nº:', font='Arial 12')
label_num.place(x= 390, y=65)
entry_num = tk.Entry(dadosPessoais, font='Arial 12', relief='solid')
entry_num.place(x=417, y=65, width=50, height=20)
##### LABEL BAIRRO #####
label_bairro = tk.Label(dadosPessoais, text='Bairro:', font='Arial 12')
label_bairro.place(x=5, y=90)
entry_bairro = tk.Entry(dadosPessoais, font='Arial 12', relief='solid')
entry_bairro.place(x=60, y=90, width=170, height=20)
##### LABEL CIDADE #####
label_cidade = tk.Label(dadosPessoais, text='Cidade:',font='Arial 12')
label_cidade.place(x=5, y=115)
entry_cidade = tk.Entry(dadosPessoais, font='Arial 12', relief='solid')
entry_cidade.place(x=70, y=115, width=170, height=20)
##### LABEL ESTADO #####
label_estado = tk.Label(dadosPessoais, text='Estado:', font='Arial 12')
label_estado.place(x=5, y=140)
combobox_estado = ttk.Combobox(dadosPessoais,values=lista_estados, font='Arial 12')
combobox_estado.place(x=67, y=140, width=180, height=20)
##### LABEL EMAIL #####
label_email = tk.Label(dadosPessoais, text='E-mail:', font='Arial 12')
label_email.place(x=5, y=165)
entry_email = tk.Entry(dadosPessoais, relief='solid', font='Arial 12')
entry_email.place(x=65, y=165, width=260, height=20)
##### LABEL TELEFONE #####
label_tel = tk.Label(dadosPessoais, text='Telefone:', font='Arial 12')
label_tel.place(x=5, y=190)
entry_tel = tk.Entry (dadosPessoais, font='Arial 12', relief='solid')
entry_tel.place(x=78, y=190, height=20)
##### LABEL DESCRIÇÃO DO PRODUTO/EQUIPAMENTO #####
label_descriprod = tk.Label(dadosProdutos, text='Descrição do produto:', font='Arial 12')
label_descriprod.place(x=5, y=15)
entry_descriprod =tk.Entry(dadosProdutos, font='Arial 12', relief='solid')
entry_descriprod.place(x=167, y=15, width=300, height=20)
##### LABEL MODELO DO PRODUTO/EQUIPAMENTO #####
label_modelo = tk.Label(dadosProdutos, text='Modelo:',font='Arial 12')
label_modelo.place(x=5, y=40)
entry_modelo = tk.Entry(dadosProdutos, font='Arial 12', relief='solid')
entry_modelo.place(x=67, y=40, height=20)
##### LABEL DEFEITO APRESENTADO #####
label_defeito = tk.Label(dadosProdutos, text='Descrição do defeito:', font='Arial 12')
label_defeito.place(x=5, y=65)
entry_defeito = tk.Text(dadosProdutos, font='Arial 12', relief='solid')
entry_defeito.place(x=162, y=65, width=300, height=70)
##### LABEL DATA DA ENTREGA #####
label_entrega = tk.Label(dadosProdutos, text='Prazo para entrega:', font='Arial 12')
label_entrega.place(x=5, y=150)
calEntrega = DateEntry(dadosProdutos, selectmode='day', locale='pt', font='Arial 12', relief='solid')
calEntrega.place(x=151, y=151, width=110, height=20)
##### LABEL OS  #####
label_os = tk.Label(dadosProdutos, text='OS', font='Arial 12')
label_os.pack(side='bottom')
entry_os = tk.Entry(dadosProdutos, font='Arial 12', relief='solid', justify='center')
entry_os.pack(side='bottom')
############# CRIANDO SCROLLBAR PARA O TREEVIEW ############
tv_frame = Frame(tb2)
tv_frame.pack(pady=20)
scroll_tv = tk.Scrollbar(tv_frame)
scroll_tv.pack(side=RIGHT, fill=Y)
############# CRIANDO O TREEVIEW ############
tv = ttk.Treeview(tv_frame,columns=('os', 'nome', 'datacad', 'logradouro', 'n', 'bairro', 'cidade', 'estado', 'email', 'telefone', 'descriprod', 'modelo', 'defeito', 'dataentrega'), show='headings', height=30, selectmode='browse', yscrollcommand=scroll_tv.set)
scroll_tv.config(command=tv.yview)
tv.pack()
tv.column('os', minwidth=0, width=40)
tv.column('nome', minwidth=0, width=155)
tv.column('datacad', minwidth=0, width=72)
tv.column('logradouro', minwidth=0, width=140)
tv.column('n', minwidth=0, width=50)
tv.column('bairro', minwidth=0, width=95)
tv.column('cidade' ,minwidth=0, width=100)
tv.column('estado', minwidth=0, width=80)
tv.column('email', minwidth=0, width=140)
tv.column('telefone', minwidth=0, width=85)
tv.column('descriprod', minwidth=0, width=130)
tv.column('modelo', minwidth=0, width=80)
tv.column('defeito', minwidth=0, width=250)
tv.column('dataentrega', minwidth=0, width=72)
tv.heading('os', text='OS')
tv.heading('nome', text='NOME')
tv.heading('datacad', text='DATACAD')
tv.heading('logradouro', text='LOGRADOURO')
tv.heading('n', text='Nº')
tv.heading('bairro', text='BAIRRO')
tv.heading('cidade', text='CIDADE')
tv.heading('estado', text='ESTADO')
tv.heading('email', text='EMAIL')
tv.heading('telefone', text='TELEFONE')
tv.heading('descriprod', text='DESCRIPROD')
tv.heading('modelo', text='MODELO')
tv.heading('defeito', text='DEFEITO')
tv.heading('dataentrega', text='DATAENTREGA')
############# CHAMANDO A FUNÇÃO PARA POPULAR OS DADOS DO BANCO DE DADOS PARA A ABA DO TREEVIEW ############
popular_banco()
############# BOTÕES ATUALIZAR, DELETAR E COPIAR DADOS DOS CLIENTES ############
botao_atualizarbanco = tk.Button(tb2, text='Atualizar', font='Arial 10', relief='flat', command=popular_banco, bg='#00513f', fg='white', bd=0, highlightthickness=0)
botao_atualizarbanco.place(x=15, y=650)
#####
botao_deletar = tk.Button(tb2, text='Deletar cliente', font='Arial 10', relief='flat',command=deletar, bg='#BF2823', fg='white', bd=0, highlightthickness=0)
botao_deletar.place(x=80, y=650)
#####
botao_obter = tk.Button(tb2, text='Copiar dados do cliente', relief='flat', font='Arial 10', bg='#00513f', fg='white', bd=0, highlightthickness=0)
botao_obter.place(x=176, y=650)
############# CRIANDO LABEL PARA PESQUISA PELA OS ############
label_pesquisa = tk.Label(tb2, text='Pesquisa:', font='Arial 12')
label_pesquisa.place(x=350, y=650)
entry_pesquisa = tk.Entry(tb2, font='Arial 12', relief='solid')
entry_pesquisa.place(x=430, y=650, width=110, height=20)
############# BOTÃO PARA PESQUISAR DADOS DOS CLIENTES PELA OS ############
botao_pesquisa = tk.Button(tb2, text='OK', font='Arial 9', relief='flat', command=pesquisar, bg='#00513f', fg='white', bd=0, highlightthickness=0)
botao_pesquisa.place(x=547, y=650)
############# CRIANDO BOTÃO DE MOSTRAR TODOS CHAMANDO A FUNÇÃO POPULAR ############
botao_mostrarTodos = tk.Button(tb2, text='Mostrar todos', font='Arial 9', relief='flat', command=popular_banco , bg='#00513f', fg='white', bd=0, highlightthickness=0)
botao_mostrarTodos.place(x=620, y=650)
############# BOTÃO DE CADASTRAR CLIENTE CHAMANDO A FUNÇÃO INSERIR_DADOS ############
botao_dados = tk.Button(botoes, text='                Cadastrar cliente                 ', font='Arial 14', relief='flat', command=inserir_dados, bg='#2DB06F', fg='white')
botao_dados.place(x=140, y=10)
############# BOTÃO PARA EXPORTAR DADOS DO BANCO DE DADOS PARA O EXCEL CHAMANDO A FUNÇÃO DE EXPORTAR_DADOS ############
botao_exportar = tk.Button(tb2, text='Exportar banco de dados para Excel', relief='flat', font='Arial 14', command=exportar_dados, bg='#00513f', fg='white')
botao_exportar.place(x=1170, y=650)
############# LOOP DA TELA NÃO FECHAR ############
window.mainloop()

