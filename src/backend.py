from flask import Flask, jsonify, request
from src.tracker import Tracker

app = Flask(__name__)
tracker = Tracker()

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """
    Get progress data for all dates.
    """
    return jsonify(tracker.tracker_data)

@app.route('/api/progress/<date>', methods=['GET'])
def get_progress_by_date(date):
    """
    Get progress data for a specific date.
    """
    return jsonify(tracker.tracker_data.get(date, []))

@app.route('/api/progress/<date>/<int:slot_index>', methods=['POST'])
def update_progress(date, slot_index):
    """
    Update the progress for a specific date and time slot.
    """
    tracker.tracker_data[date][slot_index] = not tracker.tracker_data[date][slot_index]
    return jsonify({"success": True, "updated": tracker.tracker_data[date]})

if __name__ == '__main__':
    app.run(debug=True)
