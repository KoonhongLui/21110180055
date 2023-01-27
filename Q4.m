t_0 = 0;
t_1 = 10000;

VE_0 = [0.1:0.02:0.18];
VI_0 = [0.30:0.02:0.38];

for i = 1:length(VE_0)
    for j = 1:length(VI_0)
        [t,X] = ode45(@EI, [t_0 t_1], [VE_0(i), VI_0(j)]);
        plot(X(:,1),X(:,2))
        xlabel('V_E')
        ylabel('V_I')
        hold on
    end
end
hold off

function dXdt = EI(t,X)
M_EE = 2;
M_IE = 3;
M_EI = 3;
M_II = 3;
h_I = 1;
h_E = 1;
tau_E = 1;
tau_I = 4.1;

dXdt = [(-X(1) + max(0, M_EE .* X(1) - M_IE .* X(2) + h_E))./tau_E;
        (-X(2) + max(0, M_IE .* X(1) - M_II .* X(2) + h_I))./tau_I];
end