from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from core.code import codin, CodinError
from core.sig import limited_run, OutofTimeError

def index(request):
    t = get_template('index.html')
    html = t.render(Context({}))
    return HttpResponse(html)

def jq(request):
    t = get_template('jq.html')
    html = t.render(Context())
    return HttpResponse(html)


def process_codein(curcode, precode, outqueue):
    try:
        output = codin(curcode, precode, 'exec')
        # successfully run
        outqueue.put(True)
        outqueue.put(output)

    except CodinError, e:
        # False run
        outqueue.put(False)
        outqueue.put(e.msg)

    except Exception, e:
        outqueue.put(False)
        outqueue.put(e)

def hello(request):
    if 'code' not in request.session:
        request.session['code'] = ""
    
    precode = request.session['code']
    curcode = request.GET['code'].lstrip()

    try:
        output = limited_run(process_codein, 0.5, curcode, precode)
    except OutofTimeError:
        return HttpResponse("Out of Time")
    except CodinError, e:
        return HttpResponse(e.msg)
    except Exception, e:
        return HttpResponse("Current Code Error: %s" % str(e))

    # successfully run
    request.session['code'] += curcode + '\n'
    #res = 'Res: ' + str(output) + '<br/>'
    return HttpResponse(str(output))
