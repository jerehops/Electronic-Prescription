from flask import request, flash, redirect, url_for, jsonify
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView
from flask_login import current_user


from app import db, admin
from app.models import User, Patient, Doctor, Pharmacist, Admin
from app.auth.forms import AdminCreateUserForm, AdminEditUserForm, EditAdminForm

class MyAdminView(ModelView):

    @expose('/')
    def index(self):
        return self.render('admin/user.html')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.get_role() == 'admin'
        return False

class AdminUserView(MyAdminView):

    @expose('/')
    def index(self):
        """
        # Admin User Pannel to manage users
        """
        users = User.get_all_users()
        # return "users"
        # return {'users': [user() for user in users]}
        return self.render('admin/user.html', users=users)


    @expose('/add', methods=['GET', 'POST'])
    def create_user(self):
        form = AdminCreateUserForm()

        if form.validate_on_submit():
            """
            # Create New User
            """
            try:
                user = User.get_user_by_username (form.username.data)
                if user:
                    error = 'User already exists with username, {}'.format(form.username.data)
                    return self.render('admin/user_regis_form.html', form=form, error=error)

                if form.user_role.data == 'Doctor':
                    if self.email_taken('doctor', form.email.data):
                        error = 'User already exists with email, {}'.format(form.email.data)
                        return self.render('admin/user_regis_form.html', form=form, error=error)
                    # Create new doctor
                    new_doctor = Doctor(
                        username = form.username.data,
                        role = 'doctor',
                        fName=form.fName.data,
                        lName=form.lName.data,
                        mobile=form.mobile.data,
                        email = form.email.data,
                        dob=form.dob.data,
                        gender=form.gender.data
                    )
                    new_doctor.set_password(form.password.data)
                    new_doctor.save()

                    flash ('New User Created. [info] {}'.format(new_doctor))
                    return redirect(url_for('user.index'))

                elif form.user_role.data == 'Pharmacist':
                    if self.email_taken('pharmacist', form.email.data):
                        error = 'User already exists with email, {}'.format(form.email.data)
                        return self.render('admin/user_regis_form.html', form=form, error=error)
                    # Create new pharmacist
                    new_pharmacist = Pharmacist(
                        username = form.username.data,
                        role = 'pharmacist',
                        fName=form.fName.data,
                        lName=form.lName.data,
                        mobile=form.mobile.data,
                        email = form.email.data,
                        dob=form.dob.data,
                        gender=form.gender.data,
                    )
                    new_pharmacist.set_password(form.password.data)
                    new_pharmacist.save()

                    flash ('New User Created. [info] {}'.format(new_pharmacist))
                    return redirect(url_for('user.index'))

                elif form.user_role.data == 'Admin':
                    if self.email_taken('admin', form.email.data):
                        error = 'User already exists with email, {}'.format(form.email.data)
                        return self.render('admin/user_regis_form.html', form=form, error=error)
                    # create new admin
                    new_admin = Admin(
                        username = form.username.data,
                        role = 'admin',
                        fName=form.fName.data,
                        lName=form.lName.data,
                        mobile=form.mobile.data,
                        email = form.email.data,
                        dob=form.dob.data,
                        gender=form.gender.data
                    )
                    new_admin.set_password(form.password.data)
                    new_admin.save()

                    flash ('New User Created. [info] {}'.format(new_admin))
                    return redirect(url_for('user.index'))

            except ValueError as ve:
                print(str(ve))
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error: [ValueError] {}'.format(str(ve)))
            except KeyError as ke:
                print(str(ke))
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error: [KeyError] {}'.format(str(ke)))
            except AttributeError as ae:
                print(str(ae))
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error: [AttrubuteError] {}'.format(str(ae)))
            except Exception as e:
                print(str(e))
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error. Please try again')

        return self.render('admin/user_regis_form.html', form=form)


    @expose('/<id>', methods=['DELETE'])
    def delete_user(self, id):
        if request.method == 'DELETE':
            try:
                user = User.get_user_by_id(id)
                if user is None:
                    return jsonify("User Not Found!"), 200
                if user.activated:
                    return jsonify("Cannot delete active user"), 200

                if user.role == 'patient':
                    print('deleting patient')
                    Patient.delete_patient(id)
                elif user.role == 'admin':
                    print('deleting admin')
                    Admin.delete_admin(id)
                elif user.role == 'doctor':
                    print('deleting doctor')
                    Doctor.delete_doctor(id)
                elif user.role == 'pharmacist':
                    print('deleting pharmacist')
                    Pharmacist.delete_pharmacist(id)

                flash('User Deleted. ID: {}, Username: {}'.format(id, user.username))
                return '', 204

            except ValueError as ke:
                print(ke)
                flash ('Internal Server Error [ValueErorr], {}'.format(str(ve)))
                return redirect(url_for('user.index'))
            except KeyError as ke:
                print(ke)
                flash ('Internal Server Error [KeyErorr], {}'.format(str(ke)))
                return redirect(url_for('user.index'))
            except AttributeError as ae:
                print(ae)
                flash ('Internal Server Error [AttributeErorr], {}'.format(str(ae)))
                return redirect(url_for('user.index'))
            except Exception as e:
                print(e)
                flash ('Internal Server Error [Error], {}'.format(str(e)))
                return redirect(url_for('user.index'))


    @expose('/edit/<id>', methods=['GET', 'POST'])
    def edit_user(self, id):
        user = User.get_user_by_id(id)
        if user is None:
            return "User Not Found", 404

        role = user.get_role()
        # get user type instance based on user role --> doctor, patient, pharmacist
        user_with_role = self.get_user_type_instance(role, id)

        if role == 'admin':
            flash ("You can't update other admin profiles. If you want to edit your profile, go to edit profile page.")
            return redirect(url_for('user.index'))
        else:
            form = AdminEditUserForm(activated='Active' if user.activated else 'Inactive')
            try:
                if form.validate_on_submit():

                    if not self.valid_username_on_edit(user, form.username.data):
                        error = "Username, {}, is already taken by other user.".format(form.username.data)
                        return self.render('admin/edit_user.html', form=form, user=user_with_role, error=error)

                    if not self.valid_email_on_edit(user_with_role, form.email.data):
                        error = "Email Address, {}, is already registered with other user.".format(form.email.data)
                        return self.render('admin/edit_user.html', form=form, user=user_with_role, error=error)

                    data = self.to_user_dict(form.username.data, form.email.data, form.fName.data, form.lName.data, form.mobile.data, form.activated.data)

                    updated_user = self.update_user_by_role(role, id, data)
                    flash ('Successful User Update: User {} {}'.format(updated_user.fName, updated_user.lName))
                    return redirect(url_for('user.index'))

                return self.render('admin/edit_user.html', form=form, user=user_with_role)

            except KeyError as ke:
                print('Exception occured during edit user. Key Error: {}'.format(str(ke)))
                return self.render('admin/edit_user.html', form=form, user=user_with_role, error='Internal Server Error: {}'.format(str(ke)))
            except AttributeError as ae:
                print('Exception occured during edit user. Attribute Error: {}'.format(str(ae)))
                return self.render('admin/edit_user.html', form=form, user=user_with_role, error='Internal Server Error: {}'.format(str(ae)))
            except Exception as e:
                print('Exception occured during edit user. Error: {}'.format(str(e)))
                return self.render('admin/edit_user.html', form=form, user=user_with_role, error='Internal Server Error: {}'.format(str(e)))


    @expose('view/<id>')
    def view_user(self, id):
        """
        # View user information
        """
        try:
            user = User.get_user_by_id(id)
            if user is None:
                return "User Not Found", 404

            role = user.get_role()
            # if role == 'admin':
            #     form = EditAdminForm()
            # else:
            # I am using the edit form but in this page, all the fields are readonly
            form = AdminEditUserForm()
            # get user type instance based on user role --> doctor, patient, pharmacist
            user_with_role = self.get_user_type_instance(role, id)
            status = 'Active' if user.activated else 'Inactive'
            return self.render('admin/view_user.html', form=form, user=user_with_role, status=status)

        except Exception as e:
            print('Exception occured during edit user. Error: {}'.format(str(e)))
            flash ('Internal Server Error [Error], {}'.format(str(e)))
            return redirect(url_for('user.index'))


    @expose('search')
    def search_user(self):
        """
        # Search User by Username
        """
        try:
            q = request.args.get('q')
            results = User.search_user_by_username(q)
            return jsonify([r() for r in results]), 200
        except Exception as e:
            return jsonify({'message' : str(e)}), 500


    def to_user_dict (self, username, email, fName, lName, mobile, activated):
        """
        # Converts form data to python dictionary
        """
        return {
            'username'   : username,
            'email'     : email,
            'fName'     : fName,
            'lName'     : lName,
            'mobile'    : mobile,
            'activated' : activated
        }


    def get_user_type_instance (self, role, id):
        """
        # Get role instance of user
        """
        if role == 'admin':
            return Admin.get_admin_by_acc_id(id)
        elif role == 'doctor':
            return Doctor.get_doctor_by_acc_id(id)
        elif role == 'patient':
            return Patient.get_patient_by_acc_id(id)
        elif role == 'pharmacist':
            return Pharmacist.get_pharmacist_by_acc_id(id)
        raise Exception('Unknown User Role')


    def update_user_by_role (self, role, id, data):
        """
        # Update user based on the user role
        """
        if role == 'admin':
            return Admin.update_admin_profile(id, data)
        elif role == 'doctor':
            return Doctor.update_doctor_profile(id, data)
        elif role == 'patient':
            return Patient.update_patient_profile(id, data)
        elif role == 'pharmacist':
            return Pharmacist.update_pharmacist_profile(id, data)
        raise Exception('Unkown User Role')


    def valid_username_on_edit (self, editingUser: object, new_username: str):
        """
        # Check if the new username has been taken by other users
        """
        if editingUser.username != new_username:
            user = User.get_user_by_username(new_username)
            return user is None

        return True


    def valid_email_on_edit (self, editingUser: object, new_email: str):
        """
        # Check if the new email address is taken by other users
        """
        if editingUser.email != new_email:
            return self.email_taken(editingUser.role, new_email) == False
        return True


    def email_taken (self, role: str, email: str) -> bool:
        """
        # Check if the user with same email is already registered
        """
        if Admin.get_user_by_email(email) is not None:
            return True
        elif Doctor.get_user_by_email(email) is not None:
            return True
        elif Patient.get_user_by_email(email) is not None:
            return True
        elif Pharmacist.get_user_by_email(email) is not None:
            return True
        else:
            return False


# admin.add_view(AdminIndexView(name="E Prescription", endpoint="index"))
admin.add_view(AdminUserView(User, db.session, endpoint='user'))
