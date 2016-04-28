function [B,L] = theoTracing(region)
B = {};
L = {};

traceRegion = region; 
marker = zeros(size(traceRegion));

disp(traceRegion(600:620,1980:2000));
% disp(1);

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
                
                if numcells == 10,
                    disp(currentPx);
                    disp(currentPy);
                    disp(1);
                end
                
                numRows = numRows + 1;
                [currentPx,currentPy,prev] = getTheoNeighbourhood(traceRegion,currentPx,currentPy,prev);
                B{numcells}(numRows,1) = currentPx;
                B{numcells}(numRows,2) = currentPy;
                marker(currentPx,currentPy) = -1;
                
                if numcells == 10,
                    n = 0;
                    while n < 20,
                        numRows = numRows + 1;
                        [currentPx,currentPy,prev] = getTheoNeighbourhood(traceRegion,currentPx,currentPy,prev);
                        B{numcells}(numRows,1) = currentPx;
                        B{numcells}(numRows,2) = currentPy;
                        marker(currentPx,currentPy) = -1;
                        n = n + 1;
                    end
                end
                
                if numcells == 10,
                    disp(B{10});
                    imshow(region);
                    hold on
                    boundary = B{10};
                    plot(boundary(:,2), boundary(:,1), 'r', 'LineWidth', 2);
                    disp(1);
                end
                
                n = 0;
                while n < 12000, %(s(1) ~= currentPx) | (s(2)~=currentPy),
                    numRows = numRows + 1;
                    [currentPx,currentPy,prev] = getTheoNeighbourhood(traceRegion,currentPx,currentPy,prev);
                    B{numcells}(numRows,1) = currentPx;
                    B{numcells}(numRows,2) = currentPy;
                    marker(currentPx,currentPy) = -1;
                    n = n + 1;
                end
            end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        end
    end
end

end