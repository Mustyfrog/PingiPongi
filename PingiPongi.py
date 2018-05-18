#-*- coding: utf-8 -*-


import pyping
from Tkinter import *
import os

# Creation classe qui hérite des attributs de Frame (et donc deviens un widget)
class Interface(Frame):
    """ Fenetre principal
        Les widgets sont stockés sous formes d'attributs de cette classe
    """
    def __init__(self,fenetre,**kwargs):
        Frame.__init__(self,fenetre,**kwargs)
        # Initialisation titre, taille et comportement fenetre
        fenetre.title("Pingi Pongi")
        fenetre.geometry("500x500")
        self.pack(fill=BOTH)
        # Variables
        self.ping="ah"
        self.stop=0
        self.adresseIP=""
        self.isDown=0
        # Champ où s'affiche le serveur que l'on ping
        self.message=Label(self,text="Ping avec serveur Google : ",bg="LightSeaGreen")
        self.message.pack(pady=20,fill=X)
        # Champ ou s'affiche la latence
        self.pingM=Label(self,text="")
        self.pingM.pack()

        # Boutton radio
        self.var_choix=StringVar()
        self.choix_un=Radiobutton(fenetre,text="Google",variable=self.var_choix,value="8.8.8.8")
        self.choix_deux=Radiobutton(fenetre,text="Cines",variable=self.var_choix,value="193.48.169.60")
        self.choix_trois=Radiobutton(fenetre,text="LoL",variable=self.var_choix,value="104.160.141.3")
        self.choix_un.pack()
        self.choix_deux.pack()
        self.choix_trois.pack()

        # Boutton ping
        self.bouton_ping=Button(self,text="Ping",command=self.Hugeping)
        self.bouton_ping.pack(pady=4,fill=X)
        # Bouton stop
        self.bouton_stop=Button(self,text="Stop",command=self.stopCommand)
        self.bouton_stop.pack(pady=4,fill=X)
        # Bouton quitter
        self.bouton_quitter=Button(self,text="Quit",command=self.quit)
        self.bouton_quitter.pack(pady=4,fill=X)
    # Commande de stop
    def stopCommand(self):
        self.stop=1
    # Commande de ping
    def Hugeping(self):
        def piping():
            # Si bouton stop appuyé en plein ping
            if self.stop==1:
                self.stop=0
                self.isTherePing=0
                # Repasse le bouton ping en actif
                self.bouton_ping['state']="active"
                print("State returned to 0\nself.stop ={}\n".format(self.stop))
            # Si pas de bouton stop appuyé
            else:
                # Permet de récupérer le contenu de la variable var_choix
                self.adresseIP=self.var_choix.get()
                print("Adresse IP : {}".format(self.adresseIP))
                if self.adresseIP=="8.8.8.8":
                    self.message['text']="Ping avec serveur Google : "
                if self.adresseIP=="193.48.169.60":
                    self.message['text']="Ping avec serveur du Cines : "
                if self.adresseIP=="104.160.141.3":
                    self.message['text']="Ping avec serveur LoL : "
                # On désactive le bouton ping pour éviter d'avoir plusieurs instances de HugePing
                self.bouton_ping['state']="disabled"
                if self.isDown==256:
                    # Actualisation du contenu de pingM
                    self.pingM.config(text="Network is Unreachable")
                    # Temporisation de une seconde
                    self.stop=1
                    self.after(1000,piping)
                else:
                    # Ping vers serveur redirigé vers un fichier
                    os.system("ping -c1 "+self.adresseIP+"|grep time=|cut -d\"=\" -f4 > ping")
                    self.isDown=os.system("ping -c1 "+self.adresseIP)
                    print(self.isDown)
                    # Lecture du fichier plus affectation à self.ping
                    f=open("ping","r")
                    Myping=f.read()
                    self.ping=Myping
                    # Actualisation du contenu de pingM
                    self.pingM.config(text=str(self.ping))
                    # Temporisation de une seconde
                    self.after(1000,piping)
        piping()

fenetre=Tk()
interface=Interface(fenetre)
interface.mainloop()
os.remove("ping")
