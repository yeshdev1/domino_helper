function[nextPx,nextPy,nextprev,newtruth] = rightLook(traceRegion,currentPx,currentPy,prev,truth)
    
    nextPx = currentPx;
    nextPy = currentPy;
    nextprev = prev;
    newtruth = 0;

    p1 = traceRegion(currentPx-1,currentPy+1);
    p2 = traceRegion(currentPx,currentPy+1);
    p3 = traceRegion(currentPx+1,currentPy+1);
    
    if(p1 == traceRegion(currentPx,currentPy)),
        nextPx = currentPx-1;
        nextPy = currentPy+1;
        nextprev(1) = currentPx;
        nextprev(2) = currentPy+1;
        newtruth = 1;
        return;
    end
    if(p2 == traceRegion(currentPx,currentPy)),
        nextPx = currentPx;
        nextPy = currentPy+1;
        nextprev(1) = currentPx;
        nextprev(2) = currentPy;
        newtruth = 1;
        return;
    end
    if(p3 == traceRegion(currentPx,currentPy)),
        nextPx = currentPx+1;
        nextPy = currentPy+1;
        nextprev(1) = currentPx;
        nextprev(2) = currentPy+1;
        newtruth = 1;
        return;
    end
end