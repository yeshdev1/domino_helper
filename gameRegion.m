%This is the function that will detect each one of the dominos
%This would be a good starting point from my point of view
%Problem now is that it does not detect yellow dots on the dominos

function [region] = gameRegion(img)

aveFilter = fspecial('average', [25 25]);
img= imfilter(img, aveFilter, 'replicate');

imdata = rgb2gray(img);
threshold = graythresh(imdata);
BW = im2bw(imdata,threshold);
imshow(BW);
BW = ~ BW;
region = BW;

end