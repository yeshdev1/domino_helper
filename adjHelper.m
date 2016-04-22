% Classify if dominos adjacencies

function [relations] = adjHelper(dominos, lineLength)

[numDominos, ~] = size(dominos);

relations = zeros(numDominos);

% 2 Verticals: 1 = SCT, 2 = SCB, 3 = SRTR, 4 = SRTL, 5 =SRBR, 6=SRBL

% 2 Horizontals: 1 = SRR, 2 = SRL, 3 = SCTR, 4 = SCTL, 5 = SCBR, SCBL

% Vert & Hor: 1 = SRTR, 2 = SRBR, 3 = SRER, 4 = SRTL, 5 = SRBL, 6 = SREL
%            7 = SCTR, 8 = SCTL, 9 = SCTE, 10 = SCBR, 11 = SCBL, 12 = SCBE

err = .25*lineLength;
lineLength = 1.1*lineLength;

for i = 1 : numDominos
    for j = 1 : numDominos
        d1 = dominos(i,:);
        d2 = dominos(j,:);
        if (d1(5) == 0) % I is vertical
            if (d2(5) == 0) % J is vertical
                
                %Same Col Top
                if (abs(d1(3) - d2(3)) < err && abs(d1(1)-2.1*lineLength - d2(2)) < err)
                    relations(i,j) = 1;
                end
                
                
                %Same Col Bottom
                if (abs(d1(3) - d2(3)) < err && abs(d1(1)+2.1*lineLength - d2(2)) < err)
                    relations(i,j) = 2;
                end
                
                % Same Row Top Right
                if (abs((d1(1)-lineLength) - d2(1)) < err && abs((d1(4)+.2*lineLength)-d2(3)) < err)
                    relations(i,j) = 3;
                end
                
                % Same Row Top Left
                if (abs((d1(1)-lineLength) - d2(1)) < err && abs((d1(3)-.2*lineLength)-d2(4)) < err)
                    relations(i,j) = 4;
                end
                
                % Same Row Bottom Right
                if (abs((d1(1)+lineLength) - d2(1)) < err && abs((d1(4)+.2*lineLength)-d2(3)) < err)
                    relations(i,j) = 5;
                end
                
                % Same Row Bottom Left
                if (abs((d1(1)+lineLength) - d2(1)) < err && abs((d1(3)-.2*lineLength)-d2(4)) < err)
                    relations(i,j) = 6;
                end
                
                
                
            else % J is horizontal

                % Same Row Top Right
                if (abs(d1(1) - d2(2)) < err && abs((d1(4)+lineLength) - d2(3)) < err)
                    relations(i,j) = 1;
                end
                
                % Same Row Bottom Right
                if (abs(d1(2) - d2(1)) < err && abs((d1(4)+lineLength) - d2(3)) < err)
                    relations(i,j) = 2;
                end
                
                % Same Row Even Right
                if (abs((d1(1)-.5*lineLength) - d2(1)) < err && abs((d1(4)+lineLength) - d2(3)) < err)
                    relations(i,j) = 3;
                end
                
                % Same Row Top Left
                if (abs(d1(1) - d2(2)) < err && abs((d1(3)-lineLength) - d2(4)) < err)
                    relations(i,j) = 4;
                end
                
                % Same Row Bottom Left
                if (abs(d1(2) - d2(1)) < err && abs((d1(3)-lineLength) - d2(4)) < err)
                    relations(i,j) = 5;
                end
                
                % Same Row Even Left
                if (abs((d1(1)-.5*lineLength) - d2(1)) < err && abs((d1(3)-lineLength) - d2(4)) < err)
                    relations(i,j) = 6;
                end
                
                % Same Col Top Right
                if (abs(d1(4) - d2(3)) < err && abs((d1(1)-lineLength) - d2(2)) < err)
                    relations(i,j) = 7;
                end
                
                % Same Col Top Left
                if (abs(d1(3) - d2(4)) < err && abs((d1(1)-lineLength) - d2(2)) < err)
                    relations(i,j) = 8;
                end
                
                % Same Col Top Even
                if (abs((d1(4)-.5*lineLength) - d2(4)) < err && abs((d1(1)-lineLength) - d2(2)) < err)
                    relations(i,j) = 9;
                end
                
                % Same Col Bottom Right
                if (abs(d1(4) - d2(3)) < err && abs((d1(2)+lineLength) - d2(1)) < err)
                    relations(i,j) = 10;
                end
               
                % Same Col Bottom Left
                if (abs(d1(3) - d2(4)) < err && abs((d1(2)+lineLength) - d2(1)) < err)
                    relations(i,j) = 11;
                end
                
                % Same Col Bottom Even
                if (abs((d1(4)-.5*lineLength) - d2(4)) < err && abs((d1(2)+lineLength) - d2(1)) < err)
                    relations(i,j) = 12;
                end
                
            end      
            
        else % I is horizontal
            
            if (dominos(j, 5) == 1) % J is horizontal
                
                 %Same Row Right
                if (abs(d1(1) - d2(1)) < err && abs(d1(4)+2*lineLength - d2(3)) < err)
                    relations(i,j) = 1;
                end
                
                %Same Row Left
                if (abs(d1(1) - d2(1)) < err && abs(d1(3)-2*lineLength - d2(4)) < err)
                    relations(i,j) = 2;
                end
                
                % Same Col Top Right
                if (abs((d1(4)+lineLength) - d2(3)) < err && abs((d1(1)-.2*lineLength)-d2(2)) < err)
                    relations(i,j) = 3;
                end
                
                % Same Col Top Left
                if (abs((d1(3)-lineLength) - d2(4)) < err && abs((d1(1)-.2*lineLength)-d2(2)) < err)
                    relations(i,j) = 4;
                end
                
                % Same Col Bottom Right
                if (abs((d1(4)+lineLength) - d2(3)) < err && abs((d1(2)+.2*lineLength)-d2(1)) < err)
                    relations(i,j) = 5;
                end
                
                % Same Col Bottom Left
                if (abs((d1(3)-lineLength) - d2(4)) < err && abs((d1(2)+.2*lineLength)-d2(1)) < err)
                    relations(i,j) = 6;
                end
                
            else % J is vertical
                
                % Same Row Top Right
                if (abs(d1(1) - d2(2)) < err && abs((d1(4)+lineLength) - d2(3)) < err)
                    relations(i,j) = 1;
                end
                
                % Same Row Bottom Right
                if (abs(d1(2) - d2(1)) < err && abs((d1(4)+lineLength) - d2(3)) < err)
                    relations(i,j) = 2;
                end
                
                % Same Row Even Right
                if (abs((d1(1)-.5*lineLength) - d2(1)) < err && abs((d1(4)+lineLength) - d2(3)) < err)
                    relations(i,j) = 3;
                end
                
                % Same Row Top Left
                if (abs(d1(1) - d2(2)) < err && abs((d1(3)-lineLength) - d2(4)) < err)
                    relations(i,j) = 4;
                end
                
                % Same Row Bottom Left
                if (abs(d1(2) - d2(1)) < err && abs((d1(3)-lineLength) - d2(4)) < err)
                    relations(i,j) = 5;
                end
                
                % Same Row Even Left
                if (abs((d1(1)-.5*lineLength) - d2(1)) < err && abs((d1(3)-lineLength) - d2(4)) < err)
                    relations(i,j) = 6;
                end
                
                % Same Col Top Right
                if (abs(d1(4) - d2(3)) < err && abs((d1(1)-lineLength) - d2(2)) < err)
                    relations(i,j) = 7;
                end
                
                % Same Col Top Left
                if (abs(d1(3) - d2(4)) < err && abs((d1(1)-lineLength) - d2(2)) < err)
                    relations(i,j) = 8;
                end
                
                % Same Col Top Even
                if (abs((d1(3)-.4*lineLength) - d2(3)) < err && abs((d1(1)-lineLength) - d2(2)) < err)
                    relations(i,j) = 9;
                end
                
                % Same Col Bottom Right
                if (abs(d1(4) - d2(3)) < err && abs((d1(2)+lineLength) - d2(1)) < err)
                    relations(i,j) = 10;
                end
               
                % Same Col Bottom Left
                if (abs(d1(3) - d2(4)) < err && abs((d1(2)+lineLength) - d2(1)) < err)
                    relations(i,j) = 11;
                end
                
                % Same Col Bottom Even
                if (abs((d1(3)-.4*lineLength) - d2(3)) < err && abs((d1(2)+lineLength) - d2(1)) < err)
                    relations(i,j) = 12;
                end               
            end             
        end
    end
end

end


