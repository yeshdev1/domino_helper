% Finds all rows with more than one domino and their sums
% 
% Rows = cell[numRows x 1]
%
% row = [2 x dominosInRow]
%    - row[1, i] = domino number
%    - row[2, i] = domino orientation w/ respect to row
%           1 = horizontal
%           2 = Top Vertical
%           3 = Bottom Vertical
%           4 = Middle Vertical
%
% 

function [rows, sums, rowEnds] = getRows(dominos, adjacentDoms)

[numDominos, ~] = size(dominos);

rows = cell(numDominos, 1);
numRows = 0;

% Get Rows

for i = 1 : numDominos
    currDom = i;
    thisDom = dominos(i, :);
    left = i;
    orient = -1;
    nextOrient = -1;
    
    % Move left until we reach the beginning of the column.
    
    while (left ~= 0)
        currDom = left;
        orient = nextOrient;
        thisDom = dominos(left, :);
        if (thisDom(5) == 1) 
            [left, nextOrient] = leftDom(dominos, adjacentDoms, currDom, orient);
            
            if (left > 0)
                currDom = left;
            end
        else 
            if (orient ~= -1)
                [left, nextOrient] = leftDom(dominos, adjacentDoms, currDom, orient);
            else
                [left, nextOrient] = leftDom(dominos, adjacentDoms, currDom, 2);
                
                if (left == 0)
                    [left, nextOrient] = leftDom(dominos, adjacentDoms, currDom, 3);
                end
                if (left == 0)
                    [left, nextOrient] = leftDom(dominos, adjacentDoms, currDom, 4);
                end
            end
        end
    end
             
    % Move right until we reach the end of the row
    % If there is only one domino in the row, don't add it to the row
    % matrix. After adding the next domino to the row, delete the
    % connection from the adjacentDoms matrix.
    
    thisRow = zeros(2,numDominos);
    dominosInRow = 1;
    
    
    if (orient ~= -1)
        thisRow(1,1) = currDom;
        thisRow(2,1) = orient;
        [right, nextOrient] = rightDom(dominos, adjacentDoms, currDom, orient);
        
    else
        thisRow(1,1) = currDom;
        
        [right, nextOrient] = rightDom(dominos, adjacentDoms, currDom, 1);
        thisRow(2,1) = 1;
        
        if (right == 0)
            
            [right, nextOrient] = rightDom(dominos, adjacentDoms, currDom, 2);
             thisRow(2,1) = 2;
        end
        
        if (right == 0)
            [right, nextOrient] = rightDom(dominos, adjacentDoms, currDom, 3);
            thisRow(2,1) = 3;
        end
        if (right == 0)
            [right, nextOrient] = rightDom(dominos, adjacentDoms, currDom, 4);
            thisRow(2,1) = 4;
        end
    end
    
    % There is a multi-domino row
    if (right > 0)
        
        while(right > 0)
            % Set adjacencies of dominos already in the row to zero.
            adjacentDoms(currDom, right) = 0;
            adjacentDoms(right, currDom) = 0;
            
            currDom = right;
            orient = nextOrient;
            dominosInRow = dominosInRow + 1;
            
            thisRow(1, dominosInRow) = currDom;
            thisRow(2, dominosInRow) = orient;
            
            [right, nextOrient] = rightDom(dominos, adjacentDoms, currDom, orient);
            
        end
        
        newRow = zeros(2, dominosInRow);
        
        for j = 1 : dominosInRow
            newRow(1,j) = thisRow(1,j);
            newRow(2,j) = thisRow(2,j);
        end
        
        numRows = numRows + 1;
        rows{numRows} = newRow;
        
    end  
end

temp = cell(numRows, 1);
for i = 1 : numRows
    temp{i} = rows{i};
end

rows = temp;

sums = zeros(numRows, 1);
rowEnds = zeros(numRows, 2); % [first, last]

% Find sums and end values of each row
for i = 1 : numRows
    currRow = rows{i};
    [~, numDoms] = size(currRow);
    
    sum = 0;
    
    for j = 1 : numDoms
        currDom = dominos(currRow(1,j), :);
        currOrient = currRow(2,j);
        
        if (currOrient == 1)
            rowVal = currDom(6) + currDom(7);
            startVal = currDom(6);
            endVal = currDom(7);
        end
        if (currOrient == 2)
            rowVal = currDom(6);
            startVal = currDom(6);
            endVal = currDom(6);
        end
        if (currOrient == 3)
            rowVal = currDom(7);
            startVal = currDom(7);
            endVal = currDom(7);
        end
        if (currOrient == 4)
            rowVal = currDom(6) + currDom(7);
            startVal = currDom(6);
            endVal = currDom(6);
        end
        
        sum = sum + rowVal;
        
        if (j == 1)
            rowEnds(i, 1) = startVal;
        end
        if (j == numDoms)
            rowEnds(i, 2) = endVal;
        end
        
    end
    
    sums(i) = sum;
    
end

end

