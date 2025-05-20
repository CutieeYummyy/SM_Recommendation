import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
import pandas as pd
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import SVD, Reader, Dataset
from surprise.model_selection import train_test_split

# ======= Tạo bản đồ siêu thị kiểu mới =======
class SupermarketGenerator:
    def __init__(self, rows=15, cols=20, seed=42):
        self.rows = rows
        self.cols = cols
        self.seed = seed
        self.layout = [["-" for _ in range(cols)] for _ in range(rows)]
        self.product_zones = {}
        self.products = {}
        self.entrance = [rows - 1, 2]
        self.exit = [rows - 1, cols - 3]
        random.seed(seed)

    def is_accessible(self):
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        queue = deque()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.layout[r][c] == "E":
                    queue.append((r, c))
                    visited[r][c] = True
                    break
        walkable = {"-", "E", "X"}
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if not visited[nr][nc] and self.layout[nr][nc] in walkable:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
        for r in range(self.rows):
            for c in range(self.cols):
                if self.layout[r][c] == "X" and visited[r][c]:
                    return True
        return False

    def generate_layout(self):
        self.layout = [["-" for _ in range(self.cols)] for _ in range(self.rows)]
        zone_positions = [
            (0, 0, 4, 4, "A1"),
            (0, self.cols-5, 4, 4, "A2"),
            (self.rows-5, 0, 4, 4, "A3"),
            (self.rows-5, self.cols-5, 4, 4, "A4"),
            (self.rows//2-2, self.cols//2-2, 4, 4, "A5")
        ]
        for r, c, h, w, zone in zone_positions:
            for i in range(h):
                for j in range(w):
                    if 0 <= r+i < self.rows and 0 <= c+j < self.cols:
                        self.layout[r+i][c+j] = zone
                        self.product_zones[zone] = {"position": (r+i, c+j)}

        sub_zones = ["B1", "B2", "B3", "B4", "B5", "P"]
        for zone in sub_zones:
            while True:
                r = random.randint(1, self.rows-2)
                c = random.randint(1, self.cols-2)
                if self.layout[r][c] == "-":
                    self.layout[r][c] = zone
                    self.product_zones[zone] = {"position": (r, c)}
                    break

        self.layout[self.entrance[0]][self.entrance[1]] = "E"
        self.layout[self.exit[0]][self.exit[1]] = "X"
        if not self.is_accessible():
            self.generate_layout()

    def assign_products(self, product_names):
        pid = 1
        used = set()

        for name in product_names:
            while True:
                r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
                if self.layout[r][c] == "-" and (r, c) not in used:
                    used.add((r, c))

                    # Tìm zone gần nhất
                    nearest_zone = "Unknown"
                    min_dist = float('inf')
                    for zone, info in self.product_zones.items():
                        zr, zc = info["position"]
                        d = abs(zr - r) + abs(zc - c)
                        if d < min_dist:
                            min_dist = d
                            nearest_zone = zone

                    self.products[name] = {
                        "name": name,
                        "position": [r, c],
                        "zone": nearest_zone
                    }
                    break

    def create_store_data(self):
        layout_grid = []
        for row in self.layout:
            layout_row = []
            for cell in row:
                if cell in ["E", "X", "-"]:
                    layout_row.append(cell)
                else:
                    layout_row.append("#")
            layout_grid.append(layout_row)
        return {
            "layout": {
                "grid": layout_grid,
                "entrance": self.entrance,
                "exit": self.exit
            },
            "products": self.products
        }

    def plot_layout(self, title="Bản đồ siêu thị", path=None, show=True, save=False):
        zone_colors = {
            "B1": "#FFF8DC", "B2": "#FFE4B5", "B3": "#FFB6C1", "B4": "#98FB98",
            "B5": "#87CEEB", "B6": "#E0FFFF", "A1": "#D8BFD8", "A2": "#DDA0DD",
            "A3": "#DA70D6", "A4": "#FF00FF", "A5": "#BA55D3", "E": "#228B22", "X": "#DC143C", "-": "white"
        }
        fig, ax = plt.subplots(figsize=(12, 8))
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.layout[r][c]
                color = zone_colors.get(val, "white")
                rect = patches.Rectangle((c, self.rows - 1 - r), 1, 1, edgecolor="black", facecolor=color)
                ax.add_patch(rect)
                if val in zone_colors and val not in ["E", "X", "-"]:
                    ax.text(c + 0.5, self.rows - 1 - r + 0.5, val[:3], ha='center', va='center', fontsize=8)
        for prod in self.products.values():
            r, c = prod["position"]
            ax.text(c + 0.5, self.rows - 1 - r + 0.5, prod["name"][0], color='blue', ha='center', va='center', fontsize=10)
        er, ec = self.entrance
        xr, xc = self.exit
        ax.text(ec + 0.5, self.rows - 1 - er + 0.5, 'E', color='white', ha='center', va='center', fontsize=12, weight='bold')
        ax.text(xc + 0.5, self.rows - 1 - xr + 0.5, 'X', color='white', ha='center', va='center', fontsize=12, weight='bold')
        if path:
            y = [self.rows - 1 - p[0] + 0.5 for p in path]
            x = [p[1] + 0.5 for p in path]
            ax.plot(x, y, 'b-', linewidth=2)
            ax.plot(x, y, 'bo')
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.set_xticks(range(self.cols + 1))
        ax.set_yticks(range(self.rows + 1))
        ax.set_title(title)
        plt.tight_layout()
        if save:
            plt.savefig("cbf_map_result.png")
        if show:
            plt.show()

# ======= Gợi ý sản phẩm =======
df = pd.read_excel("OnlineRetail.xlsx")
df = df[df['Quantity'] > 0].dropna(subset=['Description', 'CustomerID'])
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Description'])
tfidf_tensor = tf.convert_to_tensor(tfidf_matrix.toarray(), dtype=tf.float32)

def recommend_by_name(product_name, top_n=5):
    idx = df[df['Description'].str.contains(product_name, case=False)].index[0]
    product_vector = tf.expand_dims(tfidf_tensor[idx], 0)
    cosine_sim = tf.matmul(product_vector, tfidf_tensor, transpose_b=True).numpy().flatten()
    
    scores = list(enumerate(cosine_sim))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    seen = set()
    recommendations = []
    for i, score in scores:
        desc = df.iloc[i]['Description']
        if desc not in seen and desc.lower() != product_name.lower():
            seen.add(desc)
            recommendations.append((desc, score * 100))
        if len(recommendations) >= top_n:
            break
    return recommendations

def recommend_by_user(user_id, top_n=5):
    df_user = df[df['CustomerID'] == user_id]
    reader = Reader(rating_scale=(1, 100))
    data = Dataset.load_from_df(df_user[['CustomerID', 'Description', 'Quantity']], reader)
    trainset, _ = train_test_split(data, test_size=0.2)
    model = SVD()
    model.fit(trainset)
    all_items = df['Description'].unique()
    purchased = df_user['Description'].unique()
    recommended = [item for item in all_items if item not in purchased]
    return recommended[:top_n]

# ======= BFS tìm đường =======
def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = set([start])
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == goal:
            return path
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != "#" and (nr, nc) not in visited:
                    queue.append(((nr, nc), path + [(nr, nc)]))
                    visited.add((nr, nc))
    return []

# ======= TSP dùng GA =======
def genetic_algorithm(dist_matrix, num_points, generations=100, pop_size=80, mutation_rate=0.2):
    gene_pool = list(range(1, num_points - 1))
    population = [random.sample(gene_pool, len(gene_pool)) for _ in range(pop_size)]
    def length(order):
        total, curr = 0, 0
        for idx in order:
            total += dist_matrix[(curr, idx)]
            curr = idx
        total += dist_matrix[(curr, num_points - 1)]
        return total
    for _ in range(generations):
        population = sorted(population, key=length)
        new_gen = population[:10]
        while len(new_gen) < pop_size:
            p1, p2 = random.sample(population[:30], 2)
            cut = random.randint(1, len(gene_pool)-2)
            child = p1[:cut] + [g for g in p2 if g not in p1[:cut]]
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(child)), 2)
                child[i], child[j] = child[j], child[i]
            new_gen.append(child)
        population = new_gen
    return population[0], length(population[0])

# ======= Vòng lặp người dùng =======
if __name__ == "__main__":
    while True:
        inp = input("Nhập ID người dùng (hoặc 'q' để thoát) (Ví dụ 17850): ").strip()
        if inp.lower() == 'q':
            print("Thoát chương trình.")
            break
        if not inp.isdigit():
            print("Vui lòng nhập ID hợp lệ.")
            continue

        user_id = int(inp)

        mode = input("Chọn chế độ gợi ý: 1 - Theo tên sản phẩm | 2 - Theo ID người dùng: ").strip()
        if mode == '1':
            keyword = input("Nhập tên sản phẩm: (Ví dụ: White) ").strip()
            try:
                results = recommend_by_name(keyword, 5)
                if not results:
                    print("Không có sản phẩm phù hợp.")
                    continue
                products = [r[0] for r in results]
                print("\n🔍 Gợi ý sản phẩm:")
                for i, (desc, score) in enumerate(results):
                    print(f"{i+1}. {desc} - tương đồng {score:.2f}%")
            except:
                print("Không tìm thấy sản phẩm.")
                continue
        elif mode == '2':
            try:
                products = recommend_by_user(user_id, 5)
                print("\n📦 Gợi ý sản phẩm cho người dùng:")
                for i, desc in enumerate(products):
                    print(f"{i+1}. {desc}")
            except:
                print("Không thể gợi ý cho ID này.")
                continue
        else:
            print("Chọn không hợp lệ. Nhập 1 hoặc 2.")
            continue
        gen = SupermarketGenerator(seed=random.randint(0, 9999))
        gen.generate_layout()
        gen.assign_products(products)
        store = gen.create_store_data()
        grid = store["layout"]["grid"]
        entrance = tuple(store["layout"]["entrance"])
        exit_pos = tuple(store["layout"]["exit"])
        positions = [tuple(store["products"][p]["position"]) for p in store["products"]]

        points = [entrance] + positions + [exit_pos]
        dist_matrix, paths = {}, {}
        for i, a in enumerate(points):
            for j, b in enumerate(points):
                if i != j:
                    p = bfs(grid, a, b)
                    dist_matrix[(i, j)] = len(p)
                    paths[(i, j)] = p

        order, best_len = genetic_algorithm(dist_matrix, len(points))
        full_path = []
        current = 0
        for idx in order:
            full_path += paths[(current, idx)][:-1]
            current = idx
        full_path += paths[(current, len(points)-1)]

        print("\n🛒 Danh sách sản phẩm được gợi ý (theo thứ tự tối ưu):")
        for i, idx in enumerate(order):
            pname = products[idx - 1]
            prod_info = store["products"][pname]
            pos = prod_info["position"]
            zone = prod_info["zone"]
            print(f"{i+1}. {pname} tại vị trí {pos} (quầy: {zone})")


        gen.plot_layout(title="Đường đi tối ưu", path=full_path, save=False)
