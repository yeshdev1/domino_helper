function [xLoc, yLoc] = rowSumLoc(dominos, line, lineLength)

[~, numDoms] = size(line);
last = line(:, numDoms);

lastDom = dominos(last(1),:);
correct = 0;

if (last(2) == 1)   % Horizontal
    
    xLoc = lastDom(4) + 2* lineLength;
    yLoc = (lastDom(1) + lastDom(2))/2 - correct;
    
else

    xLoc = lastDom(4) + lineLength;
    
    if (last(2) == 2)   % Top
        yLoc = lastDom(1) - .5 * lineLength - correct;
    end

    if (last(2) == 3)   % Bottom
        yLoc = lastDom(1) + .5 * lineLength - correct;
    end

    if (last(2) == 4)   % Middle
        yLoc = lastDom(1) - correct;
    end
end



end