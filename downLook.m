function[nextPx,nextPy,nextprev,truth] = downLook(traceRegion,currentPx,currentPy,prev,truth)  
    nextPx = currentPx;
    nextPy = currentPy;
    nextprev = prev;
    newtruth = 0;

    %Change direction clock-wise
    p1 = traceRegion(currentPx+1,currentPy+1);
    p2 = traceRegion(currentPx+1,currentPy);
    p3 = traceRegion(currentPx+1,currentPy-1);
    
    if(p1 == traceRegion(currentPx,currentPy)),
        nextPx = currentPx+1;
        nextPy = currentPy+1;
        nextprev(1) = currentPx+1;
        nextprev(2) = currentPy;
        truth = 1;
        return;
    end
    if(p2 == traceRegion(currentPx,currentPy)),
        nextPx = currentPx+1;
        nextPy = currentPy;
        nextprev(1) = currentPx;
        nextprev(2) = currentPy;
        truth = 1;
        return;
    end
    if(p3 == traceRegion(currentPx,currentPy)),
        nextPx = currentPx+1;
        nextPy = currentPy-1;
        nextprev(1) = currentPx+1;
        nextprev(2) = currentPy;
        truth = 1;
        return;
    end
end