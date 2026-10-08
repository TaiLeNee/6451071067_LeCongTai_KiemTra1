# Kế hoạch và test case đăng nhập Văn phòng điện tử UTC

## 1. Thông tin dự án

| Thuộc tính | Nội dung |
|---|---|
| Tên dự án | UTC Login E2E Testing |
| Trang được kiểm thử | https://vanphongdientu.utc.edu.vn/Login |
| Công cụ dự kiến | Python, Selenium WebDriver, pytest |
| Cách tổ chức mã | Page Object Model; tách base, pages và tests |
| Số test case cơ sở | 25, ID LG-01 đến LG-25 |
| Quản lý mã nguồn | Git và GitHub; mỗi TC có một commit triển khai riêng |
| Báo cáo dự kiến | Tự sinh Excel sau khi chạy pytest |
| Hiện trạng | Chưa chạy các TC trong tài liệu; chưa có tài khoản test hợp lệ |

## 2. Phạm vi và cơ sở thiết kế

Kiểm tra form đăng nhập, validation, thao tác chuột/bàn phím, điều hướng liên kết,
ghi nhớ đăng nhập và trạng thái phiên qua giao diện trình duyệt.

Các phần tử của form được tham chiếu từ ví dụ UTC trong tài liệu buổi 8:
tên đăng nhập, mật khẩu, nút đăng nhập, tùy chọn ghi nhớ, link quên mật khẩu và
nút đăng nhập bằng e-mail UTC. Phải xác nhận lại DOM và hành vi trên website hiện tại
trước khi triển khai locator và assertion.

25 TC là bộ cơ sở theo phạm vi đã chọn, không phải cam kết bao phủ mọi tình huống.
Khi có đặc tả chính thức, bổ sung các tổ hợp dữ liệu, chính sách phiên, CAPTCHA/MFA,
SSO và trình duyệt cần hỗ trợ. LG-16 chỉ kiểm tra điều hướng tới xác thực e-mail;
chưa kiểm tra toàn bộ luồng SSO. Các TC giao diện không thay thế kiểm thử API,
phân quyền phía server hoặc kiểm thử tải JMeter.

## 3. Quy ước dữ liệu và kết quả

| Ký hiệu | Ý nghĩa |
|---|---|
| USER_VALID | Tài khoản test đã được xác nhận tồn tại, hoạt động |
| PASS_VALID | Mật khẩu đúng của USER_VALID |
| PASS_WRONG | Mật khẩu khác PASS_VALID |
| USER_UNKNOWN | Tên tài khoản được xác nhận không tồn tại; không tự giả định một tên bất kỳ là không tồn tại |
| USER_DISABLED | Tài khoản test được chuẩn bị ở trạng thái khóa/vô hiệu |
| USER_LOCKOUT | Tài khoản test riêng dùng kiểm tra giới hạn lần đăng nhập sai |
| PROTECTED_URL | URL đã xác nhận yêu cầu đăng nhập |
| MAX_USERNAME / MAX_PASSWORD | Giới hạn độ dài đã được xác nhận từ đặc tả |
| N_LOCK | Ngưỡng thất bại đã được xác nhận cho cơ chế khóa/giới hạn |

Không ghi mật khẩu thật vào tài liệu hoặc commit. Lấy bí mật từ biến môi trường khi chạy.
Kết quả mong đợi dưới đây là tiêu chí đánh giá, không phải kết quả đã quan sát.
Không tự đặt nội dung thông báo lỗi, độ dài tối đa, thời hạn phiên hoặc số lần khóa.

| Trạng thái | Ý nghĩa |
|---|---|
| Not Run | Chưa thực hiện; cần kiểm tra điều kiện trước khi chạy |
| Pass | Đã thực hiện và tất cả assertion đạt |
| Fail | Đã thực hiện nhưng hành vi khác tiêu chí mong đợi đã xác nhận |
| Blocked | Không đủ điều kiện như tài khoản, dữ liệu test hoặc đặc tả |
| Error | Lỗi môi trường/công cụ/chuẩn bị làm không thể đánh giá TC |

Các trạng thái ban đầu trong tài liệu phản ánh thông tin hiện có. Not Run không có nghĩa
đã xác nhận website hoặc locator hoạt động. Khi pytest skip do thiếu điều kiện, báo cáo
Excel ghi Blocked và lý do; trường hợp không áp dụng theo đặc tả ghi rõ Not Applicable,
không cộng vào số Pass. Những TC không được chọn trong lần chạy giữ Not Run.

## 4. Danh sách tổng hợp

| ID | Nội dung | Ưu tiên | Trạng thái ban đầu |
|---|---|---|---|
| LG-01 | Hiển thị form đăng nhập | Cao | Not Run |
| LG-02 | Che mật khẩu | Cao | Not Run |
| LG-03 | Đăng nhập thành công | Cao | Blocked |
| LG-04 | Tài khoản đúng, mật khẩu sai | Cao | Blocked |
| LG-05 | Tài khoản không tồn tại | Cao | Blocked |
| LG-06 | Bỏ trống cả hai trường | Cao | Not Run |
| LG-07 | Bỏ trống tên đăng nhập | Cao | Not Run |
| LG-08 | Bỏ trống mật khẩu | Cao | Not Run |
| LG-09 | Tên đăng nhập chỉ có khoảng trắng | Trung bình | Not Run |
| LG-10 | Mật khẩu chỉ có khoảng trắng | Trung bình | Blocked |
| LG-11 | Gửi form bằng Enter | Trung bình | Blocked |
| LG-12 | Sửa dữ liệu sau lần thất bại | Cao | Blocked |
| LG-13 | Bật/tắt ghi nhớ đăng nhập | Trung bình | Not Run |
| LG-14 | Ghi nhớ sau khi mở lại trình duyệt | Cao | Blocked |
| LG-15 | Điều hướng quên mật khẩu | Trung bình | Not Run |
| LG-16 | Điều hướng đăng nhập e-mail UTC | Trung bình | Not Run |
| LG-17 | Điều hướng và thao tác bằng bàn phím | Trung bình | Not Run |
| LG-18 | Refresh sau khi đăng nhập | Cao | Blocked |
| LG-19 | Trang bảo vệ khi chưa đăng nhập | Cao | Blocked |
| LG-20 | Truy cập lại sau đăng xuất | Cao | Blocked |
| LG-21 | Khoảng trắng đầu/cuối tên đăng nhập | Trung bình | Blocked |
| LG-22 | Hoa/thường của tên đăng nhập | Trung bình | Blocked |
| LG-23 | Biên độ dài trường nhập | Trung bình | Blocked |
| LG-24 | Tài khoản khóa/vô hiệu | Cao | Blocked |
| LG-25 | Đăng nhập sai nhiều lần | Cao | Blocked |

## 5. Test case chi tiết

### LG-01 - Hiển thị form đăng nhập

- Mục tiêu: xác nhận người dùng tiếp cận được các điều khiển trên form.
- Tiền điều kiện: website truy cập được; trình duyệt chưa đăng nhập.
- Dữ liệu: không cần tài khoản.
- Các bước:
  1. Mở trang /Login.
  2. Chờ form hiển thị.
  3. Kiểm tra ô tên đăng nhập, ô mật khẩu và nút đăng nhập.
  4. Kiểm tra nhãn/ô ghi nhớ, link quên mật khẩu và nút e-mail UTC theo giao diện đã xác nhận.
- Kết quả mong đợi: các điều khiển cần thiết hiển thị; ô nhập và nút đăng nhập có thể thao tác.
- Trạng thái ban đầu: Not Run.

### LG-02 - Che mật khẩu

- Mục tiêu: mật khẩu không hiển thị nguyên văn trên màn hình.
- Tiền điều kiện: form đăng nhập hiển thị.
- Dữ liệu: username `test_validation`, password `sample-password`.
- Các bước:
  1. Nhập dữ liệu vào hai ô, không gửi form.
  2. Quan sát ký tự mật khẩu hiển thị.
  3. Kiểm tra thuộc tính type của ô mật khẩu.
- Kết quả mong đợi: ô có type=password, ký tự được che; dữ liệu nhập vẫn được giữ trong ô.
- Trạng thái ban đầu: Not Run.

### LG-03 - Đăng nhập thành công

- Mục tiêu: tài khoản hợp lệ truy cập được workspace được phép.
- Tiền điều kiện: có USER_VALID/PASS_VALID; tài khoản hoạt động; đã xác nhận dấu hiệu tài khoản sau đăng nhập.
- Dữ liệu: USER_VALID/PASS_VALID.
- Các bước:
  1. Mở /Login trong phiên sạch.
  2. Nhập tài khoản và mật khẩu đúng.
  3. Bấm đăng nhập và chờ phản hồi.
  4. Kiểm tra dấu hiệu người dùng đã xác thực và đúng danh tính.
- Kết quả mong đợi: đăng nhập thành công và hiển thị đúng người dùng; không chỉ dựa vào URL thay đổi.
- Trạng thái ban đầu: Blocked - chưa có tài khoản test hợp lệ.

### LG-04 - Tài khoản đúng, mật khẩu sai

- Mục tiêu: từ chối thông tin xác thực sai của tài khoản tồn tại.
- Tiền điều kiện: có USER_VALID/PASS_VALID, tài khoản chưa bị khóa; biết phản hồi lỗi cần kiểm tra.
- Dữ liệu: USER_VALID/PASS_WRONG, với PASS_WRONG khác PASS_VALID.
- Các bước:
  1. Mở /Login trong phiên sạch.
  2. Nhập username đúng và password sai.
  3. Bấm đăng nhập và chờ phản hồi lỗi.
  4. Kiểm tra chưa được xác thực, form vẫn có thể thao tác.
- Kết quả mong đợi: không đăng nhập; phản hồi lỗi phù hợp; không kết luận chỉ vì chưa rời /Login.
- Trạng thái ban đầu: Blocked - chưa có tài khoản được xác nhận tồn tại.

### LG-05 - Tài khoản không tồn tại

- Mục tiêu: tài khoản không tồn tại không được xác thực.
- Tiền điều kiện: USER_UNKNOWN được xác nhận không tồn tại; biết phản hồi mong đợi.
- Dữ liệu: USER_UNKNOWN/password bất kỳ không rỗng.
- Các bước:
  1. Mở /Login.
  2. Nhập dữ liệu.
  3. Bấm đăng nhập và chờ phản hồi.
  4. Kiểm tra lỗi và trạng thái chưa xác thực.
- Kết quả mong đợi: không đăng nhập; thông báo theo thiết kế, có thể là lỗi chung cho thông tin không hợp lệ.
- Trạng thái ban đầu: Blocked - chưa có dữ liệu tài khoản không tồn tại được xác nhận.

### LG-06 - Bỏ trống cả hai trường

- Mục tiêu: không cho đăng nhập khi thiếu cả username và password.
- Tiền điều kiện: form hiển thị; xác định validation thuộc trình duyệt hay ứng dụng.
- Dữ liệu: username rỗng, password rỗng.
- Các bước:
  1. Xóa nội dung cả hai ô.
  2. Bấm đăng nhập.
  3. Chờ và kiểm tra phản hồi yêu cầu trường bắt buộc.
  4. Kiểm tra vẫn chưa đăng nhập.
- Kết quả mong đợi: xuất hiện validation; không được xác thực. Validation HTML có thể chỉ báo trường bắt buộc đầu tiên.
- Trạng thái ban đầu: Not Run.

### LG-07 - Bỏ trống tên đăng nhập

- Mục tiêu: username bắt buộc được kiểm tra.
- Tiền điều kiện: form hiển thị; biết dấu hiệu validation.
- Dữ liệu: username rỗng, password `sample-password`.
- Các bước:
  1. Để trống username, nhập password.
  2. Bấm đăng nhập.
  3. Chờ và kiểm tra validation username.
  4. Kiểm tra chưa được xác thực.
- Kết quả mong đợi: yêu cầu nhập username; không đăng nhập.
- Trạng thái ban đầu: Not Run.

### LG-08 - Bỏ trống mật khẩu

- Mục tiêu: password bắt buộc được kiểm tra; đây là ca validation của bài tập buổi 8.
- Tiền điều kiện: form hiển thị; biết dấu hiệu validation; không cần tài khoản thật.
- Dữ liệu: username `test_validation`, password rỗng.
- Các bước:
  1. Nhập username và xóa password.
  2. Bấm đăng nhập.
  3. Kiểm tra validity.valueMissing/validationMessage nếu dùng required HTML, hoặc thông báo riêng của ứng dụng.
  4. Kiểm tra chưa được xác thực.
- Kết quả mong đợi: validation mật khẩu xuất hiện; không đăng nhập.
- Trạng thái ban đầu: Not Run.

### LG-09 - Tên đăng nhập chỉ có khoảng trắng

- Mục tiêu: username toàn khoảng trắng không được xác thực thành tài khoản hợp lệ.
- Tiền điều kiện: biết cách xử lý username khoảng trắng và phản hồi lỗi của web.
- Dữ liệu: username gồm ba dấu cách, password `sample-password`.
- Các bước:
  1. Nhập dữ liệu.
  2. Bấm đăng nhập.
  3. Chờ validation hoặc phản hồi từ chối đăng nhập.
  4. Kiểm tra trạng thái chưa xác thực.
- Kết quả mong đợi: không đăng nhập; nếu trim thành rỗng thì phản hồi theo validation trường bắt buộc, nếu không trim thì theo lỗi xác thực.
- Trạng thái ban đầu: Not Run; nếu chưa xác định được tiêu chí phản hồi thì chuyển Blocked trước khi tự động hóa.

### LG-10 - Mật khẩu chỉ có khoảng trắng

- Mục tiêu: mật khẩu toàn khoảng trắng không khớp tài khoản test không có mật khẩu đó.
- Tiền điều kiện: USER_VALID tồn tại; PASS_VALID được xác nhận khác ba dấu cách; biết phản hồi mong đợi.
- Dữ liệu: USER_VALID/password gồm ba dấu cách.
- Các bước:
  1. Nhập dữ liệu.
  2. Bấm đăng nhập và chờ phản hồi.
  3. Kiểm tra validation hoặc lỗi xác thực phù hợp.
  4. Kiểm tra chưa đăng nhập.
- Kết quả mong đợi: từ chối xác thực; không tự giả định mọi hệ thống cấm mật khẩu chứa khoảng trắng.
- Trạng thái ban đầu: Blocked - thiếu tài khoản test hợp lệ.

### LG-11 - Gửi form bằng Enter

- Mục tiêu: thao tác Enter thực hiện gửi form nếu chức năng được hỗ trợ.
- Tiền điều kiện: có USER_VALID/PASS_VALID; đặc tả xác nhận hỗ trợ Enter.
- Dữ liệu: USER_VALID/PASS_VALID.
- Các bước:
  1. Nhập thông tin hợp lệ.
  2. Giữ focus tại ô password.
  3. Nhấn Enter và chờ kết quả.
  4. Kiểm tra đúng tài khoản đã đăng nhập.
- Kết quả mong đợi: kết quả tương đương bấm nút đăng nhập; nếu đặc tả không hỗ trợ Enter thì ghi Not Applicable.
- Trạng thái ban đầu: Blocked - thiếu tài khoản và xác nhận hỗ trợ Enter.

### LG-12 - Sửa dữ liệu sau lần đăng nhập thất bại

- Mục tiêu: người dùng sửa lỗi và đăng nhập lại được trong cùng phiên trình duyệt.
- Tiền điều kiện: có USER_VALID/PASS_VALID, biết phản hồi lỗi; tài khoản chưa ở gần ngưỡng khóa.
- Dữ liệu: lần đầu USER_VALID/PASS_WRONG; lần sau USER_VALID/PASS_VALID.
- Các bước:
  1. Đăng nhập bằng mật khẩu sai.
  2. Chờ phản hồi lỗi của lần đầu.
  3. Xóa mật khẩu cũ, nhập mật khẩu đúng và gửi lại.
  4. Chờ và kiểm tra trạng thái xác thực đúng người dùng.
- Kết quả mong đợi: lần đầu bị từ chối; lần sau thành công; lỗi cũ không cản thao tác hoặc còn hiển thị sai ở trang đích.
- Trạng thái ban đầu: Blocked - thiếu tài khoản test hợp lệ.

### LG-13 - Bật/tắt ghi nhớ đăng nhập

- Mục tiêu: điều khiển ghi nhớ thay đổi trạng thái đúng.
- Tiền điều kiện: xác định checkbox thật và phần nhãn có thể click.
- Dữ liệu: không cần tài khoản.
- Các bước:
  1. Mở form, đọc trạng thái chọn hiện tại.
  2. Nếu chưa chọn, click phần nhãn/ô hiển thị để chọn.
  3. Kiểm tra checkbox thật đã chọn.
  4. Click lần nữa, kiểm tra checkbox thật bỏ chọn.
- Kết quả mong đợi: hai trạng thái được thay đổi đúng. Nếu input thật bị ẩn thì click nhãn hiển thị, không ép click phần tử ẩn.
- Trạng thái ban đầu: Not Run.

### LG-14 - Ghi nhớ sau khi mở lại trình duyệt

- Mục tiêu: tùy chọn ghi nhớ duy trì phiên theo chính sách đã xác nhận.
- Tiền điều kiện: có tài khoản hợp lệ, PROTECTED_URL và chính sách ghi nhớ; dùng profile test riêng.
- Dữ liệu: USER_VALID/PASS_VALID; chọn ghi nhớ.
- Các bước:
  1. Chọn ghi nhớ rồi đăng nhập thành công.
  2. Đóng toàn bộ trình duyệt test đúng cách.
  3. Mở lại trình duyệt bằng cùng profile test, không copy cookie thủ công.
  4. Truy cập PROTECTED_URL và kiểm tra trạng thái xác thực.
- Kết quả mong đợi: trạng thái sau restart đúng chính sách. Ca này không chứng minh toàn bộ thời hạn ghi nhớ hoặc hành vi khi bỏ chọn.
- Trạng thái ban đầu: Blocked - thiếu tài khoản, URL bảo vệ và chính sách ghi nhớ.

### LG-15 - Điều hướng quên mật khẩu

- Mục tiêu: link mở đúng trang khôi phục tài khoản.
- Tiền điều kiện: link hiển thị; đã xác nhận URL và dấu hiệu nội dung trang đích.
- Dữ liệu: không cần tài khoản.
- Các bước:
  1. Mở form đăng nhập.
  2. Click link quên mật khẩu.
  3. Chờ trang đích.
  4. Kiểm tra URL và nội dung/form khôi phục đặc trưng.
- Kết quả mong đợi: mở đúng trang khôi phục, không phải trang lỗi. Tài liệu tham chiếu đường dẫn /Login/GetPass; cần xác nhận lại. Không gửi yêu cầu khôi phục trong ca này.
- Trạng thái ban đầu: Not Run.

### LG-16 - Điều hướng đăng nhập bằng e-mail UTC

- Mục tiêu: nút e-mail UTC đưa người dùng tới luồng xác thực đúng.
- Tiền điều kiện: đã xác nhận tên miền/URL và dấu hiệu trang xác thực đích.
- Dữ liệu: không cần nhập thông tin SSO.
- Các bước:
  1. Mở form đăng nhập.
  2. Click nút e-mail UTC.
  3. Chuyển sang tab/cửa sổ mới nếu thao tác mở tab mới.
  4. Chờ và kiểm tra trang xác thực đích.
- Kết quả mong đợi: đúng trang xác thực; không phải trang lỗi. Chưa đánh giá xác thực, MFA hoặc callback SSO.
- Trạng thái ban đầu: Not Run.

### LG-17 - Điều hướng và nhập liệu bằng bàn phím

- Mục tiêu: có thể sử dụng các điều khiển form bằng bàn phím.
- Tiền điều kiện: xác nhận thứ tự focus và cách hiển thị focus theo thiết kế hiện tại.
- Dữ liệu: username `keyboard_test`, password `sample-password`; không gửi form.
- Các bước:
  1. Đặt focus vào điều khiển đầu tiên của form.
  2. Dùng Tab đi qua các điều khiển có thể focus; dùng Shift+Tab quay lại.
  3. Nhập dữ liệu tại username/password bằng bàn phím.
  4. Kiểm tra thứ tự, vị trí focus và nội dung nhập; kiểm tra bật/tắt checkbox bằng bàn phím nếu thiết kế hỗ trợ.
- Kết quả mong đợi: thứ tự hợp lý theo thiết kế, focus nhìn thấy, không bị kẹt; dữ liệu nhập đúng. Input ẩn không bắt buộc xuất hiện trong thứ tự Tab.
- Trạng thái ban đầu: Not Run; thiếu tiêu chí focus sẽ ghi Blocked cho phần tự động hóa tương ứng.

### LG-18 - Refresh sau khi đăng nhập

- Mục tiêu: tải lại trang không làm mất phiên còn hiệu lực.
- Tiền điều kiện: có tài khoản hợp lệ và dấu hiệu xác thực.
- Dữ liệu: USER_VALID/PASS_VALID.
- Các bước:
  1. Đăng nhập thành công.
  2. Kiểm tra danh tính người dùng.
  3. Refresh trang.
  4. Chờ trang sẵn sàng và kiểm tra lại danh tính.
- Kết quả mong đợi: vẫn được xác thực đúng người dùng trong phiên còn hiệu lực.
- Trạng thái ban đầu: Blocked - thiếu tài khoản test hợp lệ.

### LG-19 - Mở trang bảo vệ khi chưa đăng nhập

- Mục tiêu: người chưa xác thực không truy cập được nội dung được bảo vệ.
- Tiền điều kiện: có PROTECTED_URL; biết phản hồi chuyển tới Login/từ chối truy cập; dùng phiên sạch.
- Dữ liệu: PROTECTED_URL.
- Các bước:
  1. Mở trình duyệt với phiên chưa đăng nhập.
  2. Điều hướng trực tiếp tới PROTECTED_URL.
  3. Chờ phản hồi chuyển hướng/từ chối truy cập.
  4. Kiểm tra không hiển thị nội dung bảo vệ và dấu hiệu người dùng đã xác thực.
- Kết quả mong đợi: không truy cập được dữ liệu bảo vệ; kết quả đúng chính sách điều hướng. Không dùng URL trang public để kiểm tra ca này.
- Trạng thái ban đầu: Blocked - chưa có URL bảo vệ được xác nhận.

### LG-20 - Truy cập lại sau đăng xuất

- Mục tiêu: phiên đã logout không tiếp tục truy cập dữ liệu bảo vệ.
- Tiền điều kiện: có tài khoản hợp lệ, logout và PROTECTED_URL.
- Dữ liệu: USER_VALID/PASS_VALID, PROTECTED_URL.
- Các bước:
  1. Đăng nhập thành công và xác nhận danh tính.
  2. Đăng xuất, chờ trạng thái chưa xác thực.
  3. Mở trực tiếp lại PROTECTED_URL.
  4. Refresh và kiểm tra phản hồi từ chối/chuyển hướng.
- Kết quả mong đợi: không truy cập được dữ liệu bảo vệ sau logout. Ca này chưa kiểm tra lịch sử Back/cache hay thu hồi token ở API.
- Trạng thái ban đầu: Blocked - thiếu tài khoản và URL bảo vệ.

### LG-21 - Khoảng trắng đầu/cuối tên đăng nhập

- Mục tiêu: kiểm tra xử lý khoảng trắng theo chính sách username.
- Tiền điều kiện: có tài khoản hợp lệ; xác nhận hệ thống trim hay từ chối.
- Dữ liệu: USER_VALID có thêm hai dấu cách đầu và cuối, PASS_VALID.
- Các bước:
  1. Nhập username có khoảng trắng đầu/cuối và mật khẩu đúng.
  2. Gửi form, chờ xử lý.
  3. Kiểm tra kết quả theo chính sách đã xác nhận.
- Kết quả mong đợi: nếu trim thì đăng nhập đúng USER_VALID; nếu không chấp nhận thì có lỗi và không xác thực. Không chọn kỳ vọng tùy theo kết quả chạy để làm test Pass.
- Trạng thái ban đầu: Blocked - thiếu tài khoản và chính sách trim.

### LG-22 - Hoa/thường của tên đăng nhập

- Mục tiêu: kiểm tra chính sách phân biệt hoa/thường.
- Tiền điều kiện: username có chữ cái; biết chính sách case sensitivity; biến thể không thuộc một tài khoản khác.
- Dữ liệu: biến thể USER_VALID chỉ đổi hoa/thường, PASS_VALID.
- Các bước:
  1. Nhập biến thể username và password đúng.
  2. Gửi form và chờ kết quả.
  3. Nếu được chấp nhận, kiểm tra vẫn đúng danh tính USER_VALID.
  4. Nếu bị từ chối theo chính sách, kiểm tra phản hồi lỗi.
- Kết quả mong đợi: đúng chính sách đã xác nhận. Username toàn số không thích hợp cho ca này.
- Trạng thái ban đầu: Blocked - thiếu tài khoản và chính sách hoa/thường.

### LG-23 - Biên độ dài của trường nhập

- Mục tiêu: kiểm tra tại/vượt giới hạn của username và password.
- Tiền điều kiện: xác nhận MAX_USERNAME, MAX_PASSWORD, đơn vị độ dài và cách xử lý giới hạn ở UI/ứng dụng.
- Dữ liệu: cho từng trường, chuỗi ASCII có độ dài N-1, N và N+1; N là giới hạn trường đó.
- Các bước:
  1. Với username, lần lượt nhập chuỗi N-1, N, N+1 trong form mới.
  2. Kiểm tra số ký tự thực tế được giữ và validation theo đặc tả.
  3. Lặp lại với password; trường còn lại nhập dữ liệu không rỗng để tránh nhiễu validation rỗng.
  4. Nếu giới hạn được kiểm tra sau gửi form, kiểm tra thông báo tương ứng cho từng biên.
- Kết quả mong đợi: N-1 và N không bị từ chối riêng vì vượt độ dài; N+1 bị chặn nhập hoặc báo lỗi độ dài theo đặc tả. Dữ liệu giả có thể bị từ chối xác thực và không được coi là lỗi biên độ dài.
- Trạng thái ban đầu: Blocked - chưa xác nhận giới hạn và cách xử lý. Kiểm tra maxlength trên UI chưa chứng minh backend áp dụng cùng giới hạn.

### LG-24 - Tài khoản khóa/vô hiệu

- Mục tiêu: tài khoản không được phép hoạt động không thể đăng nhập.
- Tiền điều kiện: có USER_DISABLED được chuẩn bị đúng trạng thái và mật khẩu đúng; biết phản hồi mong đợi.
- Dữ liệu: USER_DISABLED và mật khẩu đúng của tài khoản đó.
- Các bước:
  1. Nhập thông tin của tài khoản khóa/vô hiệu.
  2. Bấm đăng nhập và chờ phản hồi.
  3. Kiểm tra từ chối xác thực và thông báo theo thiết kế.
- Kết quả mong đợi: không được đăng nhập. Nếu khóa và vô hiệu là hai trạng thái riêng thì chạy hai bộ dữ liệu hoặc tách thêm TC khi có đặc tả.
- Trạng thái ban đầu: Blocked - chưa có tài khoản trạng thái đặc biệt.

### LG-25 - Đăng nhập sai nhiều lần

- Mục tiêu: kiểm tra cơ chế giới hạn/khóa theo đặc tả; không tự giả định có khóa sau 5 lần.
- Tiền điều kiện: môi trường cho phép kiểm tra; USER_LOCKOUT riêng; bộ đếm sai được reset; biết N_LOCK, cơ chế giới hạn và phản hồi. Không dùng tài khoản cá nhân.
- Dữ liệu: USER_LOCKOUT, password sai và password đúng của tài khoản test.
- Các bước:
  1. Gửi từng lần đăng nhập sai, chờ phản hồi mới hoàn tất trước khi gửi lần kế tiếp.
  2. Kiểm tra hành vi trước và tại ngưỡng N_LOCK theo chính sách.
  3. Nếu chính sách là khóa, thử mật khẩu đúng trong thời gian khóa.
  4. Kiểm tra từ chối theo chính sách; nhờ người quản trị/reset tài khoản trước lần chạy khác.
- Kết quả mong đợi: cơ chế giới hạn hoạt động đúng; với khóa tài khoản, mật khẩu đúng không bỏ qua thời gian khóa. Nếu dùng CAPTCHA/rate limit thay vì khóa thì sửa kỳ vọng theo cơ chế thực tế.
- Trạng thái ban đầu: Blocked - thiếu tài khoản riêng và chính sách. Không bật ca này trong lần chạy mặc định khi chưa đủ điều kiện.

## 6. Quản lý commit

- Commit bộ khung, Page Objects và tài liệu kế hoạch riêng, trước các commit TC.
- Mỗi TC có một file như tests/login/test_lg01_form.py; commit chứa mã và cập nhật tài liệu của đúng TC đó.
- Kiểm tra từng TC trước commit; ghi đúng Not Run/Blocked nếu chưa thực thi được.
- Mẫu thông điệp: `test(LG-01): verify login form visibility`.
- Không commit mật khẩu, profile trình duyệt, cookie hoặc cấu hình bí mật.
- Không gom 25 TC vào một commit rồi tạo các commit rỗng để giả lịch sử từng TC.
- Thay đổi framework hoặc code sinh báo cáo có commit riêng, không tính là TC.

## 7. Dữ liệu cho báo cáo Excel tự động

| Cột | Nội dung |
|---|---|
| Run ID / Thời gian | Định danh và thời điểm lần chạy |
| Git commit | Mã commit của mã nguồn đang được kiểm thử |
| TC ID / Tên | ID LG-xx và tên ca |
| Tiền điều kiện | Điều kiện thực thi của TC |
| Dữ liệu | Ký hiệu dữ liệu; không xuất mật khẩu thật |
| Bước thực hiện | Các bước trong mục 5 |
| Mong đợi | Tiêu chí đánh giá đã xác nhận |
| Thực tế | Kết quả quan sát/assertion hoặc lý do chưa chạy |
| Trạng thái | Pass, Fail, Blocked, Error, Not Run hoặc Not Applicable |
| Thời lượng | Thời gian thực thi, giây |
| Bằng chứng | Đường dẫn screenshot khi cần |

Báo cáo được tạo từ kết quả pytest của lần chạy, không tự gán Pass theo tài liệu.
Ghi lỗi setup/teardown riêng để tránh đếm test Pass khi không hoàn thành vòng đời.
Các ca không được chọn giữ Not Run, các ca thiếu điều kiện ghi Blocked và lý do.
Tỷ lệ Pass tính trên các ca đã được đánh giá Pass/Fail; luôn hiển thị riêng số Blocked,
Error, Not Run và Not Applicable để người đọc thấy phần chưa được kiểm tra.
Chỉ chụp bằng chứng cần thiết; tránh đưa bí mật hoặc thông tin cá nhân vào báo cáo.

## 8. Checklist trước mỗi lần chạy

- Xác nhận đúng môi trường và URL.
- Xác nhận tài khoản test và trạng thái ban đầu cho các ca cần xác thực.
- Kiểm tra locator bằng DOM thực tế và dùng Explicit Wait cho điều kiện cần thiết.
- Mỗi TC độc lập, không phụ thuộc TC trước đã đăng nhập hoặc tạo phiên.
- Không dùng Thread.sleep/time.sleep để đoán thời gian phản hồi.
- Khi thiếu đặc tả, ghi Blocked; khi thay đổi kỳ vọng phải có cơ sở xác nhận.
- Sau chạy, xem Excel và bằng chứng; cập nhật kết quả theo lần chạy thực tế.

## 9. Tham chiếu

- Tài liệu buoi8.pdf: slide 19-38 (form UTC, locator và checkbox), 41-45 (wait),
  46-55 (POM), 48 (cấu trúc E2E), 60-63 (headless, bằng chứng và bài thực hành).
- Các quy tắc nghiệp vụ còn thiếu phải được xác nhận từ đặc tả hoặc người quản lý hệ thống,
  không được suy ra chỉ từ ví dụ trên slide.
