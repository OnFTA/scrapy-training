# scrapy-training
Mục đích: Áp dụng những kiến thức vào thực hành xây dựng một project crawl dữ liệu.
Các kiến thức sử dụng trong project: scrapy, docker, quy trình crawl dữ liệu.

Yêu cầu: Áp dụng đúng quy trình crawl và toàn bộ kiến thức đã được tìm hiểu:

-  Chạy scrapy với các tùy chọn:logs, jobs, cache, splash, triển khai crawl trên scrapinghub. (scrapinghub.com)
-  Thực hiện tạo dockerfile để Build image scrapy và docker-compose.
-  Triển khai project lên server.

Nội dung crawl: thực hiện crawl các trang web sau:

```
- http://xemphimbox.com/phim-le/
- http://phimbathu.com/danh-sach/phim-le.html
- http://phimvuihd.net/phim-le/
- http://phimnhanh.com/phim-le
```

Các trường cần lấy: 
<kbd>(url_sha1,title,url,image,type,quality,year,category,tags,description,time,actor,imdb,view,country,crawl_at)</kbd>
Dữ liệu được lưu trữ trong container mongodb.
