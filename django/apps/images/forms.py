# Not in use

from django.core.files.images import get_image_dimensions


# Can use a "fake" form to validate uploads from Dojo.editor
class myForm (forms.ModelForm):
   class Meta:
       model = Image
   def clean_file (self):
       image = self.cleaned_data.get("image")
       if not image:
           raise forms.ValidationError("No image!")
       else:
           w, h = get_image_dimensions (image)
           if w != 100:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 100px" % w)
           if h != 200:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be 200px" % h)
       return image
