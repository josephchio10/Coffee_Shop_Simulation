#Joseph Chio's Coffee Shop Simulation Personal Project

import random
import matplotlib.pyplot as plt

#Part 1 (Warmup Idea): Timeline and Customer Arrivals
#min-by-min simulation loop (0 to 179)
#simulate random customer arrivals every 2-5 mins
#track each arrival time in a list (the queue)

#create a list to show each list in a 3-hour timeframe
#timeline = list(range(180)) #run simulation for each min
# arrival_times = [] #empty list to later store the min of customer's arrival
# next_arrival = 0 #min next customer is expected to arrive

# #loop through time and simulate arrivals
# for min in timeline:
#     if min >= next_arrival:
#         arrival_times.append(min) #customer arrives
#         next_arrival = min + random.randint(2,5) #schedule next arrival

# #verify appended list
# print("Customer Arrival Times:")
# print(arrival_times)
# print("Total Customers:", len(arrival_times))

# #graph to visualize arrivals over time
# plt.scatter(arrival_times, [1]*len(arrival_times), marker='o')
# plt.title("Customer Arrivals Over 180 mins")
# plt.xlabel("min")
# plt.yticks([])
# plt.show()

#Part 2 (Actual Simulation): Simulate One Barista

#Part 2A:
#first barista introduced
#each customer has a wait time (service started minus arrival)
#each service takes 2-7 mins
#track customers served, wait times, remaining time for barista, and queue behavior

#Part 2B:
#track and graph queue lengths at every minute

timeline = list(range(180))
queue = []
queue_lengths = []
served_customers = []
wait_times = []
event_log = []
barista = {
    "busy": False,
    "remaining_time": 0,
    "current_customer": None,
}

next_arrival = 0
customer_id = 1  #name each customer for final event log

for min in timeline:
    #arrivals
    if min >= next_arrival:
        name = f"Customer {customer_id}"
        customer = {"name": name, "arrival_time": min}
        queue.append(customer)
        event_log.append(f"{min:03}: {name} arrived.")
        next_arrival = min + random.randint(2, 5)
        customer_id += 1
    #barista is busy so initiate countdown
    if barista["busy"]:
        barista["remaining_time"] -= 1
        if barista["remaining_time"] == 0:
            finished = barista["current_customer"]
            served_customers.append(finished)
            event_log.append(
                f"{min:03}: {finished['name']} finished service (waited {finished['wait_time']} min, served {finished['service_time']} min)."
            )
            barista["busy"] = False
            barista["current_customer"] = None
    #barista is free so serve next customer
    if not barista["busy"] and queue:
        next_customer = queue.pop(0)
        wait = min - next_customer["arrival_time"]
        service_time = random.randint(2, 7)
        #store customer transaction details
        barista["busy"] = True
        barista["remaining_time"] = service_time
        barista["current_customer"] = {
            "name": next_customer["name"],
            "arrival_time": next_customer["arrival_time"],
            "start_service": min,
            "wait_time": wait,
            "service_time": service_time,
        }
        wait_times.append(wait)
        event_log.append(
            f"{min:03}: {next_customer['name']} started service (waited {wait} min, will take {service_time} min)."
        )
    queue_lengths.append(len(queue))
event_log.append("180: Simulation ended.")
#after simulation ends, check who’s still in the queue

#prevent unlikely zero division error
if wait_times:
    avg_wait = round(sum(wait_times) / len(wait_times), 2)
else:
    avg_wait = 0

#queue analysis and output simulation summary
average_queue = round(sum(queue_lengths) / len(queue_lengths), 2)
max_queue = max(queue_lengths)

print("1 Barista Simulation Complete!")
print("\nSummary:")
print("Total customers served:", len(served_customers))
print("Average wait time:", avg_wait)
print("Longest wait time:", max(wait_times))
print("Customers who waited more than 5 minutes:", len([w for w in wait_times if w > 5]))
if queue:
    print(f"\n{len(queue)} customers left in queue:")
    for c in queue:
        print(f"- {c['name']} (arrived at minute {c['arrival_time']})")
    event_log.append(f"{180:03}: {len(queue)} customer(s) still in line at closing.")
else:
    print("\nNo customers left in queue!")

#graph to visualize queue lengths over time
plt.figure(figsize=(10, 4))
plt.plot(timeline, queue_lengths, label="Queue Lengths")
plt.xlabel("Minute")
plt.ylabel("Queue Length")
plt.title("Queue Lengths Over Time (1 Barista)")
plt.grid(True)
plt.show()

print("\nQueue Stats:")
print("Average queue length:", average_queue)
print("Max queue length:", max_queue)

#store first simulation results
avg_wait_1 = avg_wait
over5_1 = len([w for w in wait_times if w > 5])

#write full event log to txt file
with open("full_coffee_shop_log.txt", "w") as file:
    for entry in event_log:
        file.write(entry + "\n")

#Part 3: Simulate Two Baristas
#second barista introduced
#simulate rush hour (first sixty minutes)
#compare statistical outcomes in bar charts

timeline = list(range(180))
queue = []
queue_lengths = []
served_customers = []
wait_times = []
event_log = []
baristas = [
    {"busy": False, "remaining_time": 0, "current_customer": None},
    {"busy": False, "remaining_time": 0, "current_customer": None}
]

next_arrival = 0
customer_id = 1  #name each customer for final event log

for min in timeline:
    if min >= next_arrival:
        name = f"Customer {customer_id}"
        customer = {"name": name, "arrival_time": min}
        queue.append(customer)
        event_log.append(f"{min:03}: {name} arrived.")
        #rush hour: 0–59 mins (faster arrivals)
        if min < 60:
            next_arrival = min + random.randint(2, 3)
        else:
            next_arrival = min + random.randint(4, 6)
        customer_id += 1
    #update service timers
    for b in baristas:
        if b["busy"]:
            b["remaining_time"] -= 1
            if b["remaining_time"] == 0:
                finished = b["current_customer"]
                served_customers.append(finished)
                event_log.append(
                    f"{min:03}: {finished['name']} finished service (waited {finished['wait_time']} min, served {finished['service_time']} min)."
                )
                b["busy"] = False
                b["current_customer"] = None
    #assign free baristas to next customer
    for b in baristas:
        if not b["busy"] and queue:
            next_customer = queue.pop(0)
            wait = min - next_customer["arrival_time"]
            service_time = random.randint(2, 7)
            b["busy"] = True
            b["remaining_time"] = service_time
            b["current_customer"] = {
                "name": next_customer["name"],
                "arrival_time": next_customer["arrival_time"],
                "start_service": min,
                "wait_time": wait,
                "service_time": service_time,
            }
            wait_times.append(wait)
            event_log.append(
                f"{min:03}: {next_customer['name']} started service (waited {wait} min, will take {service_time} min)."
            )
    queue_lengths.append(len(queue))
event_log.append("180: Simulation ended.")
#after simulation ends, check who’s still in the queue

#prevent unlikely zero division error
if wait_times:
    avg_wait = round(sum(wait_times) / len(wait_times), 2)
else:
    avg_wait = 0

#queue analysis and output simulation summary
average_queue = round(sum(queue_lengths) / len(queue_lengths), 2)
max_queue = max(queue_lengths)

print("\n2 Baristas Simulation Complete!")
print("\nSummary:")
print("Total customers served:", len(served_customers))
print("Average wait time:", avg_wait)
print("Longest wait time:", max(wait_times))
print("Customers who waited more than 5 minutes:", len([w for w in wait_times if w > 5]))
if queue:
    print(f"\n{len(queue)} customers left in queue:")
    for c in queue:
        print(f"- {c['name']} (arrived at minute {c['arrival_time']})")
    event_log.append(f"{180:03}: {len(queue)} customer(s) still in line at closing.")
else:
    print("\nNo customers left in queue!")

#graph to visualize queue lengths over time
plt.figure(figsize=(10, 4))
plt.plot(timeline, queue_lengths, label="Queue Lengths")
plt.xlabel("Minute")
plt.ylabel("Queue Length")
plt.title("Queue Lengths Over Time (2 Baristas)")
plt.grid(True)
plt.show()

print("\nQueue Stats:")
print("Average queue length:", average_queue)
print("Max queue length:", max_queue)

#store second simulation results
avg_wait_2 = avg_wait
over5_2 = len([w for w in wait_times if w > 5])

#write full event log to second txt file
with open("full_coffee_shop_log_2baristas.txt", "w") as file:
    for entry in event_log:
        file.write(entry + "\n")

#bar charts comparison: 1 vs 2 baristas
labels = ['1 Barista', '2 Baristas']
avg_waits = [avg_wait_1, avg_wait_2]
over_5_counts = [over5_1, over5_2]

#plot average wait time
plt.figure(figsize=(6, 4))
bars = plt.bar(labels, avg_waits, color=['skyblue', 'lightgreen'], zorder=3)
#annotate bar with the exact value
for bar, val in zip(bars, avg_waits):
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.1, f"{val:.2f}", ha='center', va='bottom')
plt.title("Average Wait Time Comparison")
plt.ylabel("Average Wait Time (min)")
plt.ylim(0, max(avg_waits) + 2 if max(avg_waits) >= 3 else 3)  #always show at least up to 3
plt.grid(True, axis='y', zorder=0)
plt.tight_layout()
plt.show()

#plot customers who waited more than five minutes
plt.figure(figsize=(6, 4))
bars = plt.bar(labels, over_5_counts, color=['red', 'orange'], zorder=3)
for bar, val in zip(bars, over_5_counts):
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.3, str(val), ha='center', va='bottom')
plt.title("Customers Waiting Over 5 Minutes")
plt.ylabel("Customer Count")
plt.ylim(0, max(over_5_counts) + 4) #+4 for extra label padding
plt.grid(True, axis='y', zorder=0)
plt.tight_layout()
plt.show()