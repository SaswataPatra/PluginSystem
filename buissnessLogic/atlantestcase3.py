from dotenv import load_dotenv
import os
def atlantestcase3_func(request) -> bool:
	 #plugin developers code goes here 
	load_dotenv()
	monthly_savings = request.get('monthly_savings')
	monthly_income = request.get('monthly_income')

	if monthly_savings>monthly_income:

		msg = os.environ.get("ATLANTESTCASE3MSG")
		return False,msg

	return True,"Valid response"