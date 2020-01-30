from django.urls import path, re_path
from django.conf.urls import url

from . import views


urlpatterns = [
    #path('upvote/', views.DoUpvote, name='upvote'),
    path('upvote', views.DoUpvote, name='upvote'),
    path('checkslug', views.CheckSlugWithAjax, name='checkslug'),
    path('addCategory', views.AddCategoryWithAjax, name='checkslug'),
    path('category/<category>', views.ViewCategoryPage, name='view_category'),
    path('categories/', views.ViewAllCategories, name='view_all_categories'),
    
    path('<question>', views.ViewQuestion),
    path('<question>/', views.ViewQuestion, name='view_question'),
    path('question/<action>/', views.QuestionsActions, name='question_action'),
    path('question/<action>/<param>/',views.QuestionsActions, name='question_action_param'),
    #url(r'^upvote/<type>/<id>/$',views.DoUpvote, name='upvote_type_id'),
    # path('upvote/<type>/<id>', views.DoUpvote),


]