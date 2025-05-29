from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

DATA_FILE = 'data.json'

def load_data():
    """Load data from JSON file, create default if doesn't exist"""
    if not os.path.exists(DATA_FILE):
        # Create default data structure
        default_data = {
            "profile": {
                "name": "Kapil Sharma",
                "photo": "static/images/profile.png",
                "contact": {
                    "phone": "8595952141",
                    "email": "kapil.sharma.181410@gmail.com",
                    "linkedin": "https://linkedin.com/in/kapil-sharma-181410-yash",
                    "address": "H.N.231-A, West Azad Nagar, Delhi-51"
                }
            },
            "experience": [
                {
                    "company": "Paharpur 3P Pvt. Ltd.",
                    "duration": "Aug 2020 – Present",
                    "position": "Senior Executive - Sales & Marketing (CSC)",
                    "logo": "static/logos/paharpur.png",
                    "description": "Leading sales and marketing initiatives for CSC division"
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Commerce",
                    "institute": "University of Delhi",
                    "year": "1999–2002",
                    "icon": "static/icons/education.png"
                }
            ],
            "achievements": [
                "SAP/SAP Hana Training Program",
                "ISO Awareness Training",
                "FGS Audits Participation"
            ],
            "skills": [
                "Sales & Marketing",
                "Customer Service",
                "SAP/SAP Hana",
                "Business Development",
                "Team Leadership"
            ],
            "languages": ["English", "Hindi"]
        }
        save_data(default_data)
        return default_data
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

@app.route('/')
def index():
    """Main portfolio page"""
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/admin')
def admin():
    """Admin panel main page"""
    data = load_data()
    return render_template('admin.html', data=data, enumerate=enumerate)

@app.route('/admin/add_experience', methods=['POST'])
def add_experience():
    """Add new work experience"""
    data = load_data()
    
    new_experience = {
        'company': request.form.get('company', '').strip(),
        'position': request.form.get('position', '').strip(),
        'duration': request.form.get('duration', '').strip(),
        'logo': request.form.get('logo', 'static/logos/default.png').strip(),
        'description': request.form.get('description', '').strip()
    }
    
    if new_experience['company'] and new_experience['position']:
        data['experience'].append(new_experience)
        if save_data(data):
            flash('Experience added successfully!', 'success')
        else:
            flash('Error saving data', 'error')
    else:
        flash('Company and position are required', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/add_education', methods=['POST'])
def add_education():
    """Add new education entry"""
    data = load_data()
    
    new_education = {
        'degree': request.form.get('degree', '').strip(),
        'institute': request.form.get('institute', '').strip(),
        'year': request.form.get('year', '').strip(),
        'icon': request.form.get('icon', 'static/icons/education.png').strip()
    }
    
    if new_education['degree'] and new_education['institute']:
        data['education'].append(new_education)
        if save_data(data):
            flash('Education added successfully!', 'success')
        else:
            flash('Error saving data', 'error')
    else:
        flash('Degree and institute are required', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/add_achievement', methods=['POST'])
def add_achievement():
    """Add new achievement"""
    data = load_data()
    
    achievement = request.form.get('achievement', '').strip()
    
    if achievement:
        data['achievements'].append(achievement)
        if save_data(data):
            flash('Achievement added successfully!', 'success')
        else:
            flash('Error saving data', 'error')
    else:
        flash('Achievement text is required', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/add_skill', methods=['POST'])
def add_skill():
    """Add new skill"""
    data = load_data()
    
    skill = request.form.get('skill', '').strip()
    
    if skill:
        data['skills'].append(skill)
        if save_data(data):
            flash('Skill added successfully!', 'success')
        else:
            flash('Error saving data', 'error')
    else:
        flash('Skill name is required', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/delete/<section>/<int:index>')
def delete_item(section, index):
    """Delete item from specified section"""
    data = load_data()
    
    try:
        if section in data and isinstance(data[section], list) and 0 <= index < len(data[section]):
            deleted_item = data[section].pop(index)
            if save_data(data):
                flash(f'Item deleted successfully!', 'success')
            else:
                flash('Error saving data', 'error')
        else:
            flash('Item not found', 'error')
    except Exception as e:
        flash(f'Error deleting item: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/edit_profile', methods=['POST'])
def edit_profile():
    """Edit profile information"""
    data = load_data()
    
    data['profile']['name'] = request.form.get('name', '').strip()
    data['profile']['contact']['email'] = request.form.get('email', '').strip()
    data['profile']['contact']['phone'] = request.form.get('phone', '').strip()
    data['profile']['contact']['linkedin'] = request.form.get('linkedin', '').strip()
    data['profile']['contact']['address'] = request.form.get('address', '').strip()
    data['profile']['photo'] = request.form.get('photo', 'static/profile.jpg').strip()
    
    if save_data(data):
        flash('Profile updated successfully!', 'success')
    else:
        flash('Error saving profile', 'error')
    
    return redirect(url_for('admin'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/logos', exist_ok=True)
    os.makedirs('static/icons', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)