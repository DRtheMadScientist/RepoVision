% Analyse PCA et Kmeans : Images visages / voitures
clc, close all, clear all

%% Répertoires et fichiers
    % Noms des répertoires images
    rep_voit = 'voitures'; 
    rep_vis = 'visages'; 

    % Enregistrement des noms des fichiers jpg dans ces répertoires
    nom_fich = dir(fullfile(rep_voit, '*.jpg'));
    nbre_fich_voit = size(nom_fich,1);
    noms_fich_voit = cell(nbre_fich_voit,1);
    for f = 1:nbre_fich_voit
        noms_fich_voit{f} = nom_fich(f).name;
    end

    nom_fich = dir(fullfile(rep_vis, '*.jpg'));
    nbre_fich_vis = size(nom_fich,1);
    noms_fich_vis = cell(nbre_fich_vis,1);
    for f = 1:nbre_fich_vis
        noms_fich_vis{f} = nom_fich(f).name;
    end

%% Extraction des descripteurs locaux (SIFT)

    pas=15;
    taille_patch=80;
    nbre_images=50;
	if (1)
		tsift_voit=[];
		tpos_voit=[];
		for i=1:nbre_images
			im=imread(fullfile(rep_voit, noms_fich_voit{i}));
			[sift,pos] = sift_dense(im, pas, taille_patch);
			tsift_voit=[tsift_voit ;sift];
			tpos_voit=[tpos_voit ;pos];
		end
		tsift_vis=[];
		tpos_vis=[];
		for i=1:nbre_images
			im=imread(fullfile(rep_vis, noms_fich_vis{i}));
			[sift,pos] = sift_dense(im, pas, taille_patch);
			tsift_vis=[tsift_vis;sift];
			tpos_vis=[tpos_vis ;pos];
		end
		tsift=[tsift_voit;tsift_vis];
		tpos=[tpos_voit;tpos_vis];
		save('SIFT','tsift','tpos');
	else
		load SIFT
    end
  
    % L’objectif est d’analyser les descripteurs locaux (SIFT) issus des images de visages et des images de voitures. 
    % Nous allons pour cela travailler avec un échantillon de 100 images contenant 50 images de visages ainsi que 50 images de voitures.
    %% 1/ Analyse en composantes principales
    %% 1 a) On centre les données à l'aide des instructions suivantes 
    n = size(tsift,1);
    m = mean(tsift);
    Xc = tsift -repmat(m,n,1);
    %% 1 b) On calcule la matrice de covariance à l'aide de la fonction cov
    C =cov(Xc);
    
    
    %% 1 c) On calcule les vecteurs et valeurs propres de la matrice de covariance à l'aide de la fonction eig
    [V,D]=eig(C);
    
 
    %% 1 d) On ordonne les valeurs propres et vecteurs propres à l'aide de la fonction sort et de l'option descend
    d = diag(D);
    v = diag(V);
    [ds,ids] = sort(d,'descend');% Ordonnancement des valeurs propre
    [vs,ivs] = sort(v,'descend');% Ordonnancement des vecteurs propre
    Vord=V(:,ids);
    %% 1 e) On observe l'évolution des variances
    VAR = ds/sum(ds);
    figure();
    plot(cumsum(VAR));

    
    %% 1 f) La dimension minimale pour conserver 80% de la variance totale est 28.
    % Voir courbe
    %% 1 g) Comparaison Xn avec pca
    % Xn = Xc * Vord;
    
    % XN = Xc *Vord;
    %% 1 h) La matrice Xn de taille 37500x2 contient les dimensions les plus importantes 
    XN = Xc* Vord(:,1:2);
    Xnp=pca(tsift);
    
    %% 1 i) Descripteurs locaux des 2 classes (visages et voitures)
    figure, hold on
    plot(XN(1:n/2,1),XN(1:n/2,2),'.r');
    plot(XN(n/2+1:end,1),XN(n/2+1:end,2),'.b');
    legend({'SIFT voiture', 'SIFT visage'},'Location','northeast');
    
    
   
    