% Finds all Cols with more than one domino and their sums
% 
% cols = cell[numCols x 1]
%
% Col = [2 x dominosInCol]
%    - Col[1, i] = domino number
%    - Col[2, i] = domino orientation w/ respect to Col
%           1 = Vertical
%           2 = top Horizontal
%           3 = bottom Horizontal
%           4 = Middle Horizontal
%
% 

function [cols, sums, ColEnds] = getCols(dominos, adjacentDoms)

[numDominos, ~] = size(dominos);

cols = cell(numDominos, 1);
numcols = 0;

% Get cols

for i = 1 : numDominos
    currDom = i;
    thisDom = dominos(i, :);
    top = i;
    orient = -1;
    nextOrient = -1;
    
    
    % Move top until we reach the beginning of the column.
    
    while (top ~= 0)
        currDom = top;
        orient = nextOrient;
        thisDom = dominos(top, :);
        if (thisDom(5) == 0)
            [top, nextOrient] = topDom(dominos, adjacentDoms, currDom, orient);
        else 
            [top, nextOrient] = topDom(dominos, adjacentDoms, currDom, 2);

            if (top == 0)
                [top, nextOrient] = topDom(dominos, adjacentDoms, currDom, 3);
            end
            if (top == 0)
                [top, nextOrient] = topDom(dominos, adjacentDoms, currDom, 4);
            end
        end
    end
             
    % Move down until we reach the end of the Col
    % If there is only one domino in the Col, don't add it to the Col
    % matrix. After adding the next domino to the Col, delete the
    % connection from the adjacentDoms matrix.
    
    thisCol = zeros(2,numDominos);
    dominosInCol = 1;
    
    
    if (orient ~= -1)
        thisCol(1,1) = currDom;
        thisCol(2,1) = orient;
        [bottom, nextOrient] = bottomDom(dominos, adjacentDoms, currDom, orient);
        
    else
        thisCol(1,1) = currDom;
        
        [bottom, nextOrient] = bottomDom(dominos, adjacentDoms, currDom, 1);
        thisCol(2,1) = 1;
        
        if (bottom == 0)
            
            [bottom, nextOrient] = bottomDom(dominos, adjacentDoms, currDom, 2);
             thisCol(2,1) = 2;
        end
        
        if (bottom == 0)
            [bottom, nextOrient] = bottomDom(dominos, adjacentDoms, currDom, 3);
            thisCol(2,1) = 3;
        end
        if (bottom == 0)
            [bottom, nextOrient] = bottomDom(dominos, adjacentDoms, currDom, 4);
            thisCol(2,1) = 4;
        end
    end
    
    % There is a multi-domino Col
    if (bottom > 0)
        
        while(bottom > 0)
            % Set adjacencies of dominos already in the Col to zero.
            adjacentDoms(currDom, bottom) = 0;
            adjacentDoms(bottom, currDom) = 0;
            
            currDom = bottom;
            orient = nextOrient;
            dominosInCol = dominosInCol + 1;
            
            thisCol(1, dominosInCol) = currDom;
            thisCol(2, dominosInCol) = orient;
            
            [bottom, nextOrient] = bottomDom(dominos, adjacentDoms, currDom, orient);
            
        end
        
        newCol = zeros(2, dominosInCol);
        
        for j = 1 : dominosInCol
            newCol(1,j) = thisCol(1,j);
            newCol(2,j) = thisCol(2,j);
        end
        
        numcols = numcols + 1;
        cols{numcols} = newCol;
        
    end  
end

temp = cell(numcols, 1);
for i = 1 : numcols
    temp{i} = cols{i};
end

cols = temp;

sums = zeros(numcols, 1);
ColEnds = zeros(numcols, 2); % [first, last]

% Find sums and end values of each Col
for i = 1 : numcols
    currCol = cols{i};
    [~, numDoms] = size(currCol);
    
    sum = 0;
    
    for j = 1 : numDoms
        currDom = dominos(currCol(1,j), :);
        currOrient = currCol(2,j);
        
        if (currOrient == 1)
            ColVal = currDom(6) + currDom(7);
            startVal = currDom(6);
            endVal = currDom(7);
        end
        if (currOrient == 2)
            ColVal = currDom(6);
            startVal = currDom(6);
            endVal = currDom(6);
        end
        if (currOrient == 3)
            ColVal = currDom(7);
            startVal = currDom(7);
            endVal = currDom(7);
        end
        if (currOrient == 4)
            ColVal = currDom(6) + currDom(7);
            startVal = currDom(6);
            endVal = currDom(6);
        end
        
        sum = sum + ColVal;
        
        if (j == 1)
            ColEnds(i, 1) = startVal;
        end
        if (j == numDoms)
            ColEnds(i, 2) = endVal;
        end
        
    end
    
    sums(i) = sum;
    
end

end

