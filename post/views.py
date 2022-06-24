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
        
        query = Q()
        for skill in skills:
            query.add(Q(skill_set__name=skill), Q.OR)
        
        job_skills = JobPostSkillSet.objects.filter(query)
        job_posts = JobPost.objects.filter(
            id__in=[job_skill.job_post.id for job_skill in job_skills]
        )
        
        if job_posts.exists():
            serialized_posts = JobPostSerializer(job_posts, many=True)
            return Response(serialized_posts.data)
        
        return Response(status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        """
        * exists를 사용하려면 filter로 값을 받아와야 함
        
        1. job_type이 만약 테이블에 없다면 400 에러 메세지
           -> 먼저 JobType 모델에 해당 값이 존재하는지 찾아보자.
           -> find_job_type으로 찾고, 결과가 나오면 JobType object (1) 또는 JobType object (2)로 나옴
        2. 회사 이름이 존재 하지 않으면 생성해서 채용공고를 등록
           -> 회사 이름이 존재하는지 찾아보자. 
           -> 만약 회사 이름이 없다면 <QuerySet []>이 반환됨
           -> 회사 이름이 없다면 이름을 채워 저장하고, 있다면 해당하는 이름 중 첫번째 값 가져옴
        3. JobPostSerializer에 수정된 데이터를 넣음
        4. 그리고 is_valid()를 통해 데이터가 형식에 맞게, 필드에 맞게 잘 들어왔다면
           저장하고, 아니라면 에러 메세지 보내줌
        """
        # 1
        job_type = int(request.data.get("job_type", None))
        find_job_type = JobType.objects.filter(id=job_type)
        if not find_job_type.exists():
            return Response({"error": "invalid job type"}, status=status.HTTP_400_BAD_REQUEST)
 
        # 2
        company_name = request.data.get("company", None)
        company = Company.objects.filter(company_name=company_name)
        if not company.exists():
            company = Company(company_name=company_name).save()
        else:
            company = company.first()
        
        serialized_post = JobPostSerializer(data=request.data)

        
        if serialized_post.is_valid():
            serialized_post.save(company=company, job_type=find_job_type.first())
            return Response(serialized_post.data, status=status.HTTP_200_OK)
        
        return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)

