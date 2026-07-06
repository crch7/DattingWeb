import datetime
import dateutil.tz
import flask_login
from flask import Blueprint, app, render_template
from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from flask import abort

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from sqlalchemy import or_
from datetime import datetime
from sqlalchemy import Date

import os
from werkzeug.utils import secure_filename

import pathlib
from pathlib import Path
from flask import current_app


from . import model

bp = Blueprint("main", __name__)


"""@bp.route("/")
def enter():    
    return render_template("main/enter.html")


@bp.route("/index")
@flask_login.login_required
def index():    
    return render_template("main/index.html")"""

@bp.route("/")
def enter():    
    return render_template("main/index.html")    

@bp.route("/view_profile/<int:user_id>", methods=["GET"])
@login_required
def view_profile(user_id):
    profile = model.Profile.query.filter_by(user_id=user_id).first()

    # Check if the current user has liked this profile
    has_liked = current_user in profile.user.likers

    # Check if the current user has blocked this profile
    has_blocked = current_user in profile.user.blockers

    return render_template(
        'main/view_profile.html', 
        profile=profile, 
        has_liked=has_liked, 
        has_blocked=has_blocked
    )


@bp.route("/create_profile")
@flask_login.login_required
def create_profile():   
    return render_template("main/create_profile.html")

@bp.route("/create_profile", methods=["POST"])
@flask_login.login_required
def create_profile_post():

    # Retrieve form data
    name = request.form.get("name")
    gender = request.form.get("gender")
    bio = request.form.get("bio")
    year = request.form.get("year")
    study = request.form.get("study")
    city = request.form.get("city")

    music = request.form.getlist("music[]")  
    cuisine = request.form.getlist("cuisine[]")  
    personality_traits = request.form.getlist("personality_traits[]")  
    lifestyle = request.form.getlist("lifestyle[]") 

    music_str = ",".join(music)
    cuisine_str = ",".join(cuisine)
    personality_traits_str = ",".join(personality_traits)
    lifestyle_str = ",".join(lifestyle)

    
    allergies = request.form.getlist("allergies[]")  
    allergies_other = request.form.get("allergies_other")  
    if allergies_other:
        allergies.append(allergies_other)  

    
    hobbies = request.form.getlist("hobbies[]")
    if len(hobbies) > 5:
        flash("Please select up to 5 hobbies.", "warning")
        return redirect(url_for("main.create_profile"))


    uploaded_file = request.files['photo']
    if uploaded_file.filename != '':

        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

       
        photo = model.Photo(file_extension=file_extension)
        db.session.add(photo)
        db.session.commit()

        
        path = photo_filename(photo)
        uploaded_file.save(path)   

    
    allergies_str = ",".join(allergies)  
    hobbies_str = ",".join(hobbies)       

    profile = model.Profile(
        user_id=current_user.id,
        name=name,
        gender=gender,
        year = year,
        bio=bio,
        study=study,
        city=city,
        allergies=allergies_str,
        hobbies = hobbies_str,
        music=music_str,
        cuisine=cuisine_str,
        personality_traits=personality_traits_str,
        lifestyle=lifestyle_str,
        photo=photo,
                
    )
    db.session.add(profile)
    db.session.commit()

    return redirect(url_for("main.create_preferences"))

@bp.route("/edit_profile")
@flask_login.login_required
def edit_profile():   
    return render_template("main/edit_profile.html")

@bp.route("/edit_profile", methods=["POST"])
@flask_login.login_required
def edit_profile_post():

    
    gender = request.form.get("gender")
    bio = request.form.get("bio")
    study = request.form.get("study")
    music = request.form.getlist("music[]")  
    cuisine = request.form.getlist("cuisine[]")  
    personality_traits = request.form.getlist("personality_traits[]")  
    lifestyle = request.form.getlist("lifestyle[]") 

    music_str = ",".join(music)
    cuisine_str = ",".join(cuisine)
    personality_traits_str = ",".join(personality_traits)
    lifestyle_str = ",".join(lifestyle)

    # Handle allergies
    allergies = request.form.getlist("allergies[]")  # Get selected checkboxes
    allergies_other = request.form.get("allergies_other")  # Get other input
    if allergies_other:
        allergies.append(allergies_other)  # Add custom allergy if provided
    # Convert allergies to a comma-separated string
    allergies_str = ",".join(allergies) 


    hobbies = request.form.getlist("hobbies[]")
    if len(hobbies) > 5:
        flash("Please select up to 5 hobbies.", "warning")
        return redirect(url_for("main.create_profile"))
    hobbies_str = ",".join(hobbies)  

    uploaded_file = request.files['photo']
    
    if uploaded_file.filename != '':
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

        old_photo = flask_login.current_user.profile.photo
        if old_photo is not None:
            path = photo_filename(old_photo)
            path.unlink()

        old_photo = flask_login.current_user.profile.photo
        photo = model.Photo(file_extension=file_extension)
        db.session.add(photo)

        profile = current_user.profile
        profile.gender = gender
        profile.bio = bio
        profile.study = study 
        profile.allergies = allergies_str 
        profile.hobbies = hobbies_str
        profile.music = music_str
        profile.cuisine = cuisine_str
        profile.personality_traits= personality_traits_str 
        profile.lifestyle = lifestyle_str 
        profile.photo = photo
    
        db.session.commit()
        path = photo_filename(photo)
        uploaded_file.save(path) 

    return redirect(url_for("main.view_my_profile"))


@bp.route("/create_preferences")
@flask_login.login_required
def create_preferences():
    return render_template("main/create_preferences.html")

@bp.route("/create_preferences", methods=["GET", "POST"])
def create_preferences_post():
    if request.method == "POST":
        # Retrieve selected genders as a list
        interested_genders = request.form.getlist("interested_genders[]")  # Updated to handle multiple values
        min_age = request.form.get("min_age")
        max_age = request.form.get("max_age")
        relationship_type = request.form.get("relationship_type") 

        # Convert the list to a comma-separated string for storage
        interested_genders_str = ",".join(interested_genders)
        
        # Update or create profile
        matches = model.MatchingPreferences.query.filter_by(user_id=current_user.id).first()
        if matches:
            matches.interested_genders = interested_genders_str
            matches.min_age = min_age
            matches.max_age = max_age
            matches.relationship_type = relationship_type
        else:
            matches = model.MatchingPreferences(
                user_id=current_user.id,
                interested_genders=interested_genders_str,
                min_age=min_age,
                max_age=max_age,
                relationship_type=relationship_type,
            )
            db.session.add(matches)

        db.session.commit()
        return redirect(url_for("main.search_matches"))

    else:
        # Retrieve existing profile for editing
        matches = model.MatchingPreferences.query.filter_by(user_id=current_user.id).first()

        # Convert the comma-separated string back to a list for display
        if matches and matches.interested_genders:
            matches.interested_genders = matches.interested_genders.split(",")
        
        return render_template("main/view_profile.html", matches=matches)

@bp.route("/view_my_profile")
@flask_login.login_required
def view_my_profile():   
    profile = model.Profile.query.filter_by(user_id=current_user.id).first()
    photo = current_user.profile.photo 
    MatchingPreferences = current_user.matching_preferences
    liked_users = current_user.liking  
    blocked_users = current_user.blocking  
    if not profile:
        
        return render_template("main/view_my_profile.html", error="Profile not found")


    return render_template(
        "main/view_my_profile.html", liked_users=liked_users, blocked_users=blocked_users,
        profile={
            "name": profile.name,
            "gender": profile.gender,
            "year": profile.year,
            "bio": profile.bio,
            "photo": current_user.profile.photo,
        },
        MatchingPreferences={
            "interested_genders": MatchingPreferences.interested_genders,
            "min_age": MatchingPreferences.min_age,
            "max_age": MatchingPreferences.max_age,

        },
         user=flask_login.current_user
    )

@bp.route("/add_additional_photo", methods=["POST"])
@login_required
def add_additional_photo():
    uploaded_file = request.files['photo']
    
    if uploaded_file.filename != '':
        # Validate content type
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

        # Check if the user has less than 5 photos
        profile = current_user.profile
        if len(profile.additional_photos) >= 5:
            flash("You cannot upload more than 5 additional photos.", "error")
            return redirect(url_for("main.view_my_profile"))

        # Create a new AdditionalPhoto object
        additional_photo = model.AdditionalPhoto(
            profile_id=profile.id,
            file_extension=file_extension
        )
        db.session.add(additional_photo)
        db.session.commit()

        # Save the file to the correct directory
        path = os.path.join(current_app.static_folder, f"photos/addphoto-{additional_photo.id}.{file_extension}")
        uploaded_file.save(path)

        flash("Photo uploaded successfully!", "success")
    else:
        flash("No file selected.", "error")

    return redirect(url_for("main.view_my_profile"))  # Change this if you want a different redirect target


@bp.route("/delete_additional_photo/<int:photo_id>", methods=["POST"])
@login_required
def delete_additional_photo(photo_id):

    photo = model.AdditionalPhoto.query.filter_by(id=photo_id).first()
    # Check if the photo exists and if the user is authorized to delete it
    if photo is None or photo.profile_id != current_user.profile.id:
        abort(403)  

    # Prevent deletion of the profile picture
    if photo == current_user.profile.photo:
        abort(400, "Cannot delete the profile picture")

    # Delete only the record from the database (without deleting the file from the system)
    db.session.delete(photo)
    db.session.commit()

    return redirect(url_for("main.view_my_profile"))


@bp.route("/view_my_proposals")
@flask_login.login_required
def view_my_proposals():  
    return render_template("received_proposals.html")

@bp.route("/search_matches", methods=["GET"])
@login_required
def search_matches():

    current_profile = model.Profile.query.filter_by(user_id=current_user.id).first()
    
    if not current_profile:
        flash("You need to create a profile first!", "warning")
        return redirect(url_for("main.create_profile"))

    preferences = current_user.matching_preferences
    if not preferences:
        return render_template("main/search_matches.html", matches=[])

    # Gender preference
    preferred_genders = preferences.interested_genders.split(',')
    
    # Age range
    min_age, max_age = current_user.profile.year - preferences.min_age, current_user.profile.year + preferences.max_age  # Assuming stored as (min, max)

    # Relationship type
    preferred_relationship_type = preferences.relationship_type


    matches = (
        db.session.query(model.Profile)
        .options(joinedload(model.Profile.user))
        .filter(
            model.Profile.gender.in_(preferred_genders), 
            model.Profile.year.between(min_age, max_age),
            ~model.Profile.user.has(model.User.id == current_user.id),  # Exclude current user
            ~model.Profile.user.has(model.User.blockers.any(model.User.id == current_user.id)),  # Exclude users who have blocked you
            ~model.Profile.user.has(model.User.blocking.any(model.User.id == current_user.id))  # Exclude users you have blocked
        )
        .all()
    )
   
    return render_template("main/search_matches.html", matches=matches)

@bp.route("/recommended_matches", methods =["GET"] )
@login_required
def recommended_matches():
    current_profile = model.Profile.query.filter_by(user_id=current_user.id).first()
    
    if not current_profile:
        flash("You need to create a profile first!", "warning")
        return redirect(url_for("main.create_profile"))

    preferences = current_user.matching_preferences
    if not preferences:
        return render_template("main/search_matches.html", matches=[])

    # Gender preference
    preferred_genders = preferences.interested_genders.split(',')
    
    # Age range
    min_age, max_age = current_user.profile.year - preferences.min_age, current_user.profile.year + preferences.max_age  # Assuming stored as (min, max)

    # Relationship type
    preferred_relationship_type = preferences.relationship_type


    matches = (
        db.session.query(model.Profile)
        .filter(
            model.Profile.gender.in_(preferred_genders),
            model.Profile.year.between(min_age, max_age),
            or_(
                model.Profile.music.in_(current_profile.music.split(',')),
                model.Profile.cuisine.in_(current_profile.cuisine.split(',')),
                model.Profile.personality_traits.in_(current_profile.personality_traits.split(',')),
                model.Profile.lifestyle.in_(current_profile.lifestyle.split(','))
            ),
            model.Profile.user.has(
                model.User.matching_preferences.has(
                    model.MatchingPreferences.relationship_type == preferred_relationship_type  # Match relationship type
                )
            ),
            ~model.Profile.user.has(model.User.id == current_user.id),  # Exclude current user
            ~model.Profile.user.has(model.User.blockers.any(model.User.id == current_user.id)),  # Exclude users who have blocked you
            ~model.Profile.user.has(model.User.blocking.any(model.User.id == current_user.id))  # Exclude users you have blocked
        )
        .all())

    current_hobbies = set(current_profile.hobbies.split(','))
    matches = [match for match in matches if len(current_hobbies.intersection(set(match.hobbies.split(',')))) >= 2]

       
    return render_template("main/recommended_matches.html", matches=matches)



@bp.route("/like/<int:user_id>", methods=["POST"])
@login_required
def like_user(user_id):
    if user_id == current_user.id:
        flash("You cannot like yourself.", "error")
        return redirect(url_for("main.search_matches"))
    
    # Check if the relationship already exists
    liked_user = model.User.query.get_or_404(user_id)
    
    # Check if the current user has already liked this user
    if liked_user in current_user.liking:
        flash(f"You already liked {liked_user.profile.name}!", "info")
        return redirect(url_for("main.search_matches"))
    
    # Add to the liking relationship
    current_user.liking.append(liked_user)
    db.session.commit()
    flash(f"You liked {liked_user.profile.name}!", "success")
    return redirect(url_for("main.search_matches"))


@bp.route("/block/<int:user_id>", methods=["POST"])
@login_required
def block_user(user_id):
    if user_id == current_user.id:
        flash("You cannot block yourself.", "error")
        return redirect(url_for("main.search_matches"))
    
    # Check if the user to be blocked exists
    blocked_user = model.User.query.get_or_404(user_id)
    
    # Check if the current user has already blocked this user
    if blocked_user in current_user.blocking:
        flash(f"You have already blocked {blocked_user.profile.name}.", "info")
        return redirect(url_for("main.search_matches"))
    
    # Add to the blocking relationship
    current_user.blocking.append(blocked_user)
    db.session.commit()
    flash(f"You blocked {blocked_user.profile.name}.", "info")
    return redirect(url_for("main.search_matches"))


@bp.route("/unlike/<int:user_id>", methods=["POST"])
@login_required
def unlike_user(user_id):
    if user_id == current_user.id:
        flash("You cannot unlike yourself.", "error")
        return redirect(url_for("main.search_matches"))
    
    # Check if the user is in the liking list
    liked_user = model.User.query.get_or_404(user_id)
    
    # Check if the current user has liked this user
    if liked_user not in current_user.liking:
        flash(f"You haven't liked {liked_user.profile.name} yet.", "info")
        return redirect(url_for("main.search_matches"))
    
    # Remove from the liking relationship
    current_user.liking.remove(liked_user)
    db.session.commit()
    flash(f"You unliked {liked_user.profile.name}.", "info")
    return redirect(url_for("main.search_matches"))


@bp.route("/unblock/<int:user_id>", methods=["POST"])
@login_required
def unblock_user(user_id):
    if user_id == current_user.id:
        flash("You cannot unblock yourself.", "error")
        return redirect(url_for("main.search_matches"))
    
    # Check if the user is in the blocking list
    blocked_user = model.User.query.get_or_404(user_id)
    
    # Check if the current user has blocked this user
    if blocked_user not in current_user.blocking:
        flash(f"You haven't blocked {blocked_user.profile.name} yet.", "info")
        return redirect(url_for("main.search_matches"))
    
    # Remove from the blocking relationship
    current_user.blocking.remove(blocked_user)
    db.session.commit()
    flash(f"You unblocked {blocked_user.profile.name}.", "info")
    return redirect(url_for("main.search_matches"))


@bp.route('/toggle_like/<int:user_id>', methods=['POST'])
@login_required
def toggle_like(user_id):
    user_to_like = model.User.query.filter_by(id=user_id).first()
    if current_user in user_to_like.likers:
        # Unlike the user
        user_to_like.likers.remove(current_user)
        flash("You unliked this user.", "info")
    else:
        # Like the user
        user_to_like.likers.append(current_user)
        flash("You liked this user.", "success")

    db.session.commit()
    return redirect(url_for('main.view_profile', user_id=user_id))


@bp.route('/toggle_block/<int:user_id>', methods=['POST'])
@login_required
def toggle_block(user_id):
    user_to_block = model.User.query.filter_by(id=user_id).first()
    if current_user in user_to_block.blockers:
        # Unblock the user
        user_to_block.blockers.remove(current_user)
        flash("You unblocked this user.", "info")
    else:
        # Block the user
        user_to_block.blockers.append(current_user)
        flash("You blocked this user.", "danger")

    db.session.commit()
    return redirect(url_for('main.view_profile', user_id=user_id))



from datetime import datetime

@bp.route("/propose_date/<int:user_id>", methods=["GET", "POST"])
@login_required
def propose_date(user_id):
    recipient = model.User.query.get_or_404(user_id)
    today = datetime.now().strftime("%Y-%m-%d")  # For min date in the HTML form

    # POST request: handle form submission
    # Blocked check
    if current_user in recipient.blocking:
        flash("You cannot propose a date to this user because you are blocked.", "error")
        return redirect(url_for("main.view_profile", user_id=user_id))
    
    # For GET request, render the form
    return render_template("main/propose_date.html", recipient=recipient, user_id=user_id, today=today)



@bp.route("/send_proposal/<int:user_id>", methods=["GET", "POST"])
@login_required
def send_proposal(user_id):
    recipient = model.User.query.get_or_404(user_id)

    if request.method == "GET":
        # Render the propose date form
        today = datetime.today().date().isoformat()  # Pass today's date for validation in the form
        return render_template("propose_date.html", user_id=user_id, today=today)

    
    # Form data
    proposed_date = request.form.get("date")
    time = request.form.get("time")
    message = request.form.get("message")
    selected_table = request.form.get("selected_table")  # Get the selected table

    # Ensure the proposed date is today or in the future
    today = datetime.today().date()
    if proposed_date < today.isoformat():
        flash("You can only propose a date from today onwards.", "error")
        return redirect(url_for("main.propose_date", user_id=user_id))

    # Validate selected table
    if not selected_table:
        flash("You must select a table before proposing a date.", "error")
        return redirect(url_for("main.propose_date", user_id=user_id))

    # Ensure selected_table is a valid integer
    try:
        selected_table = int(selected_table)
    except ValueError:
        flash("Invalid table selection.", "error")
        return redirect(url_for("main.propose_date", user_id=user_id))

    # Check if the table is available
    reserved_tables = db.session.query(model.RestaurantAvailability).filter_by(
        date=proposed_date, table_id=selected_table
    ).first()

    if reserved_tables:
        flash(f"Table {selected_table} is already reserved on {proposed_date}", "error")
        return redirect(url_for("main.propose_date", user_id=user_id))
    
    # Create a new date proposal
    new_proposal = model.DateProposal(
        proposer_id=current_user.id,
        recipient_id=recipient.id,
        date=proposed_date,
        time=time,
        message=message,
        response_message="",
        status=model.ProposalStatus.proposed,
        table_id=selected_table
    )

    # Add the proposal to the restaurant availability
    new_table = model.RestaurantAvailability(
        table_id=selected_table,
        date=proposed_date
    )

    db.session.add(new_proposal)
    db.session.add(new_table)
    db.session.commit()
    flash(f"Date proposal sent to {recipient.profile.name}!", "success")

    return redirect(url_for("main.view_profile", user_id=user_id))




@bp.route("/proposals/respond/<int:proposal_id>", methods=["GET", "POST"])
@login_required
def respond_date(proposal_id):
    proposal = model.DateProposal.query.get_or_404(proposal_id)

    # Ensure the recipient is the current user
    if proposal.recipient_id != current_user.id:
        flash("You cannot respond to this proposal.", "error")
        return redirect(url_for("main.view_proposals"))

    if request.method == "POST":
        # Handle the response submission
        status = request.form.get("status")
        response_message = request.form.get("response_message")

        # Validate status input
        if status not in [e.name for e in model.ProposalStatus]:
            flash("Invalid response status.", "error")
            return redirect(request.url)

        # Update the proposal
        proposal.status = model.ProposalStatus[status]
        proposal.response_message = response_message
        proposal.response_timestamp = datetime.utcnow()

        # If the proposal is rejected or ignored, remove the table reservation
        if status in ["rejected", "ignored"]:
            # Check if the table is available
            reserved_table = db.session.query(model.RestaurantAvailability).filter_by(
                date=proposal.date, table_id=proposal.table_id
            ).first()

            if reserved_table:
                db.session.delete(reserved_table)

        db.session.commit()
        flash("Response submitted successfully.", "success")
        return redirect(url_for("main.view_received_proposals"))

    # Render the response form for GET requests
    return render_template("main/respond_to_proposals.html", proposal=proposal)


@bp.route("/proposals/sent", methods=["GET"])
@login_required
def view_sent_proposals():
    # Fetch all proposals sent by the current user
    sent_proposals = current_user.sent_proposals
    return render_template("main/sent_proposals.html", proposal=sent_proposals)


@bp.route("/proposals/received", methods=["GET"])
@login_required
def view_received_proposals():
    # Get the list of users blocked by the current user
    blocked_users = {user.id for user in current_user.blocking}

    # Filter proposals to exclude those sent by blocked users
    received_proposals = [
        proposal for proposal in current_user.received_proposals
        if proposal.proposer.id not in blocked_users
    ]

    return render_template("main/received_proposals.html", proposals=received_proposals)



# Define a function to get the photo file path
def photo_filename(photo):
    return Path(current_app.root_path) / 'static' / 'photos' / f"photo-{photo.id}.{photo.file_extension}"

@bp.route("/principal")
@flask_login.login_required
def principal():
    return render_template("main/principal.html")


# Route for Privacy Policy
@bp.route("/privacy-policy")
def privacy_policy():
    return render_template("main/privacy_policy.html")

# Route for Terms of Service
@bp.route("/terms_of_service")
def terms_of_service():
    return render_template("main/terms_of_service.html")

# Route for Contact Us
@bp.route("/contact")
def contact():
    return render_template("main/contact.html")

# Route to handle the contact form submission
@bp.route("/send-message", methods=["POST"])
def send_message():
    # Get the form data
    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    # Check if the submitted email is associated with an existing user
    query = db.select(model.User).where(model.User.email == email)
    user = db.session.execute(query).scalar_one_or_none()

    if user:
        # If a user with the email exists, show an error message and prevent submission
        flash("This email is already associated with an existing account. Please use a different email.", "error")
        return redirect(url_for("main.contact"))

    # Create a new ContactSubmission instance
    new_submission = model.ContactSubmission(
        name=name,
        email=email,
        subject=subject,
        message=message,
    )

    # Add the new submission to the database
    db.session.add(new_submission)
    db.session.commit()

    # Conditional redirect based on user authentication
    if current_user.is_authenticated:
        # Redirect to the principal page if the user is logged in
        return redirect(url_for("main.principal"))
    else:
        # Redirect to the enter page if the user is not logged in
        return redirect(url_for("main.enter"))


