#!/home/djabril/virtualenvPython/python3.5/bin/python
# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
import time
import sys
import os
import numpy as np
import time
from matplotlib import animation
import zhinst.utils as utils
import zhinst.ziPython as ziPython
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from newportxps import NewportXPS
from pyniryo import *
from Testmesure import Lockin 

 
 
 
 

 

class BRDF(QMainWindow):
    '''
    Classe codant pour le GUI du programme BRDF
    '''
    
    def __init__(self,):
        super(BRDF,self).__init__()
        self.initUI()
        self.initialisation=False
        
        self.setWindowTitle("BRDF")
        self.setGeometry(800,100,1000,800)


    def initUI(self):

        
        #on definit les onglets (tabs) comme occupant le central widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget() # intitialisation pour la tab 4
             
 
 
        self.tabs.addTab(tab1,"General")
        self.tab_xps = self.tabs.addTab(tab2,"Moteur Newport")
        self.tab_ned = self.tabs.addTab(tab3,"Robot Nyrio")
        self.tab_mode = self.tabs.addTab(tab4,"Modemesures")

        self.tabs.setTabEnabled(self.tab_xps, False)
        self.tabs.setTabEnabled(self.tab_ned, False)
        ###################################################################
        #                                                                 #
        #                             TAB 1                               #
        #                                                                 #
        ###################################################################
 
        
        btn_plot = QPushButton('Start move detector', tab1)
        btn_plot.clicked.connect(self.btn_plot_callback)
        
        self.txed_Nsample=QLineEdit('10',tab1)
        self.lbl_Nsample=QLabel('Points :',tab1)
  
        self.txed_min_detecteur=QLineEdit('1',tab1)
        self.lbl_min_detecteur=QLabel('Min :')
 
        self.toto=QLineEdit('1')

 
        
        self.txed_max_detecteur=QLineEdit('10',tab1)
        self.lbl_max_detecteur=QLabel('Max :')
  
 
        
        self.fig = plt.Figure(figsize=[15,10])
        self.ax = self.fig.add_axes([0.05,0.05,0.9,0.9]) 
        self.ax.set_xlim([0,20])
        self.ax.set_ylim([-140,-70])

        plt.show(block=False)  
        
        self.line, = self.ax.plot([],[],'-o')  # trace 
        self.canvas = FigureCanvas(self.fig)
        toolbar = NavigationToolbar(self.canvas,tab1)
        

        
        
        layout1=QHBoxLayout(tab1)
        layout11=QVBoxLayout()
        layout111=QGridLayout()
        layout1111=QGridLayout()
        layout12=QVBoxLayout()
        layout13=QVBoxLayout()
        

        layout112 = QVBoxLayout()
        self.connect = QPushButton('Connect',tab1)
        self.connect.clicked.connect(self.connect_callback)
        layout112.addWidget(self.connect)
 
        
        self.a=QLabel()
        self.b=QPixmap('images/LED_off.jpg').scaledToWidth(16)
        self.c=QPixmap('images/LED_on.jpg').scaledToWidth(16)
        self.a.setPixmap(self.b)
        self.a.filename = 'off'
        layout112.addWidget(self.a)


        self.info_newport  = QPlainTextEdit()
        layout112.addWidget(self.info_newport)
        self.info_nyrio  = QPlainTextEdit()
        layout112.addWidget(self.info_nyrio)
        self.info_mfli  = QPlainTextEdit()
        layout112.addWidget(self.info_mfli)
        
        layout11.addLayout(layout112)
 
        layout11.addStretch(1)


 

   
        layout111.addWidget(QLabel('Parametres'),0,0)

        
        
        layout111.addWidget(self.lbl_Nsample,1,0)        
        layout1111.addWidget(self.txed_Nsample,0,1)
        layout111.addLayout(layout1111,1,1)
 
        
        layout111.addWidget(self.lbl_min_detecteur,2,0)
        layout111.addWidget(self.txed_min_detecteur,2,1)
        layout111.addWidget(QLabel('deg'),2,2)
 
        
        layout111.addWidget(self.lbl_max_detecteur,3,0)
        layout111.addWidget(self.txed_max_detecteur,3,1)
        layout111.addWidget(QLabel('deg'),3,2)
 
   
        
        layout11.addLayout(layout111)
        layout11.addWidget(btn_plot)
        layout11.addStretch(1)
        layout11.addWidget(QLabel('Connexion aux appareils'))
 
        

        
 
        
        layout12.addWidget(self.canvas)
        layout12.addWidget(toolbar)
        layout12.addStretch(1)
        
        layout1.addStretch(2)
        layout1.addLayout(layout11)
        layout1.addStretch(1)
        layout1.addLayout(layout12)
        ###################################################################
        #                                                                 #
        #                             TAB 2                               #
        #                                                                 #
        ###################################################################
 
        
 
 
        moreFrame = QFrame(tab2)
        moreFrame.resize(200,200)
        moreFrame.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
 
 
        checkLayout = QGridLayout(moreFrame)
        btn_plot_xps = QPushButton('Origine moteurs', tab3)
        btn_plot_xps.clicked.connect(self.initialisation_xps)
        checkLayout.addWidget(btn_plot_xps,0,1)

        checkLayout.addWidget(QLineEdit("test"),1,1)

        
        ###################################################################
        #                                                                 #
        #                             TAB 3                               #
        #                                                                 #
        ###################################################################
  
        
        btn_plot3 = QPushButton('Movedeteta', tab3) #Bouge le detecteur et le plateau /et le robot pour l'alignement laser du banc
        btn_plot3.clicked.connect(self.btn_plot3_callback)
        btn_plot4 = QPushButton('Test mesures', tab3)
        btn_plot4.clicked.connect(self.btn_plot4_callback)
        #test part mouvement robot
        btn_plot5 = QPushButton('Placer echantillon', tab3)
        btn_plot5.clicked.connect(self.btn_plot5_callback)
        
        self.txed_browser3=QLineEdit(tab3)
        self.txed_browser3.setText('ROBOT NYRIO NED')
        
        btn_open_file_browser3 = QPushButton( parent=tab3)
 
        btn_open_file_browser3.setIcon(QIcon('images/browser.jpg'))
        
        self.txed_window3 = QLineEdit(tab3)
        self.txed_window3.setText('100')
        
        layout3=QVBoxLayout(tab3)
        layout31=QHBoxLayout()
        layout32=QHBoxLayout()

         
        layout31.addWidget(QLabel('ROBOT'))
 
        layout31.addWidget(self.txed_browser3)
 
        layout32.addWidget(btn_plot3)
        layout32.addWidget(btn_plot4)
        #Test nouveau bouton
        layout32.addWidget(btn_plot5)
 
        layout3.addLayout(layout32)
        #checkLayout.addWidget(QLineEdit("test"),1,1)
        ##_____________Tentative_de_TAB4
        ###################################################################
        #                                                                 #
        #                             TAB 4                               #
        #                                                                 #
        ###################################################################



        

        moreFrame = QFrame(tab4)
        moreFrame.resize(200,200)
        moreFrame.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
 
 
        checkLayout = QGridLayout(moreFrame)
        btn_plot6 = QPushButton('Compiler', tab4)
        checkLayout.addWidget(btn_plot6,3,2)
        
        btn_plot6.clicked.connect(self.btn_plot6_callback)
        checkLayout.addWidget(QLineEdit("teta"),1,2)
        btn_plot7 = QPushButton('Modif angle direct', tab4)
        checkLayout.addWidget(btn_plot7,4,2)
        btn_plot7.clicked.connect(self.btn_plot7_callback)        
        checkLayout.addWidget(QLineEdit("delta"),2,3)
        
        self.LPF_order = QComboBox()
        self.LPF_order.addItem('1')
        self.LPF_order.addItem('2')
        self.LPF_order.addItem('3')
        self.LPF_order.addItem('4')
        self.LPF_order.addItem('5')
        self.LPF_order.addItem('6')
        self.LPF_order.addItem('7')
        self.LPF_order.addItem('8')
        self.LPF_order.addItem('9')
        
        checkLayout.addWidget(self.LPF_order,3,5)





        

        ###################################################################
        #                                                                 #
        #                             GENERAL                             #
        #                                                                 #
        ###################################################################
        exitAction = QAction(QIcon('images/exit24.png'), 'Exit', self)        
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application') #affiche dans la status bar
        exitAction.triggered.connect(qApp.quit)
        
        saveAction = QAction(QIcon('images/save.jpg'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save parameters') #affiche dans la status bar
        # saveAction.triggered.connect(self.save_callback)
        
        loadAction = QAction(QIcon('images/load.jpg'), 'Load', self)
        loadAction.setStatusTip('Load parameters') #affiche dans la status bar
        # loadAction.triggered.connect(self.load_callback)
        
        
        toolbar = self.addToolBar('Exit') #'Exit' s'affiche lorsqu on passe la souris dessus
        #toolbar = self.addToolBar('Save')
        toolbar.addAction(exitAction)  
        toolbar.addAction(saveAction)
        toolbar.addAction(loadAction)
        
        self.statusBar().showMessage('Ready')
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        
        self.setGeometry(0, 0, 1500, 1000)
        self.setWindowTitle("BRDF")
        self.setWindowIcon(QIcon('images/web.png'))
        
        # self.load_callback() #charge les donnees enregistree
        #self.btn_plot_callback() #plot le graphe associe aux donnees
        
        self.anim_running=False

        
        self.show()
 

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',"Voulez vous vraiment quitter?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def btn_plot_callback(self): #Methode pour appeler start move detector
        
        x=[] # le pas/angle
        y=[] #amplitude ou valeur du detecteur
                
          
        nb = int(str(self.txed_Nsample.text()))
        min_det = float(str(self.txed_min_detecteur.text()))
        max_det = float(str(self.txed_max_detecteur.text()))
        angleR=0
        volute=0
        angle = min_det
        pas = (max_det- min_det)/nb
        E = np.loadtxt('C:\Users\ManipBRDF\Desktop\BRDF\djabrilBrdf\ROBOTV3\output\samples',skiprows=3)
        
        print(E[1,2])


        a1=E[0,1]*np.pi/180
        a2=-E[0,2]*np.pi/180
        a3=(90-E[0,3])*np.pi/180
        a4=E[0,4]*np.pi/180
        a5=E[0,5]*-np.pi/180
        a6=E[0,6]*np.pi/180

        print(a1, a2, a3, a4, a5,a6)

        #______________Gestion_d'exception_Sur les ranges du robot pour ne pas avoir d'erreurs_

  

        
        try:
            for i in range (len(E)):
                a1=round(E[i,1]*np.pi/180,3)
                a2=round(-E[i,2]*np.pi/180,3)
                a3=round((90-E[i,3])*np.pi/180,3)
                a4=round(((E[i,4]*np.pi/180)-0.06),3)
                a5=round(E[i,5]*-np.pi/180,3)
                a6=round((E[i,6]*np.pi/180),3)
                #gestion d'exception
                if a1>2.9 or a1<-2.9:
                    print("out of range a1")
                if a2>0.6 or a2<-1.9:
                    print("out of range a2")
                if a3>1.5 or a3<-1.3:
                    print("out of range a3")
                if a4>2.0 or a4<-2.0:
                    print("out of range a4")
                if a5>1.0 or a5<-2.0:
                    print("out of range a5")
                if a6>2.53 or a6<-2.53:
                    print("out of range a6 ")
    ##            if a6>2.53:
    ##                a6 = a6-0.05
    ##            if a6<-2.53:
    ##                a6= a6+ 0.05
                self.ned.move_joints(a1, a2, a3, a4, a5,a6) # NE pas oublier d'initialiser les moteurs.
            # rotation du plateau robot
                angleR = E[i,7] # originerobot
                print("****position plateau en deg :" ,angleR)
                self.xps.move_stage('Group1.Pos',angleR)
               
                volute = E[i,8]-90
                time.sleep(1)
                print("****position detecteur en deg :" ,volute)
                self.xps.move_stage('Group2.Pos',volute)
                print("mesure numero",i)
                Val=self.Valeur_det.get_mag()
                x.append(i)
                y.append(Val)

                self.line.set_data(x,y)
                self.canvas.draw()
                self.canvas.flush_events()
                print("Mesure = ",Val)
                
                
                
                
        except:
            print("joint not in range perso")


        
    def stop_anim(self):
        if self.anim_running:
            self.anim.event_source.stop()
            self.anim_running = False
            if not self.f.closed:
                self.f.close()
            self.led2.setPixmap(self.led2_off)
            self.led2.filename = 'off'
#        else:
#            self.anim.event_source.start()
#            self.anim_running = True
    
    def btn_plot3_callback(self): #Positionnement pour l'étalonnage et l'lalignement laser avec le 
#Movedata
        nb = int(str(self.txed_Nsample.text()))
        min_det = float(str(self.txed_min_detecteur.text()))
        max_det = float(str(self.txed_max_detecteur.text()))
        angleR=0
        volute=0
        angle = min_det
        pas = (max_det- min_det)/nb
        E = np.loadtxt('C:\Users\ManipBRDF\Desktop\BRDF\djabrilBrdf\ROBOTV3\output\samples',skiprows=3)
        print(E[0,2])


        a1=E[0,1]*np.pi/180
        a2=-E[0,2]*np.pi/180
        a3=(90-E[0,3])*np.pi/180
        a4=E[0,4]*np.pi/180
        a5=(E[0,5]*-np.pi/180)-0.06
        a6=E[0,6]*np.pi/180

        print(a1, a2, a3, a4, a5,a6)
        try:
            for i in range (40):
                a1=E[i,1]*np.pi/180
                a2=-E[i,2]*np.pi/180
                a3=(90-E[i,3])*np.pi/180
                a4=E[i,4]*np.pi/180
                a5=E[i,5]*-np.pi/180
                a6=E[i,6]*np.pi/180
    ##            if a6>2.53:
    ##                a6 = a6-0.05
    ##            if a6<-2.53:
    ##                a6= a6+ 0.05
                self.ned.move_joints(a1, a2, a3, a4, a5,a6)
            # rotation du plateau robot
                angleR = E[i,7]-90 # originerobot
                self.xps.move_stage('Group1.Pos',angleR)
                print(angleR)
                volute = E[i,8]-180
                self.xps.move_stage('Group2.Pos',volute)
                Val=self.Valeur_det.get_mag()        
                print("Mesure = ",Val)
        except:
            print("joint not in range")
                

            

        
        
    def btn_plot4_callback(self):#Positionnement pour l'étalonnage et l'lalignement laser avec le

        #testmesures
                    
      # instancier la classe
        for i in range(40):
            
            Val=self.Valeur_det.get_mag()
           
            print("Mesure = ",Val)
        

        
   #vertical
       # self.ned.move_to_home_pose()
   #horizontal
       # self.ned.move_joints(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

       
    def btn_plot5_callback(self):          # Placer l'échantillon
        E = np.loadtxt('C:\Users\ManipBRDF\Desktop\BRDF\djabrilBrdf\ROBOTV3\output\samples')

        a1=0
        a1>-2.9 and a1<2.9

        a2=0.471
        a2>-1.9 and a2<0.6

        a3=0.602
        a3>-1.3 and a3<1.5

        a4=0
        a4>-2.0 and a4<2.0

        a5=0.195
        a5>-2.0 and a5<1

        a6=1.242
        a6>-2.0 and a6<2.0
        
     

            
        self.ned.move_joints(-1.2, -11.23, 20, -3.44, 49.73, -12.49)


    def btn_plot6_callback(self):

        ligne1="MODE De FONCTIONNEMENT (1:tetai,phii,tetao,phio   2:tetai,phii,delta,pas_gamma  3:tetai,phii,pas_delta,pas_gamma,1(hemisphere complet) ou 2(demihemisphere))\n"
        ligne2="Choisir mode\n"
        ligne3="les angles de consignes (en °) (teta [0;90] phi[-180;180] delta[90;270])\n"
        ligne4="Choisir les angels connu et l'angle cherché\n"
        print("Compiler")
        #os.system("robot.exe")
        
        choix = int(self.LPF_order.currentText())
        print("choix",choix)
        if choix == 4:
            ligne2="4  1\n"            
            ligne4="40 100.D0 60.D0 185.D0\n"
        if choix == 1:
            ligne2="1  1\n"
            ligne4="45.D0 175.D0 60.D0 185.D0\n"
        if choix ==2 :
            ligne2="2  1\n"
            ligne4="65.D0 -125.D0 160.D0 40\n"
        if choix ==3 :
            ligne2="3  1\n"
            ligne4="40.D0 -155.D0 40 40 1\n"
        if choix ==5 :
            ligne2="5  1\n"
            ligne4="48.D0 40 -55.D0 235.D0 30.D0 95.D0\n"
        if choix ==6 :
            ligne2="6  1\n"
            ligne4="40.D0 -39.D0 40\n"   
        if choix ==7 :
            ligne2="7  1\n"
            ligne4="20  39.D0 20\n"
        if choix ==8 :
            ligne2="8  1\n"
            ligne4="3 14.D0 5  10\n"
        if choix ==9 :
            ligne2="9  0\n"
            ligne4="20 20 -55.D0 235.D0 20  20\n"


            
        ouverture=open("consigne","w")
        ouverture.write(ligne1)
        ouverture.write(ligne2)
        ouverture.write(ligne3)    
        ouverture.write(ligne4)
        ouverture.close()

        time.sleep(1)
        os.system("robot.exe")
        

    def btn_plot7_callback(self):

        print("Angle en direct")
        ligne1="MODE De FONCTIONNEMENT (1:tetai,phii,tetao,phio   2:tetai,phii,delta,pas_gamma  3:tetai,phii,pas_delta,pas_gamma,1(hemisphere complet) ou 2(demihemisphere))\n"
        ligne2="Choisir mode\n"
        ligne3="les angles de consignes (en °) (teta [0;90] phi[-180;180] delta[90;270])\n"
        ligne4="Choisir les angels connu et l'angle cherché\n"
        print("Compiler")
        #os.system("robot.exe")
 

    def initialisation_xps(self):
        self.xps.kill_group()

        self.xps.initialize_allgroups()
        self.xps.home_allgroups()


 
    def connect_callback(self):
  
        #Initialisation moteur Newport
        self.xps=NewportXPS('169.254.200.150', username='Administrator', password='Administrator')
        self.info_newport.appendPlainText("***************************************")
    #    self.info_newport.appendPlainText(self.xps.status_report())
         


        
        #Initialisation robot Nyrio : échantillon 
        self.ned = NiryoRobot("169.254.200.200")
        self.ned.calibrate_auto()
 
        self.info_nyrio.appendPlainText(str(self.ned.get_hardware_status()))

 


        
        self.Valeur_det = Lockin() #instancie lockin

        self.initialisation = True
        self.a.setPixmap(self.c)
        self.tabs.setTabEnabled(self.tab_xps, True)
        self.tabs.setTabEnabled(self.tab_ned, True)


    
    def save_motif_callback(self):
        f=open('motif.dat','w')
        self.motif= [0.]
        f.write('{:12.10f}\n'.format(self.motif[0]))
        for ii in range(len(self.Rampe_IPW)):
	        self.motif.append(self.Rampe_IPW[ii] + self.motif[ii])
	        f.write('{:12.10f}\n'.format(self.Rampe_IPW[ii] + self.motif[ii]))
        f.close()
        print(self.motif)	
    

def main():
    app = QApplication(sys.argv)
    LIDR = BRDF()
    LIDR.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

