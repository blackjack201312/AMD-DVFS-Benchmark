import os
import subprocess
import time
import re
import ConfigParser
import json

APP_ROOT = 'applications'
LOG_ROOT = 'logs'

# Reading benchmark settings
cf_bs = ConfigParser.SafeConfigParser()
cf_bs.read("configs/benchmark_settings.cfg")

# running iteration/timing settings
running_iters = cf_bs.getint("profile_control", "iters")
running_time = cf_bs.getint("profile_control", "secs")

# device id settings
nvIns_dev_id = cf_bs.getint("profile_control", "nvIns_device_id")
cuda_dev_id = cf_bs.getint("profile_control", "cuda_device_id")

# power sampling settings
pw_sample_int = cf_bs.getint("profile_control", "power_sample_interval")
rest_int = cf_bs.getint("profile_control", "rest_time")

# kernel profiling
metrics = json.loads(cf_bs.get("profile_control", "metrics"))

# dvfs settings and control
core_frequencies = json.loads(cf_bs.get("dvfs_control", "coreF"))
memory_frequencies = json.loads(cf_bs.get("dvfs_control", "memF"))
mode = cf_bs.get("dvfs_control", "mode")

# Read GPU application settings
cf_ks = ConfigParser.SafeConfigParser()
cf_ks.read("configs/kernels_settings.cfg")
benchmark_programs = cf_ks.sections()

print benchmark_programs
print metrics
print core_frequencies
print memory_frequencies

# time.sleep(100)
# open GPU monitor
# os.system('start nvidiaInspector.exe -showMonitoring')

# # reset GPU first
# command = 'nvidiaInspector.exe -forcepstate:%s,16' % nvIns_dev_id
# print command
# os.system(command)
# time.sleep(rest_int)

for core_f in core_frequencies:
    for mem_f in memory_frequencies:

        if mode == 'auto':
            pass
            # print command
            # os.system(command)
        else:
            print "Core F: %s, Mem F: %s, Hit Enter to begin benchmark." % (core_f, mem_f)
            # os.system("read")
            os.system("pause")

        time.sleep(rest_int)

        for app in benchmark_programs:

            args = json.loads(cf_ks.get(app, 'args'))

            argNo = 0

            for arg in args:

                # arg, number = re.subn('-device=[0-9]*', '-device=%d' % cuda_dev_id, arg)
                powerlog = 'benchmark_%s_core%d_mem%d_input%02d_power' % (app, core_f, mem_f, argNo)
                perflog = 'benchmark_%s_core%d_mem%d_input%02d_perf' % (app, core_f, mem_f, argNo)
                metricslog = 'benchmark_%s_core%d_mem%d_input%02d_metrics' % (app, core_f, mem_f, argNo)

                # start record power data
                # os.system("echo \"arg:%s\" >> %s/%s" % (arg, LOG_ROOT, powerlog))
                esti_pwS_time = int(running_time) + 2 * int(rest_int) + 20
                command = 'start /B CodeXLPowerProfiler.exe -e all -T %d -d %d -o %s/%s -F txt' % (pw_sample_int, esti_pwS_time, LOG_ROOT, powerlog)
                print command
                os.system(command)
                time.sleep(rest_int)

                # execute program to collect power data
                os.system("echo \"arg:%s\" >> %s/%s.txt" % (arg, LOG_ROOT, perflog))
                command = '%s\\%s %s -q -d %d -s %d >> %s/%s.txt' % (APP_ROOT, app, arg, cuda_dev_id, running_time, LOG_ROOT, perflog)
                # command = '%s\\%s %s >> %s/%s' % (APP_ROOT, app, arg, LOG_ROOT, perflog)
                print command
                os.system(command)
                time.sleep(rest_int)

                # stop record power data
                # os.system('tasklist|findstr "CodeXLPowerProfiler.exe" && taskkill /F /IM CodeXLPowerProfiler.exe')
                print "Waiting power sampling exit..."
                while True:
                    live_pro = os.popen('tasklist|findstr "CodeXLPowerProfiler.exe"')
                    if len(live_pro.readlines()) == 0:
                        break

                # execute program to collect time data, metrics data, grid and block settings
                command = 'rcprof-x64.exe -o "./%s/%s" -p -w "./%s" "./%s/%s.exe" %s -d %d -i 50 -q -s %d ' % (LOG_ROOT, metricslog, APP_ROOT, APP_ROOT, app, arg, cuda_dev_id, running_time)
                print command
                os.system(command)
                time.sleep(rest_int)


# # reset GPU first
# command = 'nvidiaInspector.exe -forcepstate:%s,16' % nvIns_dev_id
# print command
# os.system(command)
# time.sleep(rest_int)
# os.system('pause')