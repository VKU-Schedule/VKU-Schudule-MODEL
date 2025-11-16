from flask import Blueprint, request, jsonify, render_template
from app.model import model_instance
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/convert', methods=['POST'])
def predict_endpoint():
    """
    Convert prompt và tạo lịch học
    ---
    tags:
      - Convert
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - queries
            - prompt
          properties:
            queries:
              type: array
              description: Danh sách các môn học (có thể kèm sub_topic với format "course_name @ sub_topic")
              items:
                type: string
              example:
                - "Phân tích dữ liệu @ Pandas, trực quan hóa với Matplotlib"
                - "Cơ sở dữ liệu @ Cơ sở dữ liệu"
                - "Xử lý dữ liệu"
            prompt:
              type: string
              description: Yêu cầu về lịch học bằng ngôn ngữ tự nhiên (sẽ được model xử lý và convert thành ràng buộc)
              example: "Tôi chỉ học nếu lớp bắt đầu sau 10 giờ sáng. Tôi thích lịch học trải đều trong tuần"
    responses:
      200:
        description: Danh sách các lịch học được tạo
        schema:
          type: object
          properties:
            message:
              type: string
            schedules:
              type: array
              items:
                type: object
                properties:
                  schedule:
                    type: array
                  score:
                    type: number
      400:
        description: Thiếu tham số queries hoặc prompt, hoặc request không phải JSON
      502:
        description: Lỗi kết nối tới server NSGA-II hoặc lỗi xử lý từ server
    """
    # Kiểm tra xem request có chứa JSON không
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if 'queries' not in data:
        return jsonify({"error": "Missing 'text' field in request"}), 400

    queries = data['queries']
    prompt = data['prompt']

    result = model_instance.predict(prompt)
    print(result["result"])

    # forward to server nsga2
    server_nsga2_url = 'http://20.106.16.223:8001/api/schedule'
    try:
        response_from_server_nsga2 = requests.post(
            server_nsga2_url, 
            json={'queries': queries, 'prompt': result["result"]}
        )
        if response_from_server_nsga2.status_code == 200:
            try:
                ans = response_from_server_nsga2.json()
            except Exception as e:
                print("Không parse được JSON từ server nsga2:", e)
                return jsonify({"error": "Response từ server nsga2 không phải JSON"}), 502
        else:
            print("Server nsga2 trả về mã lỗi:", response_from_server_nsga2.status_code)
            return jsonify({"error": f"Lỗi từ server nsga2: {response_from_server_nsga2.status_code}", 
                            "details": response_from_server_nsga2.text}), 502
    except Exception as ex:
        print("Không gọi được server nsga2:", ex)
        return jsonify({"error": "Không kết nối được tới server nsga2", "details": str(ex)}), 502

    message = ans.get("message", "No message available")
    schedules = ans.get("schedules", [])

    return jsonify({
        "message": message,
        "schedules": schedules
    })

@main_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Trạng thái server và model
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
            model_loaded:
              type: boolean
              description: Model đã được load hay chưa
    """
    return jsonify({
        "status": "ok",
        "model_loaded": model_instance.model is not None
    })

@main_bp.route('/', methods=['GET'])
def home():
    """
    Trang chủ
    ---
    tags:
      - Home
    responses:
      200:
        description: Trang chủ của API
    """
    return render_template('index.html')
