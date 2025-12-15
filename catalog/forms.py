from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_available', 'is_published']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите наименование'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Добавьте изображение'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        self._check_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        self._check_forbidden_words(description)
        return description

    def _check_forbidden_words(self, text):
        if not text:
            return
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in text_lower:
                raise forms.ValidationError(
                    f"Использование слова '{word}' запрещено."
                )

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price