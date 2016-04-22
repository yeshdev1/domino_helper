% Return domino to the left
function [domino, orientation] = leftDom(dominos, adjacencies, currDom, rowOrient)
numDominos = length(adjacencies);
thisDom = dominos(currDom, :);
domino = 0;
orientation = 0;

for i = 1 : numDominos
    otherDom = dominos(i,:);
    if (adjacencies(currDom,i) ~=0)
        type = adjacencies(currDom, i);
        if (thisDom(5) == 1) % thisDom = Horizontal
            if (otherDom(5) == 1) % otherDom = Horizontal
                if (type == 2)
                    domino = i;
                    orientation = 1;
                    return;
                end

            else % otherDom = vertical
                if (type == 4)
                    domino = i;
                    orientation = 3;
                    return;
                end
                if (type == 5)
                    domino = i;
                    orientation = 2;
                    return;
                end
                if (type == 6)
                    domino = i;
                    orientation = 4;
                    return;
                end
            end
        else % ThisDom = vertical
            if (rowOrient == 2) % Checking for a top row
                if (otherDom(5) == 1) % otherDom is horizontal
                    if (type == 4)
                        domino = i;
                        orientation = 1;
                        return;
                    end
                else % otherDom is vertical
                    if (type == 4)
                        domino = i;
                        orientation = 3;
                        return;
                    end
                end
            end
                
            if (rowOrient == 3) % Checking for bottom row
                if (otherDom(5) == 1) % otherDom is horizontal
                    if (type == 5)
                        domino = i;
                        orientation = 1;
                        return;
                    end
                else % otherDom is vertical
                    if (type == 6)
                        domino = i;
                        orientation = 2;
                        return;
                    end
                end
            end
            
            if (rowOrient == 4) % Checking middle row
                 if (otherDom(5) == 1) % otherDom is horizontal
                    if (type == 6)
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