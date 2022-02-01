from django.shortcuts import render
from rest_framework import viewsets

from reviews.models import Review

from .serializers import (CommentSerializer, ReviewSerializer)


