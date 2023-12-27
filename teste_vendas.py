import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import teste_produtos
import banco_sistema as db

conexao = db.conecta_bd()

def draw_window():
    if not conexao:
        # Mostra uma mensagem de erro se a conexão falhar
        messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
        return

    vendas = tk.Toplevel()
    vendas.title('Cadastro de vendas')
    vendas.resizable(False, False)
    vendas.grab_set()

    def adicionar_produto():
        # Função para adicionar produto ao Treeview
        id_produto = entry_id_produto.get()
        nome_produto = entry_nome_produto.get()
        preco_produto = entry_preco_produto.get()
        quantidade_produto = entry_quantidade_produto.get()
        hora_venda = datetime.now().strftime("%H:%M:%S")

        # Adiciona os dados ao Treeview
        tree.insert("", tk.END, values=(id_produto, nome_produto, preco_produto, quantidade_produto, hora_venda))

        # Limpa os campos de entrada após a adição
        entry_id_produto.delete(0, tk.END)
        entry_nome_produto.delete(0, tk.END)
        entry_preco_produto.delete(0, tk.END)
        entry_quantidade_produto.delete(0, tk.END)

        # Adiciona a venda ao banco de dados
        cursor = conexao.cursor()
        try:
            cursor.execute("INSERT INTO cadastra_vendas (id_produto, nome_produto, preço, quantidade, hora_venda) VALUES (%s, %s, %s, %s, %s)",
                           (id_produto, nome_produto, preco_produto, quantidade_produto, hora_venda))
            conexao.commit()
            print("Venda adicionada ao banco de dados com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar venda ao banco de dados: {e}")
        finally:
            cursor.close()

    def calcular_total():
        # Função para calcular o total da venda
        total = 0
        for item in tree.get_children():
            preco_total = float(tree.item(item, 'values')[2])
            quantidade_item = float(tree.item(item, 'values')[3])
            total += preco_total * quantidade_item

        label_resultado["text"] = f"Total da Venda: R${total:.2f}"

    def excluir_produto():
        # Função para excluir produto do Treeview
        item_selecionado = tree.selection()
        for item in item_selecionado:
            tree.delete(item)

            # Exclui a venda do banco de dados
            id_produto = tree.item(item, 'values')[0]
            cursor = conexao.cursor()
            try:
                cursor.execute("DELETE FROM cadastra_vendas WHERE id_produto = %s", (id_produto,))
                conexao.commit()
                print(f"Venda do produto com ID {id_produto} excluída do banco de dados com sucesso!")
            except Exception as e:
                print(f"Erro ao excluir venda do banco de dados: {e}")
            finally:
                cursor.close()

    def abrir_produtos():
        # Chama a função da janela de consulta
        teste_produtos.draw_teste_produtos()

    def preencher_treeview(tree):
        # Função de exemplo para preencher o Treeview com dados fictícios
        for i in range(1, 11):
            tree.insert("", "end", values=("Item {}".format(i)))


    # Criando a estrutura básica da interface
    frame = ttk.Frame(vendas, padding="10")
    frame.grid(row=0)

    # Labels e Entry para produtos
    label_id_produto = ttk.Label(frame, text="ID do Produto:")
    label_id_produto.grid(row=0, column=1, sticky=tk.W, pady=5)

    entry_id_produto = ttk.Entry(frame)
    entry_id_produto.grid(row=0, column=2, sticky=tk.W, pady=5)

    label_nome_produto = ttk.Label(frame, text="Nome do Produto:")
    label_nome_produto.grid(row=0, column=3, sticky=tk.W, pady=5)

    entry_nome_produto = ttk.Entry(frame)
    entry_nome_produto.grid(row=0, column=4, sticky=tk.W, pady=5)

    label_preco_produto = ttk.Label(frame, text="Preço Unitário:")
    label_preco_produto.grid(row=0, column=5, sticky=tk.W, pady=5)

    entry_preco_produto = ttk.Entry(frame)
    entry_preco_produto.grid(row=0, column=6, sticky=tk.W, pady=5)

    label_quantidade_produto = ttk.Label(frame, text="Quantidade do Produto:")
    label_quantidade_produto.grid(row=0, column=7, sticky=tk.W, pady=5)

    entry_quantidade_produto = ttk.Entry(frame)
    entry_quantidade_produto.grid(row=0, column=8, sticky=tk.W, pady=5)

    btn_buscar_produto = ttk.Button(frame, text="Consultar Produto", command=abrir_produtos)
    btn_buscar_produto.grid(row=0, column=9, pady=10)
    
    # Treeview para exibir a lista de produtos
    tree = ttk.Treeview(vendas, columns=("ID", "Nome do Produto", "Preço Unitário", "Quantidade", "Hora da Venda"), show="headings")
    tree.column("ID", anchor=tk.W)
    tree.column("Nome do Produto", anchor=tk.W)
    tree.column("Preço Unitário", anchor=tk.W)
    tree.column("Quantidade", anchor=tk.W)
    tree.column("Hora da Venda", anchor=tk.W)

    tree.heading("ID", text="ID")
    tree.heading("Nome do Produto", text="Nome do Produto")
    tree.heading("Preço Unitário", text="Preço Unitário")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Hora da Venda", text="Hora da Venda")

    tree.grid(row=1, column=0, sticky="nsew")

    frame_bo = tk.Frame(vendas)
    frame_bo.grid(row=3)

# Rótulo para exibir o resultado do cálculo
    label_resultado = ttk.Label(frame_bo, text="Total da Venda: R$0.00")
    label_resultado.grid(row=3, column=0,sticky="nswe",pady=20)
    
     # Botão para inserir produto
    btn_inserir_produto = ttk.Button(frame_bo, text="Inserir Produto", command=adicionar_produto)
    btn_inserir_produto.grid(row=3, column=1, pady=10, sticky="ns")

    btn_excluir_produto = ttk.Button(frame_bo, text="Excluir Produto", command=excluir_produto)
    btn_excluir_produto.grid(row=3, column=4, pady=10, sticky="ns")

    # Botão para calcular total
    btn_calcular_total = ttk.Button(frame_bo, text="Calcular Total", command=calcular_total)
    btn_calcular_total.grid(row=3, column=3, pady=10, sticky="ns")

    botao_cancelar = ttk.Button(frame_bo, text='Finalizar venda', command=vendas.destroy)
    botao_cancelar.grid(row=3, column=5, sticky="ns", pady=10)
