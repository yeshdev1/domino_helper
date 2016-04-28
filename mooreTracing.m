function [B,L] = mooreTracing(region)
B = {};
L = {};

traceRegion = region; % changing the binary region by placing a -1 one in place of the border starting value
marker = zeros(size(traceRegion)); %Use this adjacent matrix / overlapping matrix

%disp(traceRegion(590:630,1970:2000));

[x,y] = size(region);
numcells = 0; % Current cell of B

for i = 1:x,
    for j = 1:y,

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if(and(j + 1 < y,i + 1 < x)),
            entryLocation = []; 
            s = []; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if((traceRegion(i,j+1) == 0) && traceRegion(i,j) ~= traceRegion(i,j+1) && marker(i,j+1)~=-1), %white to black detection
                numcells = numcells + 1;
                numRows = 1;
                prev = [];
                entryLocation(1) = i;
                entryLocation(2) = j;
                s(1) = i;
                s(2) = j+1;
                prev(1) = i;
                prev(2) = j;
                currentPx = s(1);
                currentPy = s(2);
                B{numcells}(numRows,1) = currentPx;
                B{numcells}(numRows,2) = currentPy;
                marker(currentPx,currentPy) = -1;
                
                numRows = numRows + 1;
                [currentPx,currentPy,prev] = getNeighbourhood(traceRegion,currentPx,currentPy,prev);
                B{numcells}(numRows,1) = currentPx;
                B{numcells}(numRows,2) = currentPy;
                marker(currentPx,currentPy) = -1;
                
                while (s(1) ~= currentPx) | (s(2)~=currentPy),
                    numRows = numRows + 1;
                    [currentPx,currentPy,prev] = getNeighbourhood(traceRegion,currentPx,currentPy,prev);
                    B{numcells}(numRows,1) = currentPx;
                    B{numcells}(numRows,2) = currentPy;
                    marker(currentPx,currentPy) = -1;
                end
%                 disp(B{2});
%                 imshow(region);
%                 hold on
%                 boundary = B{8};
%                 plot(boundary(:,2), boundary(:,1), 'r', 'LineWidth', 2) 
            end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        end
    end
end

end