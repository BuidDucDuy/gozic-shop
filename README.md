# Gozic Shop API

API quản lý sản phẩm và danh mục, hỗ trợ đăng ký, đăng nhập, reset mật khẩu, thêm/sửa/xóa danh mục và sản phẩm. Được xây dựng bằng Django REST Framework, sử dụng JWT Authentication.

---

## Mô tả dự án

Gozic Shop là một hệ thống API backend cho ứng dụng quản lý sản phẩm.  
Các chức năng chính:
- Đăng ký người dùng
- Đăng nhập với JWT Token
- Reset mật khẩu
- Quản lý danh mục: thêm, sửa, xóa, tìm kiếm theo tên
- Quản lý sản phẩm: thêm, sửa, xóa, tìm kiếm theo tên

---

## Công nghệ sử dụng

- Python 3.x
- Django 4.x
- Django REST Framework
- djangorestframework-simplejwt (JWT Authentication)
- drf-yasg (Swagger API documentation)
- Pillow (Xử lý ảnh)
- ...

---

## Hướng dẫn cài đặt

1. Clone repository:
```bash
git clone git@github.com:BuidDucDuy/gozic-shop.git
cd gozic-shop
