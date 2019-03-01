
from models import *

lst=TblAgentAllocation.objects.select_related('al_agent').select_related('al_master').all()
for obj in lst:
    print(obj.al_agent.username)

print("\nHello")