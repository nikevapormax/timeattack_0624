from rest_framework import serializers

from post.models import Company

from .models import Company
from .models import JobPost
from .models import JobPostSkillSet

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name", "business_area"]
        
class JobPostSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    
    def get_company(self, obj):
        print(dir(obj))
        return obj.company_name
    
    class Meta:
        model = JobPost
        fields = ["job_type", "company", "job_description", "salary"]
        
        
class JobPostSkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostSkillSet
        fields = ["skillset", "job_post"]