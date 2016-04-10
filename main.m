%This is the main function where all the parts of the project is put
%togethor.
%P.S : Please read the comments on top of each of the functions called as
%it is a detailed walkthrough of what exactly it is that is being done so
%that the image is set up for the next function



selector = 5;

image1 = 'IMG_0660.JPG';
image2 = 'IMG_4421.JPG';
image3 = 'IMG_4759.JPG';
image4 = 'IMG_7010.JPG';
image5 = 'IMG_4384.JPG'; 

dataDir = fullfile('data');

if (selector == 1)
    img = imread(fullfile(dataDir, image1));
end
if (selector == 2)
     img = imread(fullfile(dataDir, image2));  
end
if (selector == 3)
    img = imread(fullfile(dataDir, image3));
end
if (selector == 4)
    img = imread(fullfile(dataDir, image4));
end
if (selector == 5)
    img = imread(fullfile(dataDir, image5));
end    


region = gameRegion(img);

imshow(region);

dominos = dominoFinder(region, img);

