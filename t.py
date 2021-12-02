from pythonping import ping


d = ping('8.8.8.8',count=1,timeout=1)

print(d.rtt_avg_ms)