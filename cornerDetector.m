%This is the function that will detect each one of the dominos
%This would be a good starting point from my point of view
%Problem now is that it does not detect yellow dots on the dominos

function [corners] = cornerDetector(region)
image1 = fullfile('data','Domino_game.jpg');
region2 = imcomplement(region);
corners = region;

[B,L] = bwboundaries(region,'noholes');
disp(B);
imshow(label2rgb(L, @jet, [.5 .5 .5]))
hold on
for k = 1:length(B)
   boundary = B{k};
   plot(boundary(:,2), boundary(:,1), 'w', 'LineWidth', 2)
end

end