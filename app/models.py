from django.db import models


class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class User(BaseModel):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  pw_hash = models.CharField(max_length=255)

  def __str__(self):
    return f'User {self.first_name} {self.last_name}'


class Message(BaseModel):
  user_id = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='messages')
  text = models.TextField()

  def __str__(self):
    return f'Message {self.id}'


class Comment(BaseModel):
  message_id = models.ForeignKey(
    Message, on_delete=models.CASCADE, related_name='comments')
  user_id = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='comments')
  text = models.TextField()

  def __str__(self):
    return f'Comment {self.id} on {self.message_id}'
