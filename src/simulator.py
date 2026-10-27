import sys
from air_traffic_control import Flight, AirTrafficControl

def run_simulation(lines):
    atc = AirTrafficControl()
    f = None

    for line in lines:
        parts = line.split()
        if len(parts) == 0:
            continue
            
        cmd = parts[0]
        
        if cmd == "FLIGHT":
            max_speed = int(parts[1])
            pos = (int(parts[2]), int(parts[3]), int(parts[4]))
            v = (int(parts[5]), int(parts[6]), int(parts[7]))
            f = Flight(max_speed, pos, v)
            
        elif cmd == "ACCEL":
            t = float(parts[1])
            acc = (int(parts[2]), int(parts[3]), int(parts[4]))
            if f != None:
                f.set_acceleration(t, acc)
                
        elif cmd == "FSTATUS":
            t = float(parts[1])
            if f != None:
                print(f.status(t))
                
        elif cmd == "CREATE":
            t = float(parts[1])
            flight_id = parts[2]
            max_speed = int(parts[3])
            pos = (int(parts[4]), int(parts[5]), int(parts[6]))
            v = (int(parts[7]), int(parts[8]), int(parts[9]))
            atc.create(t, flight_id, max_speed, pos, v)
            
        elif cmd == "UPDATE":
            t = float(parts[1])
            flight_id = parts[2]
            acc = (int(parts[3]), int(parts[4]), int(parts[5]))
            atc.update(t, flight_id, acc)
            
        elif cmd == "STATUS":
            t = float(parts[1])
            flight_id = parts[2]
            print(atc.status(t, flight_id))

if __name__ == "__main__":
    # Supports: python3 src/simulator.py --test tests/visible_cases_1.txt
    if len(sys.argv) >= 3 and sys.argv[1] == "--test":
        with open(sys.argv[2], "r") as file:
            run_simulation(file)
    # Supports: python3 src/simulator.py tests/visible_cases_1.txt
    elif len(sys.argv) == 2:
        with open(sys.argv[1], "r") as file:
            run_simulation(file)
    # Supports: python3 src/simulator.py < tests/visible_cases_1.txt
    else:
        run_simulation(sys.stdin)