function[nextPx,nextPy,nextprev] = getNeighbourhood(traceRegion,currentPx,currentPy,prev)

currentPrev = prev;
nextprev = prev;
nextPx = currentPx;
nextPy = currentPy;
nextRegion = traceRegion;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Going left and up for the tracing
if(prev(2) < currentPy && prev(1) == currentPx),
    
    %1
    currentPrev(1) = currentPrev(1) - 1;
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        %You have a hit and prev remains the same
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        return;
    else
        %2
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) - 1;
        return;
    else
        %3
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) - 1;
        return;
    else
        %4
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) - 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %5
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) - 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %6
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) + 1;
        return;
    else
        %7
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) + 1;
        return;
    else
        %8
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    %If it reaches the end the border is most likely just 1 pixel wide
    
    return;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This is for right and down
elseif(prev(2) > currentPy && prev(1) == currentPx),
    
        %1
    currentPrev(1) = currentPrev(1) + 1;
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        %You have a hit and prev remains the same
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        return;
    else
        %2
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) + 1;
        return;
    else
        %3
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) + 1;
        return;
    else
        %4
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) + 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %5
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) + 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %6
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) - 1;
        return;
    else
        %7
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) - 1;
        return;
    else
        %8
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    %If it reaches the end the border is most likely just 1 pixel wide
    
    return;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
elseif(prev(1) < currentPx && prev(2) == currentPy),
    
        %1
    currentPrev(2) = currentPrev(2) + 1;
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        %You have a hit and prev remains the same
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        return;
    else
        %2
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) - 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %3
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) - 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %4
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) + 1;
        return;
    else
        %5
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) + 1;
        return;
    else
        %6
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) + 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %7
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) + 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %8
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    %If it reaches the end the border is most likely just 1 pixel wide
    
    return;

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
elseif(prev(1) > currentPx && prev(2) == currentPy),
        %1
    currentPrev(2) = currentPrev(2) - 1;
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        %You have a hit and prev remains the same
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        return;
    else
        %2
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) + 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %3
        currentPrev(1) = currentPrev(1) - 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) + 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %4
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) - 1;
        return;
    else
        %5
        currentPrev(2) = currentPrev(2) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1);
        nextprev(2) = currentPrev(2) - 1;
        return;
    else
        %6
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) - 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %7
        currentPrev(1) = currentPrev(1) + 1;
    end
    
    if(traceRegion(currentPrev(1),currentPrev(2)) ~= traceRegion(prev(1),prev(2))),
        nextPx = currentPrev(1);
        nextPy = currentPrev(2);
        nextprev(1) = currentPrev(1) - 1;
        nextprev(2) = currentPrev(2);
        return;
    else
        %8
        currentPrev(2) = currentPrev(2) - 1;
    end
    
    %If it reaches the end the border is most likely just 1 pixel wide
    
    return;
    
end
end