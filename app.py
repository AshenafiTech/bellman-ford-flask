from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

# Function to find the least expensive route


def find_least_expensive_route(N, paths, start, end, max_stops):
    graph = {i: [] for i in range(N)}
    for u, v, w in paths:
        graph[u].append((v, w))

    pq = [(0, start, 0, [start])]
    distances = {(start, 0): 0}

    while pq:
        cost, current, stops, path = heapq.heappop(pq)

        if current == end:
            return cost, path

        if stops > max_stops:
            continue

        for neighbor, weight in graph[current]:
            new_cost = cost + weight
            if (neighbor, stops + 1) not in distances or new_cost < distances[(neighbor, stops + 1)]:
                distances[(neighbor, stops + 1)] = new_cost
                heapq.heappush(
                    pq, (new_cost, neighbor, stops + 1, path + [neighbor]))

    return -1, []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input from the form
        N = int(request.form['stations'])
        start = int(request.form['start_station'])
        end = int(request.form['end_station'])
        max_stops = int(request.form['max_stops'])

        # Process the paths
        raw_paths = request.form['paths'].strip()
        paths = eval(raw_paths)  # Safely evaluate the input paths

        # Calculate the least expensive route
        cost, path = find_least_expensive_route(
            N, paths, start, end, max_stops)

        if cost == -1:
            result = "No such route exists (-1)"
        else:
            result = f"Minimum energy required: {cost}, Path: {' -> '.join(map(str, path))}"

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(debug=True)
