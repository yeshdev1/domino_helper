%This is the main function where all the parts of the project is put
%togethor.
%P.S : Please read the comments on top of each of the functions called as
%it is a detailed walkthrough of what exactly it is that is being done so
%that the image is set up for the next function
region = gameRegion;

imshow(region);

corners = cornerDetector(region);