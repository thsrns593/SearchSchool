from django.shortcuts import render
from django.http import HttpResponse
from common.schoolClass import SelectSH
import json
# Create your views here.

def handler(request):


    region = request.POST.get('region', '')
    region_list = region.split(" ")

    if len(region_list) == 3:
        region_list = [region_list[0], ' '.join([region_list[1],region_list[2]])]
    else:
        return HttpResponse("잘못된 주소입니다")
    
    schoolName = request.POST.get('schoolName', '')
    #situation = request.POST.get('situation', '')
    sh = SelectSH()
    result = sh.data_worker(region_list, schoolName) 
    #result = sh.data_worker(['경기도','안양시','만안구'],"성문중학교")
    result2 = sh.total_current_situation()
    return HttpResponse(json.dumps(result2))
