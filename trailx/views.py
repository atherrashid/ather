from django.shortcuts import render
from django.http import HttpResponse
from xml.etree.ElementTree import parse
from urllib  import urlopen
from math import log

def numfound(disease):
    doc = urlopen('http://66.228.43.27:8080/solr/select?q='+disease)
    document = parse(doc)
    root = document.getroot()
    result=root.find('result')
    numfound=result.attrib.get('numFound',0)
    return numfound

def lastcount(disease):
    doc = urlopen('http://66.228.43.27:8080/solr/select?q='+disease)
    
    numfound=result.attrib.get('numFound',0)
    return numfound 

def parsexml(question,disease):
    doc = urlopen(question)
    print question
    document = parse(doc)
    root = document.getroot()
    result = root.find("./lst/lst/lst")
    numfounds=numfound(disease)
    entrop=0
    for i in result:
        val=i.text
        x=float(val)/float(numfounds)
        print x
        if x > 0.0000000000001:
            y=x*log(x)
            print y
            entrop=entrop+y
    return entrop
    
    
def nextquestion(disease):
    lst=['city','phase','state','gender','treatment_status']
    storedentropy=[]
    for i in lst:
        temp=[]
        question='http://66.228.43.27:8080/solr/select?q='+disease+'&facet=true&facet.field='+i+'&rows=0'
        entrop=parsexml(question,disease)
        temp.append(i)
        temp.append(entrop)
        storedentropy.append(temp)
    storedentropy.sort(key=lambda x: x[1], reverse=True)
    print storedentropy
    return storedentropy

    
def index(request):
    values=request.GET
    name=values.get('name')
    step = values.get('step')
    if  not step:
        context = {}
	return render(request, 'index.html', context)
    
    nq=nextquestion(name)
    step=int(step)
    template=nq[step-1][0]
    formvalues=None
    disease = name
    if step>1:
        formvalue=nq[step-2][0]
        formvalues=values.get(formvalue)
        disease = name
        disease =name+'&fq='+formvalue+':'+str(formvalues)
        print disease
    trials=numfound(disease)
    if step==6:
        trials=lastcount(disease)
        context = {'trials': trials,'step':step,'disease': disease}
	return render(request, 'result.html', context)
    
    step = step+1
    context = {'trials': trials,'step':step,'disease': disease}
    return render(request, template+'.html', context)
