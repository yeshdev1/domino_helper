%Path to the directory
image1 = fullfile('data','black_dominos.jpg');

imdata = imread(image1);
imdata = rgb2gray(imdata);
imdata = im2double(imdata);

[B,L,N] = bwboundaries(imdata);
disp(N);