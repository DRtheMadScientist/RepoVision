function display_visual_word(center,Xn,tpos,rep_voit,rep_vis,noms_fich_voit,noms_fich_vis,taille_patch)

dist_mat = matrice_dist(center,Xn);
[~,ind]=sort(dist_mat);
for i=1:10
    num_im=ceil(ind(i)/375);
    if num_im<51
        rep=rep_voit;
        nom_fich=noms_fich_voit{num_im};
    else
        rep=rep_vis;
        nom_fich=noms_fich_vis{num_im-50};
    end
    im=imread(fullfile(rep, nom_fich));
    figure(100), subplot(2,5,i)
    imshow(im); 
    hold on
    rectangle('position',[tpos(ind(i),2)-taille_patch*0.5,tpos(ind(i),1)-taille_patch*0.5,taille_patch,taille_patch]);
end
    
