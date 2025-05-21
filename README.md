# Tổng Quan Demo
Dự án này mô phỏng việc tạo bản đồ siêu thị và gợi ý sản phẩm cho người dùng dựa trên sở thích hoặc lịch sử mua sắm của họ. Nó tích hợp một số kỹ thuật tiên tiến, bao gồm tạo bản đồ siêu thị, gợi ý sản phẩm theo tên hoặc theo lịch sử người dùng, thuật toán tìm đường ngắn nhất (BFS) và Thuật toán Di truyền (GA) để giải quyết vấn đề TSP (Traveling Salesman Problem) tối ưu hóa lộ trình lấy sản phẩm.
# Chức năng
Tạo bản đồ siêu thị với nhiều khu vực khác nhau.
Gán sản phẩm vào bản đồ.
Gợi ý sản phẩm cho người dùng theo ID người dùng hoặc tên sản phẩm 
Tối ưu hóa lộ trình mà người dùng nên đi qua siêu thị bằng thuật toán di truyền.
# Tạo Bản Đồ Siêu Thị
Class SupermarketGenerator tạo một bản đồ siêu thị ngẫu nhiên, gán các khu vực sản phẩm, vị trí cửa ra vào và cửa thoát, và xác thực tính khả dụng giữa các điểm này. Bản đồ siêu thị được thể hiện dưới dạng lưới, trong đó các khu vực và sản phẩm được gán các vị trí cụ thể.
Các loại khu vực: Bản đồ chứa nhiều loại khu vực (ví dụ: A1, A2, A3, v.v.).
Cửa ra vào và cửa thoát: Các vị trí này được xác định trong lưới.
Gán sản phẩm ngẫu nhiên: Sản phẩm được gán vào các vị trí ngẫu nhiên và tính toán khu vực sản phẩm gần nhất cho mỗi mặt hàng
# Gợi Ý Sản Phẩm
Theo Tên Sản Phẩm: Sử dụng vector hóa TF-IDF để gợi ý các sản phẩm tương tự với tên sản phẩm đã cho.
Theo ID Người Dùng: Dựa trên lịch sử mua sắm của người dùng, hệ thống gợi ý sản phẩm sử dụng lọc cộng tác với thuật toán SVD (Phân tích Giá trị Kỳ dị).
# Tối Ưu Hóa Lộ Trình
Sử dụng Thuật toán Tìm kiếm theo chiều rộng (BFS) để tính toán lộ trình ngắn nhất giữa các điểm (cửa ra vào, cửa thoát, khu vực sản phẩm, và sản phẩm) trong siêu thị. Sau đó, một Thuật toán Di truyền (GA) được sử dụng để giải quyết bài toán TSP (Traveling Salesman Problem) nhằm xác định lộ trình tối ưu để lấy các sản phẩm đã được gợi ý.
# Kết quả demo 
![image](https://github.com/user-attachments/assets/700be2f2-b08b-47f9-ba8a-e4aa3a0f801e)
![image](https://github.com/user-attachments/assets/53ef5f4c-c6f8-45d3-9435-536cf73f3396)
