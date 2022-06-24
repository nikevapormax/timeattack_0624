from rest_framework import serializers

from post.models import Company

from .models import Company
from .models import JobPost
from .models import JobPostSkillSet
from .models import JobType

class JobTypeSerializer(serializers.ModelSerializer):
    """
    JobType 모델에서 id 값과 job_type을 가져온다.
    """
    
    class Meta:
        model = JobType
        fields = ["id", "job_type"]

class CompanySerializer(serializers.ModelSerializer):
    """
    Company 모델에서 id 값과 company_name을 가져온다.
    """
    
    class Meta:
        model = Company
        fields = ["id", "company_name"]
        
class JobPostSerializer(serializers.ModelSerializer):
    """
    1. job_type과 company는 ForeignKey 
    2. job_description과 salary는 JobPost 모델에 있는 정보
    
    1. company는 회사의 정보를 다른 테이블에서 가져와 정보를 보여주는 것이므로 read_only 
       -> id와 company_name을 보여줌
    2. job_type 테이블에서는 job_type이라는 정보를 가져올 수 있음
       -> JobPost에서 JobType을 바라보고 있으므로 정참조를 사용하면 된다. 
    """
    company = CompanySerializer(read_only=True)
    # job_type = JobTypeSerializer(read_only=True)
    skillsets = serializers.SerializerMethodField()
    job_type = serializers.SerializerMethodField()
        
    def get_job_type(self, obj):
        return obj.job_type.job_type
    
    def get_skillsets(self, obj):
        print(obj.skillset_set.all())
        return [s.name for s in obj.skillset_set.all()]
    
    class Meta:
        model = JobPost
        fields = ["id", "job_type", "company", "job_description", "salary","skillsets"]
        
        
class JobPostSkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostSkillSet
        fields = ["skillset", "job_post"]