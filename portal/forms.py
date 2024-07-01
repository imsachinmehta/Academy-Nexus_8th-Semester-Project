from cloudinary.models import CloudinaryField
import re
from django import forms
from .models import Post, User, Product, Image, File

# User = get_user_model()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput(render_value=False)
        self.fields["confirm_password"].widget = forms.PasswordInput(render_value=False)

    first_name = forms.CharField(max_length=30, label="Firstname")
    last_name = forms.CharField(max_length=30, label="Lastname")
    username = forms.CharField(max_length=30, label="Username", required=True)
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=30, label="Password")
    confirm_password = forms.CharField(max_length=30, label="Confirm Password")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    def _has_special_characters(self, string):
        pattern = r"[^\w\s]"  # Matches any character that is not a word character or whitespace
        return bool(re.search(pattern, string))

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        print("cleaning first name")

        if first_name[0].isdigit():
            raise forms.ValidationError("First name cannot begin with a number")

        if len(first_name) > 30:
            raise forms.ValidationError("First name cannot be more than 30 characters!")

        return first_name

    def clean_last_name(self):
        print("cleaning last name")
        last_name = self.cleaned_data["last_name"]
        if last_name[0].isdigit():
            raise forms.ValidationError("Last name cannot begin with a number")
        if len(last_name) > 30:
            raise forms.ValidationError("Last name cannot be more than 30 characters!")

        return last_name

    def clean_username(self):
        username = self.cleaned_data["username"]
        print("cleaning username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken!")

        if len(username) > 30:
            raise forms.ValidationError("Username cannot be more than 30 characters!")

        return username

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        confirmPassword = cleaned_data.get("confirm_password")
        print(f"{password} - {confirmPassword}")

        if password != confirmPassword:
            raise forms.ValidationError("Password doesnot match!")

        elif len(password) < 8:
            raise forms.ValidationError("Password must be atleast 8 characters long!")

        elif not any(char.isupper() for char in password):
            raise forms.ValidationError(
                "Password must contain atleast one UPPERCASE letter!"
            )

        elif not any(char.islower() for char in password):
            raise forms.ValidationError(
                "Password must contain atleast one lowercase letter!"
            )

        elif not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain atleast 1 number!")

        elif not self._has_special_characters(password):
            raise forms.ValidationError(
                "Password must contain atleast one special character!"
            )

        elif (
            "first_name" in cleaned_data
            and cleaned_data["first_name"] in cleaned_data["password"]
        ):
            raise forms.ValidationError("Password cannot contain first name")

        elif (
            "last_name" in cleaned_data
            and cleaned_data["last_name"] in self.cleaned_data["password"]
        ):
            raise forms.ValidationError("Password cannot contain last name")

        if len(password) > 30:
            raise forms.ValidationError("Password cannot be more than 30 characters!")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]
        print("cleaning email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")

        if email[0].isdigit():
            raise forms.ValidationError("Email cannot begin with number!")

        return self.cleaned_data["email"]

    def save(self):
        user = User.objects.create_user(
            email=self.cleaned_data["email"],
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_password(self.cleaned_data["password"])

        user.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username", required=True)
    password = forms.CharField(max_length=30, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class PostForm(forms.ModelForm):
    post_files = MultipleFileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        body = cleaned_data.get("body")
        files = cleaned_data.get("post_files")

        if len(title) > 150:
            raise forms.ValidationError("Title cannot be more than 150 characters!")
        if len(body) > 500:
            raise forms.ValidationError("Body cannot be more than 500 characters!")
        imgs = []
        fls = []
        for file in files:
            filetype = file.name.split(".")[-1]
            if filetype in ["jpg", "png", "jpeg"]:
                imgs.append(file)
            elif filetype in ["doc", "docx", "pdf"]:
                fls.append(file)
            else:
                raise forms.ValidationError("Invalid file type!")
        cleaned_data["imgs"] = imgs
        cleaned_data["fls"] = fls
        return cleaned_data

    def save(self, usr):
        print(usr)
        cleaned_data = self.clean()
        imgs = cleaned_data.get("imgs")
        fls = cleaned_data.get("fls")
        post = Post.objects.create(
            title=cleaned_data["title"], body=cleaned_data["body"], author=usr
        )
        post.save()
        if imgs:
            for image in imgs:
                Image.objects.create(post=post, image=image)
        if fls:
            for file in fls:
                File.objects.create(post=post, file=file)
        return post

    class Meta:
        model = Post
        fields = ["title", "body"]


class ProductForm(forms.ModelForm):
    product_images = MultipleFileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        name = cleaned_data.get("name")
        body = cleaned_data.get("description")
        images = cleaned_data.get("product_images")
        phoneNumber = cleaned_data.get("phone_number")
        # try:
        #     int(phoneNumber)
        # except:
        #     raise forms.ValidationError("Phone number must be a number!")

        if len(name) > 150:
            raise forms.ValidationError("Title cannot be more than 150 characters!")

        if len(body) > 500:
            raise forms.ValidationError("Body cannot be more than 500 characters!")

        if not images:
            raise forms.ValidationError("Please upload atleast one image!")
        else:
            for image in images:
                filetype = image.name.split(".")[-1]
                print(filetype)
                if not filetype in ["jpg", "png", "jpeg"]:
                    raise forms.ValidationError("Invalid file type!")

        return cleaned_data

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "phone_number",
            "condition",
            "product_images",
        ]

    def save(self, usr):

        product = Product.objects.create(
            name=self.cleaned_data["name"],
            description=self.cleaned_data["description"],
            price=self.cleaned_data["price"],
            phone_number=self.cleaned_data["phone_number"],
            condition=self.cleaned_data["condition"],
            seller=usr,
        )
        product.save()

        for image in self.cleaned_data["product_images"]:
            Image.objects.create(product=product, image=image)

        return product
