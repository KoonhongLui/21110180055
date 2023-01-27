n = 7;
city_x = [1,3,5,5,6,7,9];
city_y = [2,6,3,1,7,2,4];
D = squareform(pdist([city_x;city_y]'));

T = 100000;
lambda = 100;
mu = 1;
X = zeros(T,n,n);
U = zeros(T,n,n);
for i=1:n
    U(1,i,i) = 1;
end

for i=1:T
    for x=1:n
        for s=1:n
            sum_t = 0;
            for t=1:n
                sum_t = sum_t + X(i,x,t);
            end
            sum_y = 0;
            for y=1:n
                sum_y = sum_y + X(i,y,s);
            end
            len = 0;
            for y=1:n
                len = len + D(x,y)*X(i,y,(mod(s,n)+1));
            end
            du = -lambda*(sum_t + sum_y -2) - len;
            U(i+1,x,s) = U(i,x,s) + du;
            X(i+1,x,s) = 1/(1+exp(-mu*U(i+1,x,s)));
        end
    end
end
X_res = reshape(X(T+1,:,:),[n,n]);
[M,rout] = max(X_res);
dis = 0;
for i=1:n
    dis = dis + D(rout(i),rout(mod(i,n)+1));
end
rout
dis

rout_x = city_x(abs(rout));
rout_x = [rout_x, rout_x(1)];
rout_y = city_y(abs(rout));
rout_y = [rout_y, rout_y(1)];
figure
plot(rout_x,rout_y,'-o')
