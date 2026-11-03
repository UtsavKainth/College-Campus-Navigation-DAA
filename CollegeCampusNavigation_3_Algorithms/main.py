import tkinter as tk
from tkinter import ttk, messagebox

# Sample campus locations and walking distances (metres)
places = ['Main Gate', 'Library', 'Academic Block', 'Canteen', 'Hostel', 'Sports Ground']
roads = [
    ('Main Gate', 'Library', 200),
    ('Main Gate', 'Academic Block', 350),
    ('Library', 'Academic Block', 150),
    ('Library', 'Canteen', 300),
    ('Academic Block', 'Canteen', 180),
    ('Academic Block', 'Sports Ground', 400),
    ('Canteen', 'Hostel', 250),
    ('Hostel', 'Sports Ground', 220),
    ('Canteen', 'Sports Ground', 350)
]

# Build a graph (adjacency list)
graph = {place: [] for place in places}
for a, b, distance in roads:
    graph[a].append((b, distance))
    graph[b].append((a, distance))


def dijkstra(start, end):
    distances = {place: float('inf') for place in places}
    previous = {place: None for place in places}
    visited = set()
    distances[start] = 0

    while len(visited) < len(places):
        current = None
        for place in places:
            if place not in visited:
                if current is None or distances[place] < distances[current]:
                    current = place
        if current is None or distances[current] == float('inf'):
            break
        visited.add(current)
        for neighbour, length in graph[current]:
            new_distance = distances[current] + length
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    if distances[end] == float('inf'):
        return [], None
    return path, distances[end]


def kruskal():
    parent = {place: place for place in places}

    def find(place):
        while parent[place] != place:
            place = parent[place]
        return place

    selected = []
    for a, b, distance in sorted(roads, key=lambda road: road[2]):
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b:
            parent[root_a] = root_b
            selected.append((a, b, distance))
    return selected


def bubble_sort(items):
    items = items.copy()
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j][1] > items[j + 1][1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items

# Positions on the map canvas
positions = {
    'Main Gate': (90, 280),
    'Library': (240, 130),
    'Academic Block': (370, 270),
    'Canteen': (530, 130),
    'Hostel': (700, 210),
    'Sports Ground': (660, 380)
}

root = tk.Tk()
root.title('College Campus Navigation System | DAA Mini Project')
root.geometry('1050x760')
root.minsize(920, 700)
root.configure(bg='#edf2f7')

style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', padding=6, font=('Arial', 11))

header = tk.Frame(root, bg='#142c47', height=90)
header.pack(fill='x')
header.pack_propagate(False)
tk.Label(header, text='COLLEGE CAMPUS NAVIGATION SYSTEM', bg='#142c47', fg='white', font=('Arial', 20, 'bold')).pack(pady=(14, 2))
tk.Label(header, text='DAA Mini Project  |  Dijkstra  •  Kruskal  •  Bubble Sort', bg='#142c47', fg='#b8d8f1', font=('Arial', 10)).pack()

controls = tk.Frame(root, bg='white', padx=16, pady=14)
controls.pack(fill='x', padx=20, pady=(16, 10))

tk.Label(controls, text='Starting location', bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w')
tk.Label(controls, text='Destination', bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=14)
start_box = ttk.Combobox(controls, values=places, state='readonly', width=24)
end_box = ttk.Combobox(controls, values=places, state='readonly', width=24)
start_box.set('Main Gate')
end_box.set('Hostel')
start_box.grid(row=1, column=0, pady=(5, 12), sticky='w')
end_box.grid(row=1, column=1, padx=14, pady=(5, 12), sticky='w')

canvas = tk.Canvas(root, bg='#f8fbff', highlightthickness=1, highlightbackground='#d5dfe9', height=420)
canvas.pack(fill='both', expand=True, padx=20)

output = tk.Text(root, height=6, bg='#142c47', fg='white', font=('Consolas', 11), padx=15, pady=12, wrap='word')
output.pack(fill='x', padx=20, pady=(10, 16))
output.config(state='disabled')


def show_text(message):
    output.config(state='normal')
    output.delete('1.0', tk.END)
    output.insert(tk.END, message)
    output.config(state='disabled')


def draw_map(highlighted=None):
    canvas.delete('all')
    highlighted = highlighted or []
    highlighted_edges = {frozenset((a, b)) for a, b in highlighted}
    for a, b, distance in roads:
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        active = frozenset((a, b)) in highlighted_edges
        canvas.create_line(x1, y1, x2, y2, fill='#f59e0b' if active else '#a7bacb', width=5 if active else 2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        canvas.create_text(mx, my - 11, text=str(distance) + 'm', fill='#566b7d', font=('Arial', 9, 'bold'))
    for name, (x, y) in positions.items():
        canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill='#1675b9', outline='white', width=3)
        canvas.create_text(x, y + 26, text=name, fill='#17324b', font=('Arial', 10, 'bold'))
    canvas.create_text(18, 20, anchor='w', text='CAMPUS MAP  •  Orange lines show the selected route/network', fill='#546b7e', font=('Arial', 10, 'bold'))


def shortest_route():
    start, end = start_box.get(), end_box.get()
    path, distance = dijkstra(start, end)
    if distance is None:
        show_text('No path found.')
        return
    draw_map(list(zip(path, path[1:])))
    show_text('DIJKSTRA - SHORTEST PATH\nRoute: ' + ' → '.join(path) + '\nTotal walking distance: ' + str(distance) + ' metres')


def show_mst():
    selected = kruskal()
    draw_map([(a, b) for a, b, _ in selected])
    total = sum(distance for _, _, distance in selected)
    lines = [a + ' - ' + b + ': ' + str(distance) + ' m' for a, b, distance in selected]
    show_text('KRUSKAL - MINIMUM SPANNING TREE\nTotal network distance: ' + str(total) + ' metres\n' + ' | '.join(lines))


def show_sorted():
    start = start_box.get()
    reachable = []
    for place in places:
        if place != start:
            _, distance = dijkstra(start, place)
            if distance is not None:
                reachable.append((place, distance))
    result = bubble_sort(reachable)
    draw_map()
    show_text('BUBBLE SORT - LOCATIONS BY SHORTEST WALKING DISTANCE FROM ' + start.upper() + '\n' + '\n'.join(str(i + 1) + '. ' + place + ': ' + str(distance) + ' metres' for i, (place, distance) in enumerate(result)))


def add_button(text, command, column, color):
    tk.Button(controls, text=text, command=command, bg=color, fg='white', activebackground=color, activeforeground='white', relief='flat', padx=13, pady=10, font=('Arial', 10, 'bold'), cursor='hand2').grid(row=2, column=column, padx=(0, 10), sticky='w')

add_button('Find Shortest Path', shortest_route, 0, '#1675b9')
add_button('Kruskal MST', show_mst, 1, '#147d65')
add_button('Sort Locations', show_sorted, 2, '#7655ad')

# Let the destination selection sit above its own button column.
draw_map()
show_text('Welcome! Select a starting location and destination, then choose an algorithm.\nAll campus distances are sample data for educational demonstration.')
root.mainloop()
