% reconstruction code third attempt
clc;clear;
M=readmatrix('velocity5lps.csv');
n=size(M,1);
alpha=rand(8,1);
alpha=alpha./sum(alpha);
coordinates=zeros(1,3);
anchor1_0=[104,12,-351];
anchor2_1=[-112,278,-351];
anchor7_2=[393,17.89,285];
anchor5_3=[-180,289,279];
anchor4_4=[-180,285.5,-350];
anchor6_7=[-180,289,279];
anchor8_5=[393,285,300.35];
anchor3_6=[-172,11.5,-351];
anchor_positions=[anchor1_0;anchor2_1;anchor7_2;anchor5_3;anchor4_4;anchor6_7;anchor8_5;anchor3_6]./100;
if mod(n,2)==0
    for i=1:n/2-1
        ranges=M(2*i+1,2:9);
        y=zeros(1,8);
        Cp=zeros(8,3);
        for j=1:8
           y(j)=0.5*(abs(ranges(j)^2-(anchor_positions(j,1)^2+anchor_positions(j,2)^2+anchor_positions(j,3)^2)));
           for k=1:8
               Cp(j,:)=Cp(j,:)+alpha(k)*(anchor_positions(k,:)-anchor_positions(j,:));
           end    
        end 
        y0=y*alpha;
        y=y-y0;
        coordinates(end+1,:)=pinv(Cp)*y';
    end    
else   
    for i=1:(n-1)/2
        ranges=M(2*i+1,2:9);
        y=zeros(1,8);
        Cp=zeros(8,3);
        for j=1:8
           y(j)=0.5*(abs(ranges(j)^2-(anchor_positions(j,1)^2+anchor_positions(j,2)^2+anchor_positions(j,3)^2)));
           for k=1:8
               Cp(j,:)=Cp(j,:)+alpha(k)*(anchor_positions(k,:)-anchor_positions(j,:));
           end    
        end 
        y0=y*alpha;
        y=y-y0;
        coordinates(end+1,:)=pinv(Cp)*y';

    end
end    
figure();
%plot3(coordinates(2:end,1).*1000,coordinates(2:end,3).*1000,coordinates(2:end,2).*1000);
scatter(coordinates(2:end,1).*1000,coordinates(2:end,3).*1000);