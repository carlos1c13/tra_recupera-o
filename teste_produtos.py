import tkinter as tk
from tkinter import ttk
import re
from tkinter import messagebox
import banco_sistema as db

def draw_teste_produtos():
    # Conecta ao banco de dados
    conexao = db.conecta_bd()

    if not conexao:
        # Mostra uma mensagem de erro se a conexão falhar
        messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
        return

    produtos = tk.Toplevel()
    produtos.title('Cadastro de produtos')
    produtos.resizable(False, False)
    produtos.grab_set()

    def adicionar_produto():
        # Obtém os valores dos campos de entrada
        id_produto = entry_id_produto.get()
        nome_produto = entry_nome_produto.get()
        preco_produto = entry_preco_produto.get()

        # Adiciona os dados ao Treeview
        tree.insert("", tk.END, values=(id_produto, nome_produto, preco_produto))

        # Limpa os campos de entrada após a adição
        entry_id_produto.delete(0, tk.END)
        entry_nome_produto.delete(0, tk.END)
        entry_preco_produto.delete(0, tk.END)

        # Adiciona o produto ao banco de dados
        cursor = conexao.cursor()
        try:
            cursor.execute("INSERT INTO cadastro_produtos (id_produto, nome_produto, preço) VALUES (%s, %s, %s)",
                           (id_produto, nome_produto, preco_produto))
            conexao.commit()
            print("Produto adicionado ao banco de dados com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar produto ao banco de dados: {e}")
        finally:
            cursor.close()

    def excluir_produto():
        # Obtém o item selecionado no Treeview
        selected_item = tree.selection()

        # Remove o item selecionado do Treeview
        for item in selected_item:
            tree.delete(item)

            # Exclui o produto do banco de dados
            id_produto = tree.item(item, 'values')[0]
            cursor = conexao.cursor()
            try:
                cursor.execute("DELETE FROM cadastro_produtos WHERE id_produto = %s", (id_produto,))
                conexao.commit()
                print(f"Produto com ID {id_produto} excluído do banco de dados com sucesso!")
            except Exception as e:
                print(f"Erro ao excluir produto do banco de dados: {e}")
            finally:
                cursor.close()
         
    def preencher_treeview(tree):
    # Função de exemplo para preencher o Treeview com dados fictícios
        for i in range(1, 11):
            tree.insert("", "end", values=("Item {}".format(i)))

    
    # Criando a estrutura básica da interface
    frame = ttk.Frame(produtos)
    frame.grid(row=0, padx=10, pady=10)

    # Labels e Entry para produtos
    label_id_produto = ttk.Label(frame, text="ID do Produto:")
    label_id_produto.grid(row=0, column=0, sticky=tk.W, pady=5)

    entry_id_produto = ttk.Entry(frame)
    entry_id_produto.grid(row=0, column=1, sticky=tk.W, pady=2)

    label_nome_produto = ttk.Label(frame, text="Nome do Produto:")
    label_nome_produto.grid(row=0, column=2, sticky=tk.W, pady=5)

    entry_nome_produto = ttk.Entry(frame)
    entry_nome_produto.grid(row=0, column=3, sticky=tk.W, pady=2)

    label_preco_produto = ttk.Label(frame, text="Preço do Produto:")
    label_preco_produto.grid(row=0, column=4, sticky=tk.W, pady=5)

    entry_preco_produto = ttk.Entry(frame)
    entry_preco_produto.grid(row=0, column=5, sticky=tk.W, pady=5)

    # Treeview para exibir a lista de produtos
    tree = ttk.Treeview(produtos, columns=("ID", "Nome do Produto", "Preço"), show="headings")
    tree.column("ID", anchor=tk.W)
    tree.column("Nome do Produto", anchor=tk.W)
    tree.column("Preço", anchor=tk.W)

    tree.heading("ID", text="ID")
    tree.heading("Nome do Produto", text="Nome do Produto")
    tree.heading("Preço", text="Preço")

    tree.grid(row=1, column=0, sticky="nsew")

    botões = tk.Frame(produtos)
    botões.grid(row=3)

 # Botão para ação relacionada a produtos (por exemplo, adicionar produto)
    btn_adicionar_produto = ttk.Button(botões, text="Adicionar Produto", command=adicionar_produto)
    btn_adicionar_produto.grid(row=3, column=1, pady=10)

    # Botão para excluir produtos
    btn_excluir_produto = ttk.Button(botões, text="Excluir Produto", command=excluir_produto)
    btn_excluir_produto.grid(row=3, column=2, pady=10)


    botao_cancelar = ttk.Button(botões, text='VOLTAR', command=produtos.destroy)
    botao_cancelar.grid(row=3, column=3, sticky=tk.EW, padx=5)