from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, CommunityPost, Comment, PostLike, Notification, Trip
import secrets
import os

community_bp = Blueprint('community', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})

@community_bp.route('/community')
@login_required
def community():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 10)
    
    posts_query = CommunityPost.query.order_by(CommunityPost.created_at.desc())
    posts_pagination = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = posts_pagination.items if posts_pagination else []
    
    return render_template('community.html', posts=posts, pagination=posts_pagination)

@community_bp.route('/create-post', methods=['POST'])
@login_required
def create_post():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    trip_id = request.form.get('trip_id')
    
    if not title or not content:
        flash('Title and content are required.', 'error')
        return redirect(url_for('community.community'))
    
    try:
        post = CommunityPost(
            user_id=current_user.id,
            title=title,
            post_content=content,
            trip_id=int(trip_id) if trip_id else None
        )
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{secrets.token_hex(8)}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                post.image_path = filename
            elif file and file.filename:
                flash('Invalid file type. Only images are allowed.', 'error')
                return redirect(url_for('community.community'))
        
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error creating post. Please try again.', 'error')
    
    return redirect(url_for('community.community'))

@community_bp.route('/like-post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    try:
        post = CommunityPost.query.get_or_404(post_id)
        existing = PostLike.query.filter_by(post_id=post_id, user_id=current_user.id).first()
        
        if existing:
            db.session.delete(existing)
            post.likes_count -= 1
            liked = False
        else:
            like = PostLike(post_id=post_id, user_id=current_user.id)
            db.session.add(like)
            post.likes_count += 1
            liked = True
            
            if post.user_id != current_user.id:
                notif = Notification(
                    user_id=post.user_id,
                    notification_text=f"{current_user.first_name} liked your post",
                    notification_type='like',
                    link='/community'
                )
                db.session.add(notif)
        
        db.session.commit()
        return jsonify({'success': True, 'liked': liked, 'likes_count': post.likes_count})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to like post'}), 500

@community_bp.route('/add-comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    comment_text = request.form.get('comment', '').strip()
    
    if not comment_text:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('community.community'))
    
    try:
        comment = Comment(
            post_id=post_id,
            user_id=current_user.id,
            comment_text=comment_text
        )
        db.session.add(comment)
        
        if post.user_id != current_user.id:
            notif = Notification(
                user_id=post.user_id,
                notification_text=f"{current_user.first_name} commented on your post",
                notification_type='comment',
                link='/community'
            )
            db.session.add(notif)
        
        db.session.commit()
        flash('Comment added!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding comment. Please try again.', 'error')
    
    return redirect(url_for('community.community'))

@community_bp.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifs)

@community_bp.route('/mark-notification-read/<int:notif_id>', methods=['POST'])
@login_required
def mark_notification_read(notif_id):
    try:
        notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
        notif.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to mark notification as read'}), 500

@community_bp.route('/delete-notification/<int:notif_id>', methods=['POST'])
@login_required
def delete_notification(notif_id):
    try:
        notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
        db.session.delete(notif)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to delete notification'}), 500
