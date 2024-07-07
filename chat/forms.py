from django import forms
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class AddForm(forms.Form):
    friend_username = forms.CharField()

    def clean_friend_username(self):
        entered_username = self.cleaned_data['friend_username']
        user = self.initial.get('user')

        try:
            self.friend = User.objects.get(username__iexact=entered_username) # __iexact => case insensitive match
        except User.DoesNotExist:
            raise forms.ValidationError('User with this username does not exist')
        
        if user == self.friend:
            raise forms.ValidationError('You cannot add yourself as a friend')
        
        if self.friend in user.friends_mutual:
            raise forms.ValidationError('You are already friends with this user')
        
        if self.friend in user.get_outgoing_requests():
            raise forms.ValidationError('You have already sent a friend request to this user')

        return entered_username
    
    def save(self, user):
        user.friends.add(self.friend)