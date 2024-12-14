import json
import gzip
import msgpack
import time
start = time.time()

with open("../Simulation data files/rocket_trajectory(3D).json", "r") as file:
    data = json.load(file)
print("Read from simulation file")

end = time.time()
elapsed_time = end - start
print(elapsed_time)

# Save minified JSON
with open("minified_file.json", "w") as file:
    json.dump(data, file, separators=(",", ":"))
print("Dumping in minified file")

# Save compressed JSON
with open("minified_file.json", "r") as file:
    data = file.read()
print("Read from minified file")

with open("compressed_file.msgpack", "wb") as file:
    file.write(msgpack.packb(data))
print("Written to minified file msg packed file")

with gzip.open("compressed_file.json.gz", "wt", encoding="utf-8") as gz_file:
    gz_file.write(data)
