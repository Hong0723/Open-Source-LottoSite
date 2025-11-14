from django import forms


class ManualBuyForm(forms.Form):
    n1 = forms.IntegerField(min_value=1, max_value=45, label="번호 1")
    n2 = forms.IntegerField(min_value=1, max_value=45, label="번호 2")
    n3 = forms.IntegerField(min_value=1, max_value=45, label="번호 3")
    n4 = forms.IntegerField(min_value=1, max_value=45, label="번호 4")
    n5 = forms.IntegerField(min_value=1, max_value=45, label="번호 5")
    n6 = forms.IntegerField(min_value=1, max_value=45, label="번호 6")

    def clean(self):
        cleaned = super().clean()
        nums = [cleaned.get(f"n{i}") for i in range(1, 7)]
        if None in nums:
            return cleaned
        if len(set(nums)) != 6:
            raise forms.ValidationError("번호는 중복 없이 6개를 선택해야 합니다.")
        return cleaned


class AutoBuyForm(forms.Form):
    count = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        label="구매할 티켓 수",
        help_text="최대 10장까지 자동 생성",
    )
