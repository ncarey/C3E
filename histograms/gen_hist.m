x = dlmread('./filtered_hists/case3/case3.ugly',',')

hours = x(:,3:26)
durations = x(:,27:49)

hoursx = 0:23

#durations_label = ['x <= 0us','0us < x <= 10us','10us < x <= 100us','100us < x <= 1000us','1000us < x <= .01s','.01s < x <= .1s','.1s < x <= 1s','1s < x <= 5s','5s < x <= 10s','10s < x <= 30s','30s < x <= 1m','1m < x <= 2m','2m < x <= 5m','5m < x <= 10m','10m < x <= 30m','30m < x <= 1h','1h < x <= 3h','3h < x <= 6h','6h < x <= 12h','12h < x <= 1d','1d < x <= 2d','2d < x <= 1w','1w < x <= 1 month','1 month < x']

#hours_label = ['1','2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','9-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-24']


#HAX HAX HAX
derp = [durations;durations]

bar(derp)

legend('x <= 0us','0us < x <= 10us','10us < x <= 100us','100us < x <= 1000us','1000us < x <= .01s','.01s < x <= .1s','.1s < x <= 1s','1s < x <= 5s','5s < x <= 10s','10s < x <= 30s','30s < x <= 1m','1m < x <= 2m','2m < x <= 5m','5m < x <= 10m','10m < x <= 30m','30m < x <= 1h','1h < x <= 3h','3h < x <= 6h','6h < x <= 12h','12h < x <= 1d','1d < x <= 2d','2d < x <= 1w','1w < x <= 1 month','1 month < x')

xlim([.6,1.5])

fake_label = ['','','','','','','','','','','','','','','','','','','','','']
set(gca, 'Xticklabel', fake_label)
xlabel('Duration Between Requests')
ylabel('Number of Requests')
title('Histogram of Average Client inter-DNS Request Duration')
print -dpng avg_req_dur.png




figure('Position',[25,25,1800,1000])
bar (hoursx, hours)
set(gca, 'Xtick', hoursx)
set(gca, 'Xticklabel', hoursx)
xlim([-.5,23.5])
xlabel('Hour of Day')
ylabel('Number of Requests')
title('Histogram of Average Client DNS Requests per Hour')

print -dpng avg_req_hour.png



