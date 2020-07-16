from django.db import models
import bcrypt


class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class UserManager(models.Manager):
  def validate(self, postData):
    errors = {}
    fn = postData['first_name']
    ln = postData['last_name']
    em = postData['email']
    if len(fn) < 2:
      errors['first_name'] = 'First name must be 2 or more characters'
    elif len(fn) > 45:
      errors['first_name'] = 'First name must be 45 or less characters'
    if len(ln) < 2:
      errors['last_name'] = 'Last name must be 2 or more characters'
    elif len(ln) > 45:
      errors['last_name'] = 'Last name must be 45 or less characters'
    if len(User.objects.filter(email=em)) > 0:
      errors['last_name'] = 'User with email already exists please login'
    if len(postData['pw']) < 8:
      errors['pw'] = 'Password must be 8 or more characters'
    elif len(postData['pw']) >255:
      errors['pw'] = 'Password must be 255 or less characters'
    if postData['pw'] != postData['pw_confirm']:
      errors['pw'] = 'Passwords must match'
    return errors

  def gen_token(self, user_id):
    user = self.get(id=user_id)
    string = user.last_name + user.email + str(user.created_at)
    return bcrypt.hashpw(string.encode(), bcrypt.gensalt()).decode()

  def is_user_authenticated(self, user_id, token):
    try:
      user = self.get(id=user_id)
    except User.DoesNotExist:
      return False
    string = user.last_name + user.email + str(user.created_at)
    return bcrypt.checkpw(
      string.encode(),
      self.gen_token(user_id).encode()
    )


class User(BaseModel):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  pw_hash = models.CharField(max_length=255)
  objects = UserManager()

  def __str__(self):
    return f'User {self.first_name} {self.last_name}'


class Message(BaseModel):
  owner = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='messages')
  text = models.TextField()

  def __str__(self):
    return f'Message {self.id}'


class Comment(BaseModel):
  on_message = models.ForeignKey(
    Message, on_delete=models.CASCADE, related_name='comments')
  owner = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='comments')
  text = models.TextField()

  def __str__(self):
    return f'Comment {self.id} on {self.message_id}'
