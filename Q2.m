t_0 = 0;
t_1 = 1000;

V_0 = 5:1:8;
m_0 = 0.1:0.02:0.2;
h_0 = 0.36:0.02:0.4;
n_0 = 0:0.2:1;
I_0 = 9.77;

global I

for i = 1:length(V_0)
    for j = 1:length(m_0)
        for k = 1:length(h_0) 
            for l = 1:length(n_0) 
                for a = 1:length(I_0)
                    I = I_0(a);
                    [t,X] = ode45(@HH, [t_0 t_1], [V_0(i), m_0(j), h_0(k), n_0(l)]);
                    plot3(X(:,1),X(:,2),X(:,3))
                    xlabel('V')
                    ylabel('m')
                    zlabel('h')
                    hold on
                end
            end
        end
    end
end
hold off

function dXdt = HH(t,X)
global I
V_Na = 115.0;
V_k = -12.0;
V_l = 10.599;
g_Na = 120;
g_K = 36.0; 
g_l= 0.3; 
C_M = 1.0;
Phi = 1;

alpha_m = 0.1 .* ( 25.0 - X(1)) ./ (exp((25.0 - X(1)) ./ 10.0)-10);
beta_m = 4.0 .* exp(-X(1) ./ 18.0);
alpha_h = 0.07 .* exp (-X(1) ./ 20.0);
beta_h = 1.0 ./ (exp((-X(1) + 30.0) ./ 10.0) + 1.0);
alpha_n = 0.01 .* (10.0-X(1)) ./ (exp((10.0-X(1)) ./ 10.0) -1.0);
beta_n = 0.125 .* exp(-X(1) ./ 80.0);

dXdt = [(I - g_Na .* X(2).^3 .* X(3) .* (X(1) - V_Na) - g_K .* X(4).^4 .* (X(1) - V_k) - g_l .* (X(1) - V_l))./C_M;
        (alpha_m .* ( 1 - X(2) ) - beta_m .* X(2)) .* Phi;
        (alpha_h .* ( 1 - X(3) ) - beta_h .* X(3)) .* Phi;
        (alpha_n .* ( 1 - X(4) ) - beta_n .* X(4)) .* Phi];
end