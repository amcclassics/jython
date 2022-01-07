import csv

def get_heap_data(jvm_name):
   serverJVM=AdminControl.completeObjectName('type=JVM,process=' + jvm_name + ',*')
   serverJVMObj=AdminControl.makeObjectName(serverJVM)
   perf=AdminControl.completeObjectName('type=Perf,process=' + jvm_name + ',*')
   perfObj=AdminControl.makeObjectName(perf)
   jvmObj=AdminControl.invoke_jmx(perfObj,'getStatsObject',[serverJVMObj,java.lang.Boolean('false')],['javax.management.ObjectName','java.lang.Boolean'])
 
   currentHeapsize=jvmObj.getStatistic('HeapSize').getCurrent()
   usedMemory=jvmObj.getStatistic('UsedMemory').getCount()
   usage=float(usedMemory)/float(currentHeapsize)*100
 
   print jvm_name + " Used Mem: "+str(usedMemory)+"K / Current Heap Size: "+str(currentHeapsize)+"K > "+"Usage:%.2f" % usage+"%"
   reuse_perfObj = perfObj
   return reuse_perfObj
#endDef

def print_current(inputLine):
   for eachVal in inputLine.split(','):
      if eachVal.strip().startswith('current='):
         paraName,paramValue = eachVal.strip().split('=')
      #endIf
   #endFor
   return paramValue
#endDef


def get_wc_threads(reuse_perfObj,eachJVM):
  sigs = ['javax.management.ObjectName','java.lang.Boolean']
  threadPoolName = AdminControl.completeObjectName('name=WebContainer,type=ThreadPool,process='+eachJVM+',*')
  params = [AdminControl.makeObjectName (threadPoolName), java.lang.Boolean ('false')]
  thread_data = str(AdminControl.invoke_jmx(reuse_perfObj, 'getStatsObject', params, sigs)).splitlines()
  for eachThreadLine in thread_data:
     if eachThreadLine.startswith('name=ActiveCount'):
        active_threads = print_current(eachThreadLine)
     if eachThreadLine.startswith('name=PoolSize'):
        thread_poolsize = print_current(eachThreadLine)
  print "WebContainer Threads:  Active / PoolSize   >  " + active_threads + "/" + thread_poolsize
  #endFor

reader = csv.reader([sys.argv[0]])
for eachLine in reader:
   for eachJVM in eachLine:
      #print str(eachJVM)
      reuse_perfObj = get_heap_data(eachJVM)
      get_wc_threads(reuse_perfObj,eachJVM)
   #endFor
#endFor
