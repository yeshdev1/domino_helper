%This is the function that will detect each one of the dominos
%This would be a good starting point from my point of view
%Problem now is that it does not detect yellow dots on the dominos

image1 = fullfile('data','Domino_game.jpg');
imdata = imread(image1);
imdata = rgb2gray(imdata);

imdata = 255 - imdata;

BW = imbinarize(imdata,'adaptive','ForegroundPolarity','dark','Sensitivity',0.57);

e = imfill(BW,[3 3], 8);

f = bwlabel(e);

imshow(f);