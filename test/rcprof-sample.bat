::An example to collect OpenCL performance counters: 
rcprof-x64.exe -o ".\\logs\\pc.csv" -p -w ".\\applications" ".\\applications\\MatrixMultiplication.exe" --device gpu

::An example to collect an OpenCL API trace:
rcprof-x64.exe -a ".\\logs\\api.atp" -t -T -w ".\\applications" ".\\applications\\MatrixMultiplication.exe" --device gpu

::An example to collect HSA performance counters (Linux only): 
::rcprof-x64.exe -o "/path/to/output.csv" -C -w "/path/to/app/working/directory" "/path/to/app.exe"

::An example to collect an HSA API trace(Linux only) :
::rcprof-x64.exe -o "/path/to/output.atp" -A -w "/path/to/app/working/directory" "/path/to/app.exe"

::An example to collect an OpenCL API trace with summary pages:
::rcprof-x64.exe -o "/path/to/output.atp" -t -T -w "/path/to/app/working/directory" "/path/to/app.exe" --device gpu

::An example to generate summary pages from an .atp file:
::rcprof-x64.exe -a "/path/to/output.atp" -T

::An example to generate an occupancy display page:
::rcprof-x64.exe -P "/path/to/session.occupancy" --occupancyindex 2 -o "path/to/output.html"