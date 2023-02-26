from functions import *

configs = load_config()

#print(configs)
running = True
'''
for list in configs['lists'].values():
        mb_watch(list,configs)
    #print('[*] Delaying ' + configs['delay'] + ' seconds')
    #time.sleep(int(configs['delay']))
'''
while True:
    for list in configs['lists'].values():
        stime = Decimal(time.perf_counter())
        mb_watch(list,configs)
        etime = Decimal(time.perf_counter())
        ttime = etime - stime
        if ttime <= 10:
            time.sleep(int(configs['delay']))

