%This is the function that will detect each one of the dominos
%This would be a good starting point from my point of view
%Problem now is that it does not detect yellow dots on the dominos

function [corners] = dominoFinder(region, img)
region2 = imcomplement(region);
corners = region;

[B,L] = bwboundaries(region);

[height, width] = size(img);

% Find the number of circles in the image and average circumference
[numCells, ~] = size(B);

circles = 0;
mostCommonCirc = 0;

for i = 1 : numCells
    
    cellCirc = size(B{i}, 1);
    similarCells = 0;
    
    for j = 1 : numCells
        otherCirc = size(B{j}, 1);
        
        if (abs(cellCirc - otherCirc) < 50)
            similarCells = similarCells + 1;
        end
        
    end
    
    if (similarCells > circles)
        circles = similarCells;
        mostCommonCirc = cellCirc;
    end
    
end
    
sumOfCircs = 0;

% Find average circle size

for i = 1 : numCells
    circ = size(B{i}, 1);

    if (abs(mostCommonCirc - circ) < 50)
        sumOfCircs = sumOfCircs + circ;
    end
end

averageCircleSize = sumOfCircs/circles;


% Find center lines based off circle size

centerLineEstimate = 3 * averageCircleSize;

centerLines = B;

delete_these = zeros();
index = 1;

for i = 1 : numCells
    circ = size(B{i}, 1);

    if (abs(centerLineEstimate - circ) > 80)
        delete_these(index)=i;
        index=index+1;
    end
end

% Extract Center Lines
for i=1:length(delete_these)
   centerLines{delete_these(i)} = []; 
end
centerLines = centerLines(~cellfun('isempty',centerLines));

dominos = zeros(length(centerLines), 7);


% Extract dominos from center lines
% [ topLine bottomLine leftLine rightLine vert(0)/hor(1) top/leftDots
% bottom/rightDots]

numDominos = length(centerLines);

for i = 1 : numDominos
    
    % find the max values of the line.
    top = height;
    bottom = 0;
    left = width;
    right = 0;
    
    
    for j = 1 : length(centerLines{i})
        if (centerLines{i}(j,1) < top)
            top = centerLines{i}(j,1);
            topX = centerLines{i}(j,2);
        end
        if (centerLines{i}(j,1) > bottom)
            bottom = centerLines{i}(j,1);
        end
        if (centerLines{i}(j,2) < left)
            left = centerLines{i}(j,2);
        end
        if (centerLines{i}(j,2) > right)
            right = centerLines{i}(j,2);
        end
    end
    
    dominos(i, 1) = top;
    dominos(i, 2) = bottom;
    dominos(i, 3) = left;
    dominos(i, 4) = right;
    
    % Horizontal or vertical)
    lineLength = 0;
    if (abs(left - right) < abs(top - bottom))
        dominos(i, 5) = 1;
        lineLength = abs(top - bottom);
    else
        lineLength = abs(left - right);
    end
    
    %Get Domino Values
    topLeftDots = 0;
    bottomRightDots = 0;
    
    if (dominos(i,5) == 0) % Vertical Domino
        for j = 1 : numCells
            circ = size(B{j}, 1);

            if (abs(averageCircleSize - circ) < 50)
                xVal = B{j}(1,2);
                yVal = B{j}(1,1);
                
                e = .1*lineLength;
                
                leftLim = (left - e);
                rightLim = (right + e);
                topLim = (top - 1.15*lineLength);
                bottomLim = (bottom + 1.15*lineLength);
                
                
                if (yVal < top + e && yVal > topLim && xVal > leftLim && xVal < rightLim)
                    topLeftDots = topLeftDots + 1;
                end
                
                if (yVal > bottom - e && yVal < bottomLim && xVal > leftLim && xVal < rightLim)
                    bottomRightDots = bottomRightDots + 1;
                end
            end
        end
        
    else  % Horizontal Domino
        for j = 1 : numCells
            circ = size(B{j}, 1);

            if (abs(averageCircleSize - circ) < 50)
                xVal = B{j}(1,2);
                yVal = B{j}(1,1);
                
                e = .1*lineLength; %error
                
                topLim = (top - e);
                bottomLim = (bottom + e);
                leftLim = (left - 1.1*lineLength);
                rightLim = (right + 1.1*lineLength);
                
                if (xVal < left + e && xVal > leftLim && yVal > topLim && yVal < bottomLim)
                    topLeftDots = topLeftDots + 1;
                end
                
                if (xVal > right - e && xVal < rightLim && yVal > topLim && yVal < bottomLim)
                    bottomRightDots = bottomRightDots + 1;
                end
            end
        end
    end
    
    dominos(i, 6) = topLeftDots;
    dominos(i, 7) = bottomRightDots;
    
end




% Classify if dominos are in the same row or column

relations = adjHelper(dominos, lineLength);

adjacentDoms = relations;


% Get Rows

[rows, rowSums, rowEnds] = getRows(dominos, adjacentDoms);

% Get Cols
[cols, colSums, colEnds] = getCols(dominos, adjacentDoms);








imshow(label2rgb(L, @jet, [.5 .5 .5]))
hold on
index=1;
sum=0;
for k = 1:length(B)
   if size(B{k},1)>0
       sum=sum+1;
       index=index+1;
       boundary = B{k};
       plot(boundary(:,2), boundary(:,1), 'w', 'LineWidth', 2)
   end
end

sum = sum - (numDominos*2) -1;
disp(numDominos);
disp(sum);

end