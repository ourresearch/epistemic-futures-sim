import subprocess, sys
p = subprocess.Popen(["/bin/zsh", "/Users/jasonpriem/ox/epistemic-futures-sim/sim1-simple/launch.sh"],
                     start_new_session=True, stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(p.pid)
