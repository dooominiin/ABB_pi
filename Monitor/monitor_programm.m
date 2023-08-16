clear 
close all
k=0;

maxlaenge = 600;

dicke = 2;
fig1 = figure(1);
fig2 = figure(2);
fig3 = figure(3);

while true
    
    file= "../data.h5";
    kk = dir(file).datenum;
    ist_neu = k ~= kk;
    k=kk;
    if ist_neu
        %disp("ist neu")
        tic
        table_aktualisiert = true;
        try
            info = h5info(file,'/');
            size = info.Groups.Datasets(1).Dataspace.Size;
            count = min([size, maxlaenge]);
            start = size-count+1;
            temp = table();
            for i = 1:length(info.Groups.Datasets)
                name = info.Groups.Datasets(i).Name;
                path = '/States/' + string(name);
                temp = addvars(temp, h5read(file,path,start,count), 'NewVariableNames', name);
            end
        catch exception
            fprintf('Ein Fehler ist aufgetreten: %s\n', exception.message);
            table_aktualisiert = false;
        end
        if table_aktualisiert
            p = temp;
        end
        

       
% innerer Regelkreis ___________________________________________________
        set(groot,'CurrentFigure',fig1)
        clf
        subplot(3,1,[1 2])

        plot(p.time,p.s_V,'k','LineStyle',':','LineWidth',dicke)
        hold on
        plot(p.time,p.("T_D4[0]"),'k','LineStyle','-','LineWidth',dicke)
        
        plot(p.time,p.s_V_K,'b','LineStyle',':','LineWidth',dicke)
        plot(p.time,p.T_V_tilde,'b','LineStyle','-','LineWidth',dicke)
        
        legend({'s_V','TD40','s_V_K','T_V_tilde'},'Location','northwest')
        title('innerer Regelkreis ['+ string(p.time(end))+']')
        grid on
        
        
        subplot(3,1,3)

        plot(p.time,p.r,'k','LineStyle','-','LineWidth',dicke)
        hold on
        plot(p.time,p.r_tilde,'k','LineStyle','--','LineWidth',dicke)
        plot(p.time,p.m,'k','LineStyle','-.','LineWidth',dicke)
        
        legend({'r','r_tilde','m'},'Location','northwest')
        grid on


% äusserer Regelkreis ___________________________________________________
        set(groot,'CurrentFigure',fig2)
        clf
        subplot(3,1,[1 2])

        plot(p.time,p.s_k,'k','LineStyle',':','LineWidth',dicke)
        hold on
        plot(p.time,p.TOELE,'k','LineStyle','-','LineWidth',dicke)
        
        plot(p.time,p.s,'b','LineStyle',':','LineWidth',dicke)
        
        legend({'s_k','TOELE','s'},'Location','northwest')
        
        title('äusserer Regelkreis ['+ string(p.time(end))+']')
        grid on
        
        
        subplot(3,1,3)
        plot(p.time,p.f,'k','LineStyle','-','LineWidth',dicke)
        hold on
        plot(p.time,p.k,'k','LineStyle','--','LineWidth',dicke)
        
        legend({'f','k'},'Location','northwest')
        grid on


% Totzeiten  ____________________________________________________________
        set(groot,'CurrentFigure',fig3)
        clf
        subplot(4,1,[1 2])

        plot(p.time,p.T_T_2,'k','LineStyle','-','LineWidth',dicke)
        hold on
        plot(p.time,p.TOELE,'b','LineStyle','-','LineWidth',dicke)
        
        plot(p.time,p.T_T_2-p.TOELE,'k','LineStyle',':','LineWidth',dicke*0.6)
        
        legend({'T_T_2','TOELE','differenz'},'Location','northwest')
        
        title('Totzeiten ['+ string(p.time(end))+']s')
        grid on
        
        
        subplot(4,1,[3 4])

        plot(p.time,p.T_V_tilde,'k','LineStyle','-','LineWidth',dicke)
        hold on
        plot(p.time,p.("T_D4[0]"),'b','LineStyle','-','LineWidth',dicke)
        
        plot(p.time,p.T_V_tilde-p.("T_D4[0]"),'k','LineStyle',':','LineWidth',dicke*0.6)
        
        legend({'T_V_tilde','T_D40','differenz'},'Location','northwest')
        grid on
    
        
        
        


       
        drawnow
    
            
        toc
        pause(0.01)
        
    end
end

