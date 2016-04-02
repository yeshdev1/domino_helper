%Path to the directory
image1 = fullfile('data','game_picture2.jpg');

imdata = imread(image1);
imdata = rgb2gray(imdata);
imdata = im2double(imdata);

BW = imbinarize(imdata);

[B,L] = bwboundaries(BW,'noholes');

imshow(label2rgb(L, @jet, [.6 .6 .6]))
hold on
for k = 1:length(B)
   boundary = B{k};
   plot(boundary(:,2), boundary(:,1), 'w', 'LineWidth', 2)
end