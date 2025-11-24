from flask import Blueprint, render_template, session, redirect

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/chatbot')
def chatbot_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('chatbot.html')
