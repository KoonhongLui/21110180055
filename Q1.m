n = 5;

me = linspace(1,2,n);
va = linspace(0.005,0.01,n);

mu= [];
sigma = [];

for i = 1:n 
    mu(i) = exp(me(i) + var(i)/2) / (exp(me(i) + var(i)/2)-1);
    sigma(i) = sqrt(2*va(i)/( (mu(i) - 1)^(-2) - mu(i)^(-2)));
end

% V_r=0  V_th=1 g=1 t_ref = 0;
% OU process: dV = (mu -V)dt + sigma*W;
dt = 1e-2;
for i = 1:n
    T = [];
    dt = 1e-4;
    t = 0:dt:1000;
    V = zeros(1,length(t));                 
    for j = 1:length(t)-1
        V(j+1) = V(j) + (mu(i)-V(j))*dt + sigma(i)*sqrt(dt)*randn;
        if V(j+1) >= 1
            V(j+1) = 0;
            T(end + 1) = t(j+1);
        end
    end
    for j = length(T):-1:2
        T(j) = T(j) - T(j-1);
    end
    me_est(i) = mean(T);
    va_est(i) = var(T);
end
me
me_est
va
va_est


