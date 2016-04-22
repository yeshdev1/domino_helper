function [xLoc, yLoc] = colSumLoc(dominos, line, lineLength)

[~, numDoms] = size(line);
last = line(:, numDoms);

lastDom = dominos(last(1),:);
correct = 0;

if (last(2) == 1)   % Vertical
    
    yLoc = lastDom(2) + 2* lineLength;
    xLoc = (lastDom(1) + lastDom(2))/2 - correct;
    
else

    yLoc = lastDom(2) + lineLength;
    
    if (last(2) == 2)   % Left
        xLoc = lastDom(3) - .5 * lineLength - correct;
    end

    if (last(2) == 3)   % Right
        xLoc = lastDom(4) + .5 * lineLength - correct;
    end

    if (last(2) == 4)   % Middle
        xLoc = lastDom(3) - correct;
    end
end



end