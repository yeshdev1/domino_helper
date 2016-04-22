% Return domino to the top
function [domino, orientation] = topDom(dominos, adjacencies, currDom, rowOrient)
numDominos = length(adjacencies);
thisDom = dominos(currDom, :);
domino = 0;
orientation = 0;

for i = 1 : numDominos
    otherDom = dominos(i,:);
    if (adjacencies(currDom,i) ~=0)
        type = adjacencies(currDom, i);
        if (thisDom(5) == 0) % thisDom = Vertical
            if (otherDom(5) == 0) % otherDom = Vertical
                if (type == 1)
                    domino = i;
                    orientation = 1;
                    return;
                end

            else % otherDom = horizontal
                if (type == 7)
                    domino = i;
                    orientation = 2;
                    return;
                end
                if (type == 8)
                    domino = i;
                    orientation = 3;
                    return;
                end
                if (type == 9)
                    domino = i;
                    orientation = 4;
                    return;
                end
            end
        else % ThisDom = horizontal
            if (rowOrient == 3) % Checking for a right col
                if (otherDom(5) == 0) % otherDom is vertical
                    if (type == 7)
                        domino = i;
                        orientation = 1;
                        return;
                    end
                else % otherDom is horizontal
                    if (type == 3)
                        domino = i;
                        orientation = 3;
                        return;
                    end
                end
            end
                
            if (rowOrient == 2) % Checking for left col
                if (otherDom(5) == 0) % otherDom is vertical
                    if (type == 8)
                        domino = i;
                        orientation = 1;
                        return;
                    end
                else % otherDom is horizontal
                    if (type == 4)
                        domino = i;
                        orientation = 2;
                        return;
                    end
                end
            end
            
            if (rowOrient == 4) % Checking middle col
                 if (otherDom(5) == 0) % otherDom is vertical
                    if (type == 9)
                        domino = i;
                        orientation = 1;
                        return;
                    end
                 end
            end
        end
    end  
end

end