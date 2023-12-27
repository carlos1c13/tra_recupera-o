import tkinter as tk
from tkinter import ttk
import re
from tkinter import messagebox
import banco_sistema as db

conexao = db.conecta_bd()

def draw_window():
    clientes = tk.Toplevel()
    clientes.title('Cadastro de clientes')
    clientes.resizable(False, False)
    clientes.grab_set()

    def adicionar_cliente():
        cpf = entry_cpf.get()
        nome = entry_nome.get()
        data_nascimento = entry_data.get()

        tree.insert("", tk.END, values=(cpf, nome, data_nascimento))


        entry_cpf.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        
           # Adiciona o cliente ao banco de dados
        
        if conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute("INSERT INTO cadastro_clientes (cpf, nome, data_de_nascimento) VALUES (%s, %s, %s)", (cpf, nome, data_nascimento))
                conexao.commit()
                print("Cliente adicionado ao banco de dados com sucesso!")
            except Exception as e:
                print(f"Erro ao adicionar cliente ao banco de dados: {e}")
            finally:
                conexao.close()

    # Função para excluir cliente do banco de dados
    def excluir_cliente():
        # Obtém o item selecionado no Treeview
        selected_item = tree.selection()

        # Remove o item selecionado do Treeview
        for item in selected_item:
            tree.delete(item)

            # Exclui o cliente do banco de dados
            cpf = tree.item(item, 'values')[0]

            if conexao:
                cursor = conexao.cursor()
                try:
                    cursor.execute("DELETE FROM cadastro_clientes WHERE cpf = %s", (cpf,))
                    conexao.commit()
                    print(f"Cliente com CPF {cpf} excluído do banco de dados com sucesso!")
                except Exception as e:
                    print(f"Erro ao excluir cliente do banco de dados: {e}")
                finally:
                    conexao.close()

    def preencher_treeview(tree):
    # Função de exemplo para preencher o Treeview com dados fictícios
        for i in range(1, 11):
            tree.insert("", "end", values=("Item {}".format(i)))

# Botoes =================================
    frame_fields = tk.Frame(clientes)
    frame_fields.grid(row=0, padx=10, pady=10)

    label_cpf = tk.Label(frame_fields, text='CPF')
    label_cpf.grid(row=0, column=0, padx=5, sticky=tk.W)

    entry_cpf = tk.Entry(frame_fields)
    entry_cpf.grid(row=0, column=1, padx=2, sticky=tk.W)

    label_nome = tk.Label(frame_fields, text='Nome do Cliente')
    label_nome.grid(row=0, column=2, padx=5, sticky=tk.W)

    entry_nome = tk.Entry(frame_fields)
    entry_nome.grid(row=0, column=3, padx=2, sticky=tk.W)

    label_data = tk.Label(frame_fields, text='Data de Nascimento')
    label_data.grid(row=0, column=4, padx=5, sticky=tk.W)

    entry_data = tk.Entry(frame_fields)
    entry_data.grid(row=0, column=5, padx=2, sticky=tk.W)

# Treeview
    tree = ttk.Treeview(clientes, columns=("CPF", "Nome", "Data de Nascimento"), show="headings")
    tree.column("CPF", anchor=tk.W)
    tree.column("Nome", anchor=tk.W)
    tree.column("Data de Nascimento", anchor=tk.W)

    tree.heading("CPF", text="CPF")
    tree.heading("Nome", text="Nome do Cliente")
    tree.heading("Data de Nascimento", text="Data de Nascimento")

    tree.grid(row=1, column=0, sticky="nsew")
    
    #clientes.grid_rowconfigure(0, weight=1)
    #clientes.grid_columnconfigure(0, weight=1)
    
    frame_botões = tk.Frame(clientes)
    frame_botões.grid(row=3)
    
# Botão para adicionar dados
    btn_adicionar = tk.Button(frame_botões, text="Adicionar Cliente", command=adicionar_cliente)
    btn_adicionar.grid(row=3, column=1, padx=10)

# Botão para excluir dados
    btn_excluir = tk.Button(frame_botões, text="Excluir Cliente", command=excluir_cliente)
    btn_excluir.grid(row=3, column=2, padx=10)

    botao_cancelar = ttk.Button(frame_botões, text='VOLTAR', command=clientes.destroy)
    botao_cancelar.grid(row=3, column=3, sticky=tk.EW, padx=5)
