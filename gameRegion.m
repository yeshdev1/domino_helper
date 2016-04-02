%This is the function that will detect each one of the dominos
%This would be a good starting point from my point of view
%Problem now is that it does not detect yellow dots on the dominos

image1 = fullfile('data','game_picture1.jpg');
imdata = imread(image1);
imdata = rgb2gray(imdata);

imdata = 255 - imdata;

BW = imbinarize(imdata,'adaptive','ForegroundPolarity','dark','Sensitivity',0.55);

e = imfill(BW,'holes');

f = bwlabel(e);

imshow(f);