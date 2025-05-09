from django import forms
from django.core.exceptions import ValidationError
from account.models import User
import datetime


class SignUpForm(forms.Form):
    username = forms.CharField(label="사용자명")
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    # 생년월일 입력 받기
    birth_date = forms.DateField(label="생년월일",
                                 widget=forms.SelectDateWidget(years=range(datetime.datetime.now().year - 100, datetime.datetime.now().year + 1)))

    profile_image = forms.ImageField(label="프로필 이미지", required=False)
    short_description = forms.CharField(label="간단 소개", required=False)

    def clean_username(self):
        username = self.cleaned_data['username']  # 양쪽에 빈칸을 지움
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'입력한 사용자명({username})은 이미 사용 중입니다.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            self.add_error("password2", "비밀번호와 비밀번호 확인란의 값이 다릅니다.")

    def save(self):
        birth_date = self.cleaned_data['birth_date']
        # 생년월일을 기준으로 나이 계산
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            age=age,  # 계산된 나이 저장
            birth_date=birth_date,  # 실제 생년월일 저장
            profile_image=self.cleaned_data.get('profile_image'),
            short_description=self.cleaned_data.get('short_description'),
        )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        label="사용자명",
        min_length=3,
        widget=forms.TextInput(attrs={"placeholder": "사용자명 (3자리 이상)"}),
    )
    password = forms.CharField(
        label="비밀번호",
        min_length=4,
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 (4자리 이상)"}),
    )
