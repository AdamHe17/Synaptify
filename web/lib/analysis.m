function [ridge_x, ridge_y, bifurcation_x, bifurcation_y] = analysis(image_path)

%Read Input Image
binary_image=im2bw(imread(image_path));

%Small region is taken to show output clear
binary_image = binary_image(20:120, 20:120);

%Thinning
thin_image=~bwmorph(binary_image,'thin',Inf);

%Minutiae extraction
s=size(thin_image);
N=3;%window size
n=(N-1)/2;
r=s(1)+2*n;
c=s(2)+2*n;
double temp(r,c);
temp=zeros(r,c);bifurcation=zeros(r,c);ridge=zeros(r,c);
temp((n+1):(end-n),(n+1):(end-n))=thin_image(:,:);
for x=(n+1+10):(s(1)+n-10)
    for y=(n+1+10):(s(2)+n-10)
        e=1;
        for k=x-n:x+n
            f=1;
            for l=y-n:y+n
                mat(e,f)=temp(k,l);
                f=f+1;
            end
            e=e+1;
        end;
         if(mat(2,2)==0)
            ridge(x,y)=sum(sum(~mat));
            bifurcation(x,y)=sum(sum(~mat));
         end
    end;
end;

% RIDGE END FINDING (end)
[ridge_x, ridge_y]=find(ridge==2);

%BIFURCATION FINDING (split)
[bifurcation_x, bifurcation_y]=find(bifurcation==4);

end