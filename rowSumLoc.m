function [xLoc, yLoc] = rowSumLoc(dominos, line, lineLength)

[~, numDoms] = size(line);
last = line(:, numDoms);

lastDom = dominos(last(1),:);
correct = lineLength * .25;

if (last(2) == 1)   % Horizontal
    
    xLoc = lastDom(4) + 1.5 * lineLength;
    yLoc = (lastDom(1) + lastDom(2))/2 - correct;
    
else

    xLoc = lastDom(4) + .5 * lineLength;
    
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