function[nextPx,nextPy,nextprev] = getNeighbourhood(traceRegion,currentPx,currentPy,prev)

p1 = 0;
p2 = 0;
p3 = 0;
truth = 0;
nextPx = currentPx;
nextPy = currentPy;
nextprev = prev;

%Change prev once done
%account for all the angles
%account for all 3 pixels
%report the next tile 

%determining the orientation of the location pin
if(prev(1) == currentPx && prev(2) < currentPy),
    
    [nextPx,nextPy,nextprev,truth] = rightLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = downLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = leftlookup(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = upLook(traceRegion,currentPx,currentPy,prev,truth);
    return;

elseif(prev(1) == currentPx && prev(2) > currentPy),
    
    [nextPx,nextPy,nextprev,truth] = leftlookup(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = upLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = rightLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = downLook(traceRegion,currentPx,currentPy,prev,truth);
    return;
    
    
elseif(prev(1) > currentPx && prev(2) == currentPy),
    [nextPx,nextPy,nextprev,truth] = upLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = rightLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = downLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = leftlookup(traceRegion,currentPx,currentPy,prev,truth);
    return;
    
elseif(prev(1) < currentPx && prev(2) == currentPy),
    
    [nextPx,nextPy,nextprev,truth] = downLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = leftlookup(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = upLook(traceRegion,currentPx,currentPy,prev,truth);
    if(truth == 1),
        return;
    end
    
    [nextPx,nextPy,nextprev,truth] = rightLook(traceRegion,currentPx,currentPy,prev,truth);
    return;
    
end

end