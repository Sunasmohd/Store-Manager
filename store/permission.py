from rest_framework.permissions import BasePermission

class SuperUserPerm(BasePermission):
  def has_permission(self, request, view):
    return bool(request.user and request.user.is_superuser)
  
class HistoryPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.has_perm('store.view_history')