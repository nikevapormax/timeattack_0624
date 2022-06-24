from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from post.serializers import JobPostSerializer
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company
)
from django.db.models.query_utils import Q


class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills)

        return Response(status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        job_type = int( request.data.get("job_type", None) )
        company_name = request.data.get("company_name", None)
        request.data["job_type"] = job_type

        serialized_post = JobPostSerializer(data=request.data)
        
        if serialized_post.is_valid():
            # if not request.data["company_name"]:
            #     new_company = Company.objects.create(company_name=request.data["company_name"], business_area="none")
            #     new_company.save()
            #     JobPost.company.add(new_company)
            return Response(serialized_post.data, status=status.HTTP_200_OK)
        
        return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)

