# VKU Schedule Model Server

Server API sử dụng AI model (T5) để chuyển đổi yêu cầu lịch học từ ngôn ngữ tự nhiên sang các ràng buộc JSON, sau đó tích hợp với server NSGA-II để tạo lịch học tối ưu.

## Tính năng

- 🤖 Sử dụng T5 model (`conanWinner/model_scheduler`) để xử lý prompt tiếng Việt
- 🔄 Convert yêu cầu lịch học từ ngôn ngữ tự nhiên thành JSON constraints
- 📅 Tích hợp với server NSGA-II để tạo lịch học tối ưu
- 📚 API documentation với Swagger UI
- 🐳 Hỗ trợ Docker containerization

## Cài đặt

### Yêu cầu

- Python 3.10+
- pip hoặc uv

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy server

```bash
python main.py
```

Server sẽ chạy tại `http://localhost:5000`

### Sử dụng Docker

```bash
docker build -t vku-schedule-model .
docker run -p 5000:5000 vku-schedule-model
```

## API Endpoints

### POST `/api/convert`

Convert prompt và tạo lịch học

**Request:**
```json
{
  "queries": [
    "Phân tích dữ liệu",
    "Cơ sở dữ liệu"
  ],
  "prompt": "Tôi chỉ học nếu lớp bắt đầu sau 10 giờ sáng. Tôi thích lịch học trải đều trong tuần"
}
```

**Response:**
```json
{
  "message": "Success",
  "schedules": [
    {
      "schedule": [...],
      "score": 0.95
    }
  ]
}
```

### GET `/health`

Kiểm tra trạng thái server và model

### GET `/api-docs`

Swagger UI documentation

## Công nghệ sử dụng

- **Flask**: Web framework
- **Transformers (T5)**: AI model để xử lý ngôn ngữ tự nhiên
- **Flasgger**: API documentation
- **Docker**: Containerization

## Môi trường

Model server này hoạt động kết hợp với:
- **NSGA-II Server**: Server tạo lịch học tối ưu (http://20.106.16.223:8001)

## Cấu hình

Có thể cấu hình qua environment variables:

- `MODEL_PATH`: Đường dẫn model (mặc định: `conanWinner/model_scheduler`)
- `HOST`: Host server (mặc định: `0.0.0.0`)
- `PORT`: Port server (mặc định: `5000`)
- `DEVICE`: Device để chạy model (`cuda` hoặc `cpu`)
- `USE_FP16`: Sử dụng FP16 để tiết kiệm bộ nhớ (mặc định: `True` nếu có CUDA)

