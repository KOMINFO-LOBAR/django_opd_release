class CustomCorsMiddleware:
	def __init__(A,get_response):A.get_response=get_response
	def __call__(B,request):A=B.get_response(request);A['Access-Control-Allow-Origin']='*';A['Access-Control-Allow-Headers']='*';return A