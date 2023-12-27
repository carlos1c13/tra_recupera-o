import tkinter as tk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo, askyesno, showwarning
import teste_clientes
import teste_produtos
import teste_vendas
import banco_sistema as db

conexao = db.conecta_bd()
db.cria_tabelas(conexao)

root = tk.Tk()
root.title('Sistemas de vendas')


toolbar = tk.Frame(root, relief=tk.RAISED, bg='#FFFEE1', height=100)
toolbar.pack()

content_button_img = Image.open("./images/cliente.png")
content_button_img = content_button_img.resize((48, 48))

content_button_img_tk = ImageTk.PhotoImage(content_button_img)
content_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D',
                                text="Cadastro de Clientes", compound="top", border=0, height=100,
                                image=content_button_img_tk, relief=tk.FLAT,
                                command=teste_clientes.draw_window)
content_button.image = content_button_img_tk
content_button.pack(side=tk.LEFT, padx=2)

semester_var = tk.IntVar()
discipline_var = tk.IntVar()

content_button_img = Image.open("./images/produtos.png")
content_button_img = content_button_img.resize((48, 48))

content_button_img_tk = ImageTk.PhotoImage(content_button_img)
content_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D',
                                text="cadastro de Produtos", compound="top", border=0, height=100,
                                image=content_button_img_tk, relief=tk.FLAT,
                                command=teste_produtos.draw_teste_produtos)
content_button.image = content_button_img_tk
content_button.pack(side=tk.LEFT, padx=2)

semester_var = tk.IntVar()
discipline_var = tk.IntVar()

content_button_img = Image.open("./images/carrinho-de-compras.png")
content_button_img = content_button_img.resize((48, 48))

content_button_img_tk = ImageTk.PhotoImage(content_button_img)
content_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D',
                                text="Cadastro de vendas", compound="top", border=0, height=100,
                                image=content_button_img_tk, relief=tk.FLAT,
                                command=teste_vendas.draw_window)
content_button.image = content_button_img_tk
content_button.pack(side=tk.LEFT, padx=2)

semester_var = tk.IntVar()
discipline_var = tk.IntVar()

exit_button_img = Image.open("./images/fechar.png")
exit_button_img = exit_button_img.resize((48, 48))

exit_button_img_tk = ImageTk.PhotoImage(exit_button_img)
exit_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D', border=0, height=100,
                            text="Sair", compound="top", image=exit_button_img_tk, relief=tk.FLAT,
                            command=root.quit, bd=0)

exit_button.image = exit_button_img_tk
exit_button.pack(side=tk.LEFT, padx=2)


root.mainloop()