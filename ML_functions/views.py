from django.shortcuts import render
import sys
from subprocess import run,PIPE
import pandas as pd
import time

# Create your views here.

def hello_world(request):
	return render(request, 'hello_world.html',{});

def main_page(request):
	return render(request, 'main_page.html',{});

def page_knn(request):
	return render(request, 'page_knn.html',{});

def top(request):
	return render(request, 'top.html',{});

def left(request):
	return render(request, 'left.html',{});

def img1(request):
	return render(request, 'img1.html',{});

def img2(request):
	return render(request, 'img2.html',{});

def heatmap(request):
	return render(request, 'heatmap.html',{});

def kmeans(request):
	return render(request, 'kmanalysis.html',{});

def top_bg(request):
	return render(request, 'top_bg.jpg',{});

def left_bg(request):
	return render(request, 'left_bg.jpg',{});

def graph1(request):
	return render(request, 'graph1.png',{});

def graph2(request):
	return render(request, 'graph2.png',{});

def external(request):
	inp = request.POST.get('param')
	out = run([sys.executable,'/home/ninad/workspace/movie_rcm/hello_world/test.py',inp],shell=False,stdout=PIPE)
	#out = run([sys.executable,'/home/ninad/workspace/movie_rcm/hello_world/kmeans.py'],shell=False,stdout=PIPE)
	
	time.sleep(3)
	result = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/output.csv')
	result = result.reset_index()
	result = result.drop(['index'],axis=1)
	#print(out)
	
	return render(request,'main_page.html',{'data1':result.to_html(index=False, justify="center").replace('<th>','<th style = "background-color: grey" align="center">')});
	

def get_knn(request):
	inp = request.POST.get('param')
	out = run([sys.executable,'/home/ninad/workspace/movie_rcm/hello_world/knn.py',inp],shell=False,stdout=PIPE)
	
	time.sleep(3)
	result = pd.read_csv('/home/ninad/workspace/movie_rcm/hello_world/output_knn.csv')
	result = result.reset_index()
	result = result.drop(['index'],axis=1)
	#print(out)
	
	return render(request,'page_knn.html',{'data2':result.to_html(index=False, justify="center").replace('<th>','<th style = "background-color: grey" align="center">')});
	

def kmeans(request):
	out = run([sys.executable,'/home/ninad/workspace/movie_rcm/hello_world/kmeans.py'],shell=False,stdout=PIPE)
	
	return render(request,'main_page.html',{});


