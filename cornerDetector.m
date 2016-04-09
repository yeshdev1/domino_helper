%This is the function that will detect each one of the dominos
%This would be a good starting point from my point of view
%Problem now is that it does not detect yellow dots on the dominos

function [corners] = cornerDetector(region)
image1 = fullfile('data','five_dominos.jpg');
region2 = imcomplement(region);
corners = region;

[B,L] = bwboundaries(region);


delete_these = zeros();
index = 1;

%threshld for domino size
%start at 2 to neglect image border
max=1500;
for i = 2:length(B)
    if(size(B{i},1)>max)
        max=size(B{i},1);
    end
    disp(max);
end

%count dominos, remove noise
num_dominos=0;
for i = 1:length(B)
   temp = size(B{i});
   if temp(1)<100
       delete_these(index)=i;
       index=index+1;
   end
   
   if(temp(1)>(0.75*max))
       num_dominos=num_dominos+1;
   end
end

num_dominos=num_dominos-1; %This discounts the border

%remove noise
for i=1:length(delete_these)
   B{delete_these(i)} = []; 
end
B(~cellfun('isempty',B)) ;



imshow(label2rgb(L, @jet, [.5 .5 .5]))
hold on
index=1;
sum=0;
for k = 1:length(B)
   if size(B{k},1)>0
       sum=sum+1;
       index=index+1;
       boundary = B{k};
       plot(boundary(:,2), boundary(:,1), 'w', 'LineWidth', 2)
   end
end

sum = sum - (num_dominos*2) -1;
disp(num_dominos);
disp(sum);

end