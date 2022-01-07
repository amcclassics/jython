import csv
import java 
lineseparator = java.lang.System.getProperty('line.separator')

def get_heap_data(jvm_name):
   serverJVM=AdminControl.completeObjectName('type=JVM,process=' + jvm_name + ',*')
   serverJVMObj=AdminControl.makeObjectName(serverJVM)
   perf=AdminControl.completeObjectName('type=Perf,process=' + jvm_name + ',*')
   perfObj=AdminControl.makeObjectName(perf)
   jvmObj=AdminControl.invoke_jmx(perfObj,'getStatsObject',[serverJVMObj,java.lang.Boolean('false')],['javax.management.ObjectName','java.lang.Boolean'])
 
   currentHeapsize=jvmObj.getStatistic('HeapSize').getCurrent()
   usedMemory=jvmObj.getStatistic('UsedMemory').getCount()
   usage=float(usedMemory)/float(currentHeapsize)*100
 
   print jvm_name+"\n====================="
   print "Used Mem: "+str(usedMemory)+"K / Current Heap Size: "+str(currentHeapsize)+"K > "+"Usage:%.2f" % usage+"%"
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

def parse_jndi_name(inputLine):
   jndiName = inputLine.split(' ')[1].split('=')[1]
   jndiName = jndiName[:-1]
   return jndiName
#endDef

def get_jdbc_conns(eachJVM):

   jdbcObjDb2 = AdminControl.queryNames('name=wpdbJDBC_db2,type=JDBCProvider,process='+eachJVM+',*').split(lineseparator)
   jdbcObjOra = AdminControl.queryNames('name=Oracle JDBC Driver,type=JDBCProvider,process='+eachJVM+',*').split(lineseparator)
   
   jdbcObjs = jdbcObjDb2 + jdbcObjOra

   #Organize the data we want into a list of dictionary objects
   jdbcStats = []
   for eachJdbc in jdbcObjs:
      if eachJdbc == "":
         continue  #skip loop iteration if array has no value
      #endif

      jdbcProvStats = AdminControl.getAttribute(eachJdbc,'stats').split(lineseparator)
      dsStats = {}
      for eachLine in jdbcProvStats:
         if eachLine.startswith('Stats name=jdbc/'): #identify the start of a data source stats entry
            dsStats["DataSource"] = parse_jndi_name(eachLine)
         if eachLine.startswith('name=PoolSize'):
            dsStats["PoolSize"] = print_current(eachLine)
         if eachLine.startswith('name=FreePoolSize'):
            dsStats["FreePoolSize"] = print_current(eachLine)
         if eachLine.startswith('}'):   #Reset the list if datasource info ends
            jdbcStats.append(dsStats)
            dsStats = {}
         #endIfs
      #endFor
   #endFor
   
   #Print the data pretty
   for eachJdbcStats in jdbcStats:
      actConns = str(int(eachJdbcStats.get("PoolSize")) - int(eachJdbcStats.get("FreePoolSize")))
      print "Datasource: " + eachJdbcStats.get("DataSource") +"   >  Active Connections: "+actConns+"   >   Pool Size: "+eachJdbcStats.get("FreePoolSize")
   #endFor
#endDef

reader = csv.reader([sys.argv[0]])
for eachLine in reader:
   for eachJVM in eachLine:
      print "" 
      reuse_perfObj = get_heap_data(eachJVM)
      get_wc_threads(reuse_perfObj,eachJVM)
      get_jdbc_conns(eachJVM)
   #endFor
#endFor
