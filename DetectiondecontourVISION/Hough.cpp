#include <iostream>
#include "math.h"
#include "ImageNdg.h"
#include "ImageCouleur.h"
#include "ImageClasse.h"
#include "ImageDouble.h"

int main(void)
{
	// Détection des contours
	CImageNdg img("hough3.bmp");
	CImageDouble imgD(img, "normalise");
	CImageDouble imgG = imgD.vecteurGradient("norme");
	CImageNdg imgCont = imgG.toNdg("expansion").seuillage("otsu");

	imgCont.sauvegarde("res");
	// Application de la transformée de Hough
	int y = imgCont.lireHauteur();
	int x = imgCont.lireLargeur();
	int diag = sqrt((x*x)+(y*y))+0.5;
	float Rho, Theta, max;

	CImageDouble imgTDH(diag,180);

	for (int i = 0; i < x; i++)
	{
		for (int j = 0; j < y; j++)
		{
			if (imgCont(j,i) != 0)
			for (Theta = 0; Theta<180; Theta++)
			{
				Rho = ((i-(x/2))*cos((Theta*acos(-1)/180))+(j-(y/2))*sin((Theta * acos(-1) / 180)));
				imgTDH((diag/2)-Rho, Theta) +=1;				
				imgTDH.ecrireMax((imgTDH.lireMax() < imgTDH((diag/2) - Rho, Theta)) ? imgTDH((diag/2) - Rho, Theta) : imgTDH.lireMax());
			}
		}
	}
	CImageNdg imgTDHough = imgTDH.toNdg();
	imgTDHough.sauvegarde("res");
	


}