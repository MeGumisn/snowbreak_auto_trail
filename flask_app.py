import ctypes
import logging
import threading

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # 新增导入

from TrailTaskApp import TrailTaskApp
from utils.WindowUtil import WindowUtil

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)  # 全局启用 CORS（开发环境推荐）

# 或精细化配置（生产环境推荐）
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost"],
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE"]
    }
})


@app.errorhandler(400)
def handle_bad_request(e):
    app.logger.error(f'Bad request: {request.data}')
    return jsonify(error=str(e)), 400


@app.route('/api/taskList', methods=['GET'])
def get_task_list():
    """示例 GET 接口"""
    task_list = [{
        "id": 0,
        "name": "default",
    }]
    return jsonify(task_list)


@app.route('/api/selectTask', methods=['POST'])
def init_task():
    data = request.get_json()
    name = data.get('name')
    hwndMap = WindowUtil.enumerate_visible_windows()
    logging.info('init task' + name)
    taskApp['task'] = TrailTaskApp(hwndMap[name], dxgi)
    return jsonify({'message': f'init task {name}'})


@app.route('/api/changeTaskStatus', methods=['POST'])
def change_task_status():
    """示例 POST 接口"""
    data = request.get_json()
    action = data.get('action')
    if action == 'stop':
        WindowUtil.STOP = True
    elif action == 'start':
        task = taskApp['task']
        if task is not None:
            WindowUtil.STOP = False
            task.run()
    return jsonify({'message': f'change task status to {action}'})


@app.route('/api/windows', methods=['GET'])
def get_windows():
    hwndMap = WindowUtil.enumerate_visible_windows()
    return jsonify([
        {"id": hwnd, "name": title}
        for title, hwnd in hwndMap.items()  # 使用 .items() 遍历键值对
    ])


@app.route('/api/capture', methods=['POST'])
def capture_game_window():
    logging.info(f'capture game window: {taskApp}')
    task = taskApp['task']
    base64Img = task.capture.grab_window()
    return jsonify({'img': base64Img})


if __name__ == '__main__':
    ctypes.windll.user32.SetProcessDPIAware()
    global dxgi
    dxgi = ctypes.windll.LoadLibrary("./dxgi4py.dll")
    global taskApp
    taskApp = dict()
    app.run(threaded=False)
