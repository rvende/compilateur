# coding: utf8
import sys
#import os
from tkinter import *
import subprocess
from tkinter import filedialog
from tkinter import ttk
from lexical import *
from syntax import *
from semantique import *
from genCode import *

class Interface(Frame):

    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        fenetre.title("Compilateur")
        Frame.__init__(self, fenetre, width=1000, height=600, **kwargs)
        self.grid(sticky="news")
        fenetre.grid_columnconfigure(0,weight=1)
        fenetre.grid_columnconfigure(0,weight=1)
        fenetre.grid_rowconfigure(index=1,weight=1)

        self.rowconfigure(1,weight=1);
        self.columnconfigure(1,weight=1);
        self.columnconfigure(2,weight=1);

        barremenu = Menu(fenetre)
        fenetre.config(menu = barremenu)

        menufichier = Menu(barremenu,tearoff=0)
        barremenu.add_cascade(label="Fichier", menu=menufichier)
        menufichier.add_command(label="Ouvrir", command=self.ouvrir)
        menufichier.add_command(label="Enregistrer",command=self.enregistrer)
        #menufichier.add_command(label="Enregistrer sous")
        menufichier.add_command(label="Quitter", command=fenetre.destroy)

        menuCompiler = Menu(barremenu,tearoff=0)
        barremenu.add_cascade(label='Compiler',menu=menuCompiler)
        menuCompiler.add_command(label='Run',command=self.compiler,foreground="red")
        self.case_debug = IntVar()
        menuCompiler.add_checkbutton(label="Option de debug", variable=self.case_debug,command=self.debug)

        self.txt = Text(self, height=1,width=20, wrap=WORD)
        #fichier = open("test.c","r")
        #contenu = fichier.read()
        #self.txt.insert('1.0', contenu)
        #fichier.close()
        self.txt.grid(row=1, column=1,sticky="news")
        #txt.configure(width=int(fenetre.winfo_screenwidth()/12)) #la largeur est a donner en caractères pas en pixels
        self.txt.config(height=int(fenetre.winfo_screenheight()/(12*2)+2),width=80)
        self.txt.bind('<Control_L><s>',self.enregistrer)
        #txt.configure({"heigth":fenetre.winfo_screenheight()/(12*2)})
        # Création de nos widgets
        #self.message = Label(self, text="Vous n'avez pas cliqué sur le bouton.")
        #self.message.grid(row =1, column =1)

        #self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        #self.bouton_quitter.grid(row =3, column =1)

        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text='Console MSM')
        tabControl.grid(row =1, column =2, sticky='NESW')


        self.sortie2 = Text(self,bg= 'black',fg='green')
        self.sortie2.grid(row =2, column =1,sticky='NESW',columnspan=2)
        #self.sortie.insert('1.0',self.res)
        self.sortie2.config(height=5,width=100)
        #case = Checkbutton(self, text="Option de debug", variable=self.case_debug,command=self.debug)
        #case.grid(row =3, column =1)

        #self.bouton_cliquer = Button(self, text="Compiler", fg="red",
        #        command=self.compiler)
        #self.bouton_cliquer.grid(row =3, column =2)
        self.commande = "./msm/msm genCode"


    def debug(self):
        #print("debug cocher")
        #print("val case : "+str(self.case_debug.get()))
        val_case = self.case_debug.get()
        if(val_case == 1 ):
            self.commande = "./msm/msm -d -d genCode"
        else:
            self.commande = "./msm/msm genCode"

    def compiler(self):
    	filenames = ['bibliotheque_standard.c', self.filename] 
    	with open('main.c', 'w') as outfile: 
    		for fname in filenames: 
    			with open(fname) as infile: 
    				for line in infile: 
    					outfile.write(line)
    	lexical = Lexical("main.c")
    	lexical.main()
    	liste_arbre = []
    	while lexical.next()['type'] != "tok_EOF":
    		syntax = Syntax(lexical)
    		arbre = syntax.fonction()
    		arbre.afficher()
    		liste_arbre.append(arbre)
    		semantique = Analyse_semantique()
    		semantique.analyse(arbre)

    	generationCode = GenerationCode(syntax)
    	generationCode.lancementGenerationCode(liste_arbre)
    	process = subprocess.Popen(self.commande.split(), stdout=subprocess.PIPE)
    	self.res, error = process.communicate()
    	#print(output.decode('utf-8'))

    	self.sortie = Text(self.tab1,bg= 'black',fg='green')
    	self.sortie.config(state=NORMAL)
    	self.sortie.insert('1.0',self.res)
    	self.sortie.config(height=int(fenetre.winfo_screenheight()/(12*2)),width=100,state=DISABLED)
    	self.sortie.columnconfigure(1,weight=1);
    	self.columnconfigure(2,weight=1);
    	self.sortie.grid(row =1, column =1,sticky="news")
    	self.sortie.yview(END)
    	scroll = Scrollbar(self.tab1,command=self.sortie.yview)
    	self.sortie.columnconfigure(2,weight=1);
    	self.columnconfigure(3,weight=1);
    	scroll.grid(row =1, column =2,sticky="news")
    	self.sortie['yscrollcommand'] = scroll.set



    def ouvrir(self):
        self.filename = filedialog.askopenfilename(filetypes = (("C files","*.c"),("all files","*.*")))
        fichier = open(self.filename,"r")
        contenu = fichier.read()
        self.txt.insert('1.0', contenu)
        fichier.close()

    def enregistrer(self, event = None):
        nouveau_contenu = self.txt.get("1.0",END)
        fichier = open(self.filename,"w")
        fichier.write(nouveau_contenu)
        fichier.close()


if __name__ == '__main__':
	fenetre = Tk()
	interface = Interface(fenetre)

	interface.mainloop()
	interface.destroy()
